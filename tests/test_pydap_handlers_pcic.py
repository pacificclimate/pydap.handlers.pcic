import pytest
from webob.request import Request
from sqlalchemy.orm import sessionmaker

from pycds.util import sql_station_table
from pydap.handlers.sql import Engines
from pydap.handlers.pcic import PcicSqlHandler, RawPcicSqlHandler, ClimoPcicSqlHandler

@pytest.fixture(scope="function")
def raw_handler(monkeypatch, conn_params, test_session):
    handler = RawPcicSqlHandler(conn_params, test_session)

    def my_get_full_query(self, stn_id, sesh):
        return sql_station_table(sesh, stn_id)
    monkeypatch.setattr(RawPcicSqlHandler, 'get_full_query', my_get_full_query)

    return handler

@pytest.mark.parametrize(('input', 'expected'), [
    # Raw
    (RawPcicSqlHandler(''), [('wind_gust_speed', 'km/h', 'wind_speed_of_gust', 'time: maximum', 'Maximum speed of wind gust', 'Wind Gust (Max.)'), ('air_temperature_yesterday_low', 'Celsius', 'air_temperature', 'time: minimum', 'Minimum daily air temperature', 'Temperature (Min.)'), ('air_temperature_yesterday_high', 'Celsius', 'air_temperature', 'time: maximum', 'Maximum daily air temperature', 'Temperature (Max.)'), ('wind_direction', 'degree', 'wind_from_direction', 'time: mean', 'Wind direction octants', 'Wind Direction (Mean)'), ('total_precipitation', 'mm', 'lwe_thickness_of_precipitation_amount', 'time: sum', 'Daily precipitation amount', 'Precipitation Amount')]),
    # Climo
    (ClimoPcicSqlHandler(''),[('Tx_Climatology',
                               'celsius',
                               'air_temperature',
                               't: maximum within days t: mean within months t: mean over years',
                               'Climatological mean of monthly mean maximum daily temperature',
                               'Temperature Climatology (Max.)'),
                               ('T_mean_Climatology',
                                'celsius',
                                'air_temperature',
                                't: mean within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean of mean daily temperature',
                                'Temperature Climatology (Mean)'),
                               ('Tn_Climatology',
                                'celsius',
                                'air_temperature',
                                't: minimum within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean minimum daily temperature',
                                'Temperature Climatology (Min.)'),
                               ('Precip_Climatology',
                                'mm',
                                'lwe_thickness_of_precipitation_amount',
                                't: sum within months t: mean over years',
                                'Climatological mean of monthly total precipitation',
                                'Precipitation Climatology'),
                               ('Tx_Climatology',
                                'celsius',
                                'air_temperature',
                                't: maximum within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean maximum daily temperature',
                                'Temperature Climatology (Max.)'),
                               ('T_mean_Climatology',
                                'celsius',
                                'air_temperature',
                                't: mean within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean of mean daily temperature',
                                'Temperature Climatology (Mean)'),
                               ('Tn_Climatology',
                                'celsius',
                                'air_temperature',
                                't: minimum within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean minimum daily temperature',
                                'Temperature Climatology (Min.)'),
                               ('Precip_Climatology',
                                'mm',
                                'lwe_thickness_of_precipitation_amount',
                                't: sum within months t: mean over years',
                                'Climatological mean of monthly total precipitation',
                                'Precipitation Climatology'),
                               ('Tx_Climatology',
                                'celsius',
                                'air_temperature',
                                't: maximum within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean maximum daily temperature',
                                'Temperature Climatology (Max.)'),
                               ('T_mean_Climatology',
                                'celsius',
                                'air_temperature',
                                't: mean within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean of mean daily temperature',
                                'Temperature Climatology (Mean)'),
                               ('Tn_Climatology',
                                'celsius',
                                'air_temperature',
                                't: minimum within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean minimum daily temperature',
                                'Temperature Climatology (Min.)'),
                               ('Precip_Climatology',
                                'mm',
                                'lwe_thickness_of_precipitation_amount',
                                't: sum within months t: mean over years',
                                'Climatological mean of monthly total precipitation',
                                'Precipitation Climatology'),
                               ('Tx_Climatology',
                                'celsius',
                                'air_temperature',
                                't: maximum within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean maximum daily temperature',
                                'Temperature Climatology (Max.)'),
                               ('T_mean_Climatology',
                                'celsius',
                                'air_temperature',
                                't: mean within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean of mean daily temperature',
                                'Temperature Climatology (Mean)'),
                               ('Tn_Climatology',
                                'celsius',
                                'air_temperature',
                                't: minimum within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean minimum daily temperature',
                                'Temperature Climatology (Min.)'),
                               ('Precip_Climatology',
                                'mm',
                                'lwe_thickness_of_precipitation_amount',
                                't: sum within months t: mean over years',
                                'Climatological mean of monthly total precipitation',
                                'Precipitation Climatology'),
                               ('Tx_Climatology',
                                'celsius',
                                'air_temperature',
                                't: maximum within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean maximum daily temperature',
                                'Temperature Climatology (Max.)'),
                               ('T_mean_Climatology',
                                'celsius',
                                'air_temperature',
                                't: mean within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean of mean daily temperature',
                                'Temperature Climatology (Mean)'),
                               ('Tn_Climatology',
                                'celsius',
                                'air_temperature',
                                't: minimum within days t: mean within months t: mean over years',
                                'Climatological mean of monthly mean minimum daily temperature',
                                'Temperature Climatology (Min.)'),
                               ('Precip_Climatology',
                                'mm',
                                'lwe_thickness_of_precipitation_amount',
                                't: sum within months t: mean over years',
                                'Climatological mean of monthly total precipitation',
                                'Precipitation Climatology')
                                ])])
                                                                                  
def test_get_vars(test_session, input, expected):
    assert set(input.get_vars(6594, test_session)) == set(expected)

@pytest.mark.parametrize(('net_name', 'native_id', 'expected'), [
                         ('EC_raw','1106200',
                          ['station_id: "1106200"',
                           'station_name: "Point Atkinson"',
                           'network: "EC_raw"',
                           'standard_name: "lwe_thickness_of_precipitation_amount"'
                           ]
                          ),
                         ('ARDA','109147',
                          ['station_id: "109147"',
                           'station_name: "AIRPORT"',
                           'network: "ARDA"',
                           'standard_name: "lwe_thickness_of_precipitation"'
                           ]
                         )])
def test_create_ini(raw_handler, net_name, native_id, expected, monkeypatch, test_session):
    # get_full_query is not important for this test
    monkeypatch.setattr(raw_handler, 'get_full_query', lambda x, y: '' )
    s = raw_handler.create_ini(test_session, net_name, native_id)

    for substr in expected:
        print substr
        assert substr in s

def test_monkey(raw_handler, test_session):
    s = raw_handler.get_full_query(913, test_session)
    rv = test_session.execute(s)

@pytest.mark.parametrize('url', [
    '/EC/913/junk', # unparseable path
    '/EC/913.sql.html' # non-existant station
    ])
def test_404s(raw_handler, url):
    req = Request.blank(url)
    resp = req.get_response(raw_handler)

    assert '404' in resp.status

def test_returns_content(raw_handler):
    '''This is not a good 'unit' test in that it relies on some intergration with Pydap
       Unfortunately this is the case... this whole _package_ relies heavily on Pydap!
    '''
    url = '/EC/1106200.rsql.das'
    req = Request.blank(url)
    resp = req.get_response(raw_handler)
    assert resp.status == '200 OK'

    assert '''        MAX_TEMP {
            String display_name "Temperature (Max.)";
            String name "MAX_TEMP";
            String cell_method "time: maximum";''' in resp.body

def test_returns_html_content(raw_handler):
    '''This is not a good 'unit' test in that it relies on some intergration with Pydap
       Unfortunately this is the case... this whole _package_ relies heavily on Pydap!
    '''
    url = '/EC/1106200.rsql.html'
    req = Request.blank(url)
    resp = req.get_response(raw_handler)
    assert resp.status == '200 OK'
