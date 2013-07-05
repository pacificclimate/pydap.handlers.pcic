import pytest

from pydap.handlers.pcic import PcicSqlHandler, RawPcicSqlHandler, ClimoPcicSqlHandler, __file__

@pytest.fixture(scope="module")
def test_session():
    sesh = pcic.get_session('sqlite+pysqlite:///{0}/data/crmp.sqlite'.format(dirname(__file__)))()
    return sesh


def test_composite():
    pass

def test_raw():
    pass

def test_climo():
    pass

