'''This module provides an Pydap handler which reads in-situ observations out of the BC Provincial Climate Data Set. It is implemented as a subclass of :class:`pydap.handlers.sql.Handler` (the Pydap SQL handlers). Since the Pydap SQL handler is written to use an on-disk config file for each dataset, this handlers generates the config file dynamically in memory and then uses it to instantiate the base class.

The handler will configure a different dataset for each station based on the file path of the request. In general the file path is assumed to be ::

.../(raw|climo)/[network_name]/[native_id]/

Each dataset will contain a variety of global attributes such as the station and network names, latitude and longitide of the station and some contact information. Each dataset will contain one sequence named ``station_observations`` and some number of variables (including time) attached to that sequence. Each variable will be attributed with its name, long_name, CF standard_name, CF cell_method and the units.
'''

import os, sys
import re
from StringIO import StringIO
from sqlalchemy import create_engine

from pydap.handlers.sql import Handler as SqlHandler, DBPOOL, DBLOCK
from pdb import set_trace

class PcicSqlHandler(SqlHandler):
    '''A Pydap handler which reads in-situ observations from the BC Provincial Climate Data Set.
    '''
    extensions = re.compile(r"^.*\.psql$", re.IGNORECASE)

    @staticmethod
    def getcur(params):
        '''Gets a database engine to be used for queries. Either uses the engine stored at the module leve in :mod:`pydap.handlers.sql`, if available, or creates it, if not.

           :param params: dict containing the parameters to an :mod:`sqlalchemy` DSN, in particular `user`, `password`, `host`, and `database`
           :type params: dict
           :rtype: sqlalchemy.Engine
        '''
        dsn = "postgresql://%(user)s:%(password)s@%(host)s/%(database)s" % params
        with DBLOCK:
            if dsn not in DBPOOL:
                DBPOOL[dsn] = create_engine(dsn)

        return DBPOOL[dsn]

    def create_ini(self, environ):
        '''Creates the actual text of a pydap SQL handler config file and returns it as a StringIO. `self.filepath` should be set before this is called. It will typically be something like ``.../[network_name]/[native_id].rsql``. The database station_id is looked up from that.
        
           :param environ: WSGI environment which *must* contain a connection params dict under the key pydap.handlers.pcic.conn_params
           :rtype: StringIO.StringIO
        '''
        filepath = self.filepath
        conn_params = eval(environ.get('pydap.handlers.pcic.conn_params'))
        cur = self.getcur(conn_params)

        net_name, native_id = re.search(r"/([^/]+)/([^/]+)\..sql", filepath).groups()

        q = "SELECT station_id FROM meta_station NATURAL JOIN meta_network WHERE native_id = '%s' AND network_name = '%s'" % (native_id, net_name)
        station_id = cur.execute(q).first()[0]

        full_query = self.get_full_query(station_id, cur)

        get_stn_query = "SELECT native_id, station_name, network_name FROM meta_history NATURAL JOIN meta_station NATURAL JOIN meta_network WHERE station_id = %s" % station_id
        rv = cur.execute(get_stn_query).first()
        try:
            native_id, station_name, network = rv
        except TypeError:
            native_id, station_name, network = (station_id, '', '')

        dsn = "postgresql://%(user)s:%(password)s@%(host)s/%(database)s" % conn_params
        s = '''database:
  dsn: "%(dsn)s"
  id: "obs_time"
  table: "(%(full_query)s) as foo"

dataset:

  NC_GLOBAL:
    name: "CRMP/%(network)s"
    owner: "PCIC"
    contact: "Faron Anslow <fanslow@uvic.ca>"
    version: 0.2
    station_id: "%(native_id)s"
    station_name: "%(station_name)s"
    network: "%(network)s"
    latitude: !Query \'SELECT st_y(the_geom) FROM meta_history WHERE station_id = %(station_id)d\'
    longitude: !Query \'SELECT st_x(the_geom) FROM meta_history WHERE station_id = %(station_id)d\'
    history: "Created dynamically by the Pydap SQL handler, the Pydap PCIC SQL handler, and the PCIC/CRMP database"

sequence:
  name: "station_observations"

time:
  name: "time"
  axis: "T"
  col: "obs_time"
  long_name: "observation time"
  type: String

''' % locals()

        stn_vars = self.get_vars(station_id, cur)
        
        for var_name, unit, standard_name, cell_method, long_description, display_name in stn_vars:
            s = s + '''%(var_name)s:
  name: "%(var_name)s"
  display_name: "%(display_name)s"
  long_name: "%(long_description)s"
  standard_name: "%(standard_name)s"
  units: "%(unit)s"
  cell_method: "%(cell_method)s"
  col: "%(var_name)s"
  axis: "Y"
  missing_value: -9999
  type: Float64

''' % locals()

        return StringIO(str(s))

    def parse_constraints(self, environ):
        self.config_lines = self.create_ini(environ).getvalue().splitlines(True)
        return SqlHandler.parse_constraints(self, environ)

    def get_full_query(self, stn_id, cur):
        raise NotImplementedError

    def get_vars(self, stn_id, cur):
        raise NotImplementedError

class RawPcicSqlHandler(PcicSqlHandler):
    '''Subclass of PcicSqlHandler which handles the raw observations
    '''
    extensions = re.compile(r"^.*\.rsql$", re.IGNORECASE)
    virtual = True

    def get_full_query(self, stn_id, cur):
        '''Sends a special query to the database that actually retrieves generated SQL for constructing an observation table (time by variable) for a single station. Uses the ``query_one_station`` stored procedure.

           :param stn_id: the *database* station_id of the desired station
           :type stn_id: int or str
        '''
        query_string = "SELECT query_one_station(%s)" % stn_id
        return cur.execute(query_string).fetchone()[0]

    def get_vars(self, stn_id, cur):
        '''Makes a database query to retrieve all of the raw variables for a particular station
        '''
        get_var_query = "SELECT net_var_name, unit, standard_name, cell_method, long_description, display_name FROM meta_network NATURAL JOIN meta_history NATURAL JOIN vars_per_history_mv NATURAL JOIN meta_vars WHERE station_id = %s AND cell_method !~ '(within|over)'" % stn_id
        return cur.execute(get_var_query).fetchall()


class ClimoPcicSqlHandler(PcicSqlHandler):
    '''Subclass of PcicSqlHandler which handles the climatological observations
    '''
    extensions = re.compile(r"^.*\.csql$", re.IGNORECASE)
    virtual = True

    def get_full_query(self, stn_id, cur):
        '''Sends a special query to the database that actually retrieves generated SQL for constructing an observation table (time by variable) for a single station. Uses the ``query_one_station`` stored procedure.

           :param stn_id: the *database* station_id of the desired station
           :type stn_id: int or str
        '''
        query_string = "SELECT query_one_station_climo(%s)" % stn_id
        return cur.execute(query_string).first()[0]

    def get_vars(self, stn_id, cur):
        '''Makes a database query to retrieve all of the climatological variables for a particular station
        '''
        get_var_query = "SELECT net_var_name, unit, standard_name, cell_method, long_description, display_name FROM meta_network NATURAL JOIN meta_history NATURAL JOIN vars_per_history_mv NATURAL JOIN meta_vars WHERE station_id = %s AND cell_method ~ '(within|over)'" % stn_id
        return cur.execute(get_var_query).fetchall()

if __name__ == '__main__':

    import sys
    from paste.httpserver import serve

    application = PcicSqlHandler(sys.argv[1])
    serve(application, host='0.0.0.0', port=8002)
