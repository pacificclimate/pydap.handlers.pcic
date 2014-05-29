'''
Basic test to see if pysqlite has spatial capatbilities
'''
def test_can_use_spatial_functions(test_session):
    res = test_session.execute("select AsText(GeomFromText( 'LINESTRING (30 10, 10 30, 40 40)' , 4326 ))")
    assert res

def test_can_select_spatial_data(test_session):
    res = test_session.execute("select AsBinary(GeomFromText( 'LINESTRING (30 10, 10 30, 40 40)' , 4326 ))")
    assert res
