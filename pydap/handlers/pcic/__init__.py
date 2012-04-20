import os
import re
from StringIO import StringIO
import psycopg2

from pydap.handlers.sql import Handler as SqlHandler
from pdb import set_trace

class PcicSqlHandler(SqlHandler):

    extensions = re.compile(r"^.*\.psql$", re.IGNORECASE)

    @staticmethod
    def getcur(params):
        con = psycopg2.connect(**params)
        return con.cursor()

    def create_ini(self, environ):
        # This will be something like .../[network_name]/[native_id].rsql
        # The database station_id is looked up from that
        filepath = self.filepath
        conn_params = eval(environ.get('pydap.handlers.pcic.conn_params'))
        cur = self.getcur(conn_params)

        net_name, native_id = re.search(r"/([^/]+)/([^/]+)\..sql", filepath).groups()

        q = "SELECT station_id FROM meta_station NATURAL JOIN meta_network WHERE native_id = '%s' AND network_name = '%s'" % (native_id, net_name)
        cur.execute(q)
        station_id = cur.fetchone()[0]

        full_query = self.get_full_query(station_id, cur)

        get_stn_query = "SELECT native_id, station_name, network_name FROM meta_history NATURAL JOIN meta_station NATURAL JOIN meta_network WHERE station_id = %s" % station_id
        cur.execute(get_stn_query)
        try:
            native_id, station_name, network = cur.fetchone()
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
    latitude: !Query \'SELECT y(the_geom) FROM meta_history WHERE station_id = %(station_id)d\'
    longitude: !Query \'SELECT x(the_geom) FROM meta_history WHERE station_id = %(station_id)d\'
    history: "Created dynamically by the Pydap SQL handler, the Pydap PCIC SQL handler, and the PCIC/CRMP database"

sequence:
  name: "station_observations"

time:
  name: "time"
  axis: "T"
  col: "obs_time"
  long_name: "observation time"
  type: "String"

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

''' % locals()

        return StringIO(s)

    def parse_constraints(self, environ):
        self.filepath = self.create_ini(environ)
        return SqlHandler.parse_constraints(self, environ)

    def get_full_query(self, stn_id, cur):
        raise NotImplementedError

    def get_vars(self, stn_id, cur):
        raise NotImplementedError

class RawPcicSqlHandler(PcicSqlHandler):
    extensions = re.compile(r"^.*\.rsql$", re.IGNORECASE)
    virtual = True

    def get_full_query(self, stn_id, cur):
        query_string = "SELECT query_one_station(%s)" % stn_id
        cur.execute(query_string)
        return cur.fetchone()[0]

    def get_vars(self, stn_id, cur):
        get_var_query = "SELECT net_var_name, unit, standard_name, cell_method, long_description, display_name FROM meta_network NATURAL JOIN meta_history NATURAL JOIN vars_per_history_mv NATURAL JOIN meta_vars WHERE station_id = %s AND cell_method !~ '(within|over)'" % stn_id
        cur.execute(get_var_query)
        return cur.fetchall()


class ClimoPcicSqlHandler(PcicSqlHandler):
    extensions = re.compile(r"^.*\.csql$", re.IGNORECASE)
    virtual = True

    def get_full_query(self, stn_id, cur):
        query_string = "SELECT query_one_station_climo(%s)" % stn_id
        cur.execute(query_string)
        return cur.fetchone()[0]

    def get_vars(self, stn_id, cur):
        get_var_query = "SELECT net_var_name, unit, standard_name, cell_method, long_description, display_name FROM meta_network NATURAL JOIN meta_history NATURAL JOIN vars_per_history_mv NATURAL JOIN meta_vars WHERE station_id = %s AND cell_method ~ '(within|over)'" % stn_id
        cur.execute(get_var_query)
        return cur.fetchall()

if __name__ == '__main__':

    import sys
    from paste.httpserver import serve

    application = PcicSqlHandler(sys.argv[1])
    serve(application, host='0.0.0.0', port=8002)
