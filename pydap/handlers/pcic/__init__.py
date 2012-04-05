import os
import re
from StringIO import StringIO
import psycopg2

from pydap.handlers.sql import Handler as SqlHandler

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

        net_name, stn_id = re.search(r"/([^/]+)/([^/]+)\..sql", filepath).groups()
        print net_name, stn_id
        q = "SELECT station_id FROM meta_station NATURAL JOIN meta_network WHERE native_id = '%s' AND network_name = '%s'" % (stn_id, net_name)
        cur.execute(q)
        stn_id = cur.fetchone()

        full_query = self.get_full_query(stn_id, cur)

        get_loc_query = "SELECT x(the_geom) as longitude, y(the_geom) as latitude FROM meta_history WHERE station_id = %s" % stn_id
        cur.execute(get_loc_query)
        try:
            lat, lon = cur.fetchone()
        except TypeError:
            lat = lon = float('nan')

        get_stn_query = "SELECT native_id, station_name, network_name FROM meta_history NATURAL JOIN meta_station NATURAL JOIN meta_network WHERE station_id = %s" % stn_id
        cur.execute(get_stn_query)
        try:
            station_id, station_name, network = cur.fetchone()
        except TypeError:
            station_id, station_name, network = (stn_id, '', '')

        dsn = "postgresql://%(user)s:'%(password)s'@%(host)s/%(database)s" % conn_params
        s = '''[database]
dsn = "%s"
id = "obs_time"
table = "(%s) as foo"

[dataset]

    [[NC_GLOBAL]]
    name = "CRMP/%s"
    owner = "PCIC"
    contact = "Faron Anslow <fanslow@uvic.ca>"
    version = 0.1
    station_id = "%s"
    station_name = "%s"
    network = "%s"
    latitude = %f
    longitude = %f
    history = "Created dynamically by the Pydap SQL handler, the Pydap PCIC SQL handler, and the PCIC/CRMP database"

[sequence]
name = "station_observations"

[time]
name = "time"
axis = "T"
col = "obs_time"
units = "seconds since 1970-01-01"
long_name = "observation time"
type = "Float64"
missing_value = -9999

''' % (dsn, full_query, network, station_id, station_name, network, lat, lon)

        get_var_query = "SELECT net_var_name, unit, standard_name, cell_method, long_description FROM meta_station NATURAL JOIN meta_network NATURAL JOIN meta_vars WHERE station_id = %s AND cell_method !~ '(within|over)'" % stn_id
        stn_vars = self.get_vars(stn_id, cur)
        
        for var_name, unit, standard_name, cell_method, long_description, display_name in stn_vars:
            s = s + '''[%s]
name = "%s"
display_name = "%s"
long_name = "%s"
standard_name = "%s"
units = "%s"
cell_method = "%s"
col = "%s"
axis = "Y"
missing_value = -9999

''' %(var_name, var_name, display_name, long_description, standard_name, unit, cell_method, var_name)

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
