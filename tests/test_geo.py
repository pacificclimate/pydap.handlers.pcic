'''
Basic test to see if pysqlite has spatial capatbilities
'''
def test_can_use_postgis(test_session):
    res = test_session.execute("SELECT PostGIS_full_version()")
    assert res
