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

def test_create_ini_with_multiple_hist_ids(raw_handler, monkeypatch, session_with_multiple_hist_ids_for_one_station):
    # get_full_query is not important for this test
    monkeypatch.setattr(raw_handler, 'get_full_query', lambda x, y: '' )

    s = raw_handler.create_ini(session_with_multiple_hist_ids_for_one_station, 'test_network', 'some_station')

    assert '''station_id: "some_station"
    station_name: "The same station"
    network: "test_network"
    latitude: 49.000000
    longitude: -118.000000''' in s

def test_handles_missing_sdates(raw_handler, monkeypatch, session_multiple_hist_ids_null_dates):
    # get_full_query is not important for this test
    monkeypatch.setattr(raw_handler, 'get_full_query', lambda x, y: '' )

    with pytest.raises(ValueError) as excinfo:
        raw_handler.create_ini(session_multiple_hist_ids_null_dates, 'test_network', 'some_station')

    assert "multiple history entries" in str(excinfo.value)
