import pytest

def test_create_ini_with_bad_station_id(raw_handler, monkeypatch, session_with_duplicate_station):
    # get_full_query is not important for this test
    monkeypatch.setattr(raw_handler, 'get_full_query', lambda x, y: '' )

    s = raw_handler.create_ini(session_with_duplicate_station, 'EC_raw', '1106200')

    assert '''station_id: "1106200"
    station_name: ""
    network: "EC_raw"
    latitude: nan
    longitude: nan''' in s
