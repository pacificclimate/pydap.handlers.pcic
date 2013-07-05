import pytest

from pydap.handlers.pcic import PcicSqlHandler, RawPcicSqlHandler, ClimoPcicSqlHandler

def test_composite(test_session):
    pass

def test_raw(test_session):
    pass

def test_climo(test_session):
    pass

@pytest.mark.parametrize(('input', 'expected'), [
    # No valid filters
    (RawPcicSqlHandler(''), [('wind_gust_speed', 'km/h', 'wind_speed_of_gust', 'time: maximum', 'Maximum speed of wind gust', 'Wind Gust (Max.)'), ('air_temperature_yesterday_low', 'Celsius', 'air_temperature', 'time: minimum', 'Minimum daily air temperature', 'Temperature (Min.)'), ('air_temperature_yesterday_high', 'Celsius', 'air_temperature', 'time: maximum', 'Maximum daily air temperature', 'Temperature (Max.)'), ('wind_direction', 'degree', 'wind_from_direction', 'time: mean', 'Wind direction octants', 'Wind Direction (Mean)'), ('total_precipitation', 'mm', 'lwe_thickness_of_precipitation_amount', 'time: sum', 'Daily precipitation amount', 'Precipitation Amount')]),
    # One valid filter
    (ClimoPcicSqlHandler(''), [])
    ])

def test_get_vars(test_session, input, expected):
    assert set(input.get_vars(6594, test_session)) == set(expected)
