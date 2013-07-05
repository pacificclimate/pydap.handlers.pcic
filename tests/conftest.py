import pytest
import pycds
import pcic

@pytest.fixture(scope="module")
def test_session():
    sesh = pcic.get_session('sqlite+pysqlite:///{0}'.format(pycds.test_dsn))()
    return sesh

@pytest.fixture(scope="module")
def conn_params():
    return 'sqlite+pysqlite:///{0}'.format(pycds.test_dsn)
