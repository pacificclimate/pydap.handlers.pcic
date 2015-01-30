import datetime

import pytest
import pycds
from pycds.util import create_test_database
from pycds.util import sql_station_table

from pydap.handlers.pcic import RawPcicSqlHandler


@pytest.fixture(scope="module")
def test_session():
    return pycds.test_session()

@pytest.fixture(scope="module")
def conn_params():
    return pycds.test_dsn

# FIXME: We should consider adding an empty, in-ram session function to pycds.util
@pytest.fixture(scope="function")
def in_ram_session():
    from pysqlite2 import dbapi2 as sqlite
    from sqlalchemy import create_engine, event
    from sqlalchemy.orm import sessionmaker

    dsn = 'sqlite:///'
    engine = create_engine(dsn, module=sqlite, echo=True)
    engine.echo = True

    # Make sure spatial extensions are loaded for each connection, not just the current session                                                      # https://groups.google.com/d/msg/sqlalchemy/eDpJ-yZEnqU/_XJ4Pmd712QJ                                                                        
    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_rec):
        dbapi_connection.enable_load_extension(True)
        dbapi_connection.execute("select load_extension('libspatialite.so')")

    create_test_database(engine)

    Session = sessionmaker(bind=engine)
    sesh = Session()
    
    return sesh

@pytest.fixture(scope="function")
def session_with_duplicate_station(in_ram_session):
    '''In 0.0.5, if there's bad data in the database where there's a spurrious station
       without a corresponding history_id, it gets selected first and then the
       metadata request fails. Construct a test database to test for this.
    '''
    s = in_ram_session

    ecraw = pycds.Network(name='EC_raw')
    station0 = pycds.Station(native_id='1106200', network=ecraw, histories=[])
    history1 = pycds.History()
    station1 = pycds.Station(native_id='1106200', network=ecraw, histories=[history1])
    s.add_all([ecraw, station0, station1, history1])
    s.commit()

    return s

@pytest.fixture(scope="function")
def session_with_multiple_hist_ids_for_one_station(in_ram_session):
    s = in_ram_session

    net = pycds.Network(name='test_network')
    history0 = pycds.History(station_name='Some station', elevation=999,
                             sdate = datetime.datetime(1880, 1, 1),
                             edate = datetime.datetime(2000, 1, 1))
    # Empty end date... i.e. and "active station"
    history1 = pycds.History(station_name='The same station', elevation=999,
                             sdate = datetime.datetime(2000, 1, 2),
                             the_geom = 'POINT(-118 49)')
    station0 = pycds.Station(native_id='some_station', network=net, histories=[history0, history1])
    s.add(station0)
    s.commit()

    return s

@pytest.fixture(scope="function")
def session_multiple_hist_ids_null_dates(in_ram_session):
    s = in_ram_session

    net = pycds.Network(name='test_network')
    history0 = pycds.History(station_name='Some station', elevation=999)
    history1 = pycds.History(station_name='The same station', elevation=999)
    station0 = pycds.Station(native_id='some_station', network=net, histories=[history0, history1])
    s.add(station0)
    s.commit()

    return s

@pytest.fixture(scope="function")
def raw_handler(monkeypatch, conn_params, test_session):
    handler = RawPcicSqlHandler(conn_params, test_session)

    def my_get_full_query(self, stn_id, sesh):
        return sql_station_table(sesh, stn_id)
    monkeypatch.setattr(RawPcicSqlHandler, 'get_full_query', my_get_full_query)

    return handler

