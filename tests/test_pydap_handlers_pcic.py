import pytest

from pydap.handlers.pcic import PcicSqlHandler, RawPcicSqlHandler, ClimoPcicSqlHandler

def test_composite(test_session):
    pass

def test_raw(test_session):
    pass

def test_climo(test_session):
    pass

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

def raw_query(*args):
    return '''SELECT * FROM(SELECT obs_time, datum AS air_temperature, flag_name as air_temperature_flag FROM obs_with_flags WHERE vars_id = 542 AND station_id = 6628) AS a FULL OUTER JOIN (SELECT obs_time, datum AS wind_gust_speed, flag_name as wind_gust_speed_flag FROM obs_with_flags WHERE vars_id = 543 AND station_id = 6628) AS aa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS air_temperature_yesterday_low, flag_name as air_temperature_yesterday_low_flag FROM obs_with_flags WHERE vars_id = 545 AND station_id = 6628) AS aaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS air_temperature_yesterday_high, flag_name as air_temperature_yesterday_high_flag FROM obs_with_flags WHERE vars_id = 544 AND station_id = 6628) AS aaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS dew_point, flag_name as dew_point_flag FROM obs_with_flags WHERE vars_id = 551 AND station_id = 6628) AS aaaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS wind_speed, flag_name as wind_speed_flag FROM obs_with_flags WHERE vars_id = 550 AND station_id = 6628) AS aaaaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS snow_amount, flag_name as snow_amount_flag FROM obs_with_flags WHERE vars_id = 548 AND station_id = 6628) AS aaaaaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS mean_sea_level, flag_name as mean_sea_level_flag FROM obs_with_flags WHERE vars_id = 549 AND station_id = 6628) AS aaaaaaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS relative_humidity, flag_name as relative_humidity_flag FROM obs_with_flags WHERE vars_id = 552 AND station_id = 6628) AS aaaaaaaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS total_rain, flag_name as total_rain_flag FROM obs_with_flags WHERE vars_id = 547 AND station_id = 6628) AS aaaaaaaaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS tendency_amount, flag_name as tendency_amount_flag FROM obs_with_flags WHERE vars_id = 555 AND station_id = 6628) AS aaaaaaaaaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS wind_direction, flag_name as wind_direction_flag FROM obs_with_flags WHERE vars_id = 553 AND station_id = 6628) AS aaaaaaaaaaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS total_cloud_cover, flag_name as total_cloud_cover_flag FROM obs_with_flags WHERE vars_id = 554 AND station_id = 6628) AS aaaaaaaaaaaaa USING (obs_time) FULL OUTER JOIN (SELECT obs_time, datum AS total_precipitation, flag_name as total_precipitation_flag FROM obs_with_flags WHERE vars_id = 546 AND station_id = 6628) AS aaaaaaaaaaaaaa USING (obs_time)'''

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
                           'standard_name: "surface_snow_thickness"'
                           ]
                         )])
def test_create_ini(conn_params, net_name, native_id, expected, monkeypatch):
    x = RawPcicSqlHandler(conn_params)
    # get_full_query is not important for this test
    monkeypatch.setattr(x, 'get_full_query', lambda x, y: '' )
    s = x.create_ini(net_name, native_id)

    for substr in expected:
        print substr
        assert substr in s

