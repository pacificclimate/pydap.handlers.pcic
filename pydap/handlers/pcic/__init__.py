import os
import re
from StringIO import StringIO
import psycopg2
import pdb

from pydap.handlers.sql import Handler as SqlHandler

class PcicSqlHandler(SqlHandler):

    extensions = re.compile(r"^.*\.psql$", re.IGNORECASE)
    con = psycopg2.connect(database='crmp', user='httpd', password='R3@d0nly', host='localhost')

    # stn_id should be the native station id.  The database station_id is looked up from that.
    def __init__(self, stn_id):

        stn_id = stn_id.split(os.sep)[-1].split('.')[0]
        q = "SELECT station_id FROM meta_station WHERE native_id = '%s'" % stn_id
        cur = self.con.cursor()
        cur.execute(q)
        stn_id = cur.fetchone()

        query_string = "SELECT query_one_station(%s)" % stn_id
        cur = self.con.cursor()
        cur.execute(query_string)
        full_query = cur.fetchone()

        get_loc_query = "SELECT x(the_geom) as longitude, y(the_geom) as latitude FROM meta_history WHERE station_id = %s" % stn_id
        cur.execute(get_loc_query)
        lat, lon = cur.fetchone()

        get_stn_query = "SELECT native_id, station_name, network_name FROM meta_history NATURAL JOIN meta_station NATURAL JOIN meta_network WHERE station_id = %s" % stn_id
        cur.execute(get_stn_query)
        station_id, station_name, network = cur.fetchone()
        
        s = '''[database]
dsn = "postgresql://httpd:'R3@d0nly'@localhost/crmp"
id = "obs_time"
table = "(%s) as foo"

[dataset]
name = "CRMP/%s"
owner = "PCIC"
contact = "hiebert@uvic.ca"
version = 0.1

    [[NC_GLOBAL]]
    history = "Created dynamically by the Pydap SQL handler, the Pydap PCIC SQL handler, and the PCIC/CRMP database"

[sequence]
name = "station_observations"
station_id = "%s"
station_name = "%s"
network = "%s"
latitude = %f
longitude = %f

[time]
name = "time"
col = "obs_time"
units = "seconds since 1970-01-01"
long_name = "observation time"
type = "Float64"
missing_value = -9999

''' % (full_query[0], network, station_id, station_name, network, lat, lon)

        get_var_query = "SELECT net_var_name, unit, standard_name, cell_method, long_description FROM meta_station NATURAL JOIN meta_network NATURAL JOIN meta_vars WHERE station_id = %s" % stn_id
        cur.execute(get_var_query)
        
        for var_name, unit, standard_name, cell_method, long_description in cur.fetchall():
            s = s + '''[%s]
name = "%s"
long_name = "%s"
standard_name = "%s"
units = "%s"
cell_method = "%s"
col = "%s"
axis = "Y"
missing_value = -9999

''' %(var_name, var_name, long_description, standard_name, unit, cell_method, var_name)

        print s
        s = StringIO(s)

        SqlHandler.__init__(self, s)
        print "In SqlHander.__init__(self, s)"

if __name__ == '__main__':

    import sys
    from paste.httpserver import serve

    application = PcicSqlHandler(sys.argv[1])
    serve(application, host='0.0.0.0', port=8002)
