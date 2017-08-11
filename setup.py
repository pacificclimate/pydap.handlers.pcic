import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
from pkg_resources import resource_filename
import ctypes
import warnings

__version__ = (0, 0, 8)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["-v", "--tb=no", "-m", "not poor_unittest", "tests"]
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        if not check_for_spatialite():
            raise Exception(
                "Cannot run without libspatialite, which is not installed"
            )
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def check_for_spatialite():
    try:
        ctypes.cdll.LoadLibrary('libspatialite.so')
    except OSError:
        warnings.warn(
            "libspatialite must be installed if you want to run the tests"
        )
        return False

    from sqlalchemy import create_engine

    msg = 'Unfortunately, for using sqlite for testing geographic '
    'functionality , you need to manually install pysqlite2 '
    'according to the instructions here: '
    'http://www.geoalchemy.org/usagenotes.html#notes-for-spatialite '
    'Otherwise, you will not be able to run any of the unit tests '
    'for this package for any packages which depend upon it.'

    try:
        from pysqlite2 import dbapi2
    except ImportError:
        warnings.warn('pysqlite2 package is not installed.\n' + msg)
        return False

    dsn = 'sqlite:///{0}'.format(
        resource_filename('pycds', 'data/crmp.sqlite')
    )
    engine = create_engine(dsn, module=dbapi2, echo=True)
    con = engine.raw_connection().connection
    if not hasattr(con, 'enable_load_extension'):
        warnings.warn('The pysqlite2 package has been built without extension '
                      'loading support.\n' + msg)
        return False
    else:
        return True

setup(
    name="pydap.handlers.pcic",
    description="A custom handler for PCIC's in-situ observational database",
    keywords="sql database opendap dods dap data science climate oceanography"
             "meteorology",
    packages=['pydap', 'pydap.handlers', 'pydap.handlers.pcic'],
    version='.'.join(str(d) for d in __version__),
    url="http://www.pacificclimate.org/",
    author="James Hiebert",
    author_email="hiebert@uvic.ca",
    namespace_packages=['pydap', 'pydap.handlers'],
    entry_points='''[pydap.handler]
                    rsql = pydap.handlers.pcic:RawPcicSqlHandler
                    csql = pydap.handlers.pcic:ClimoPcicSqlHandler
                 ''',
    install_requires=[
        'pydap.handlers.sql',
        'pycds',
        'pydap.responses.html',
        'pydap_pdp >=3.2.1',
        'sqlalchemy',
        'paste'
    ],
    tests_require=['pytest',
                   'pysqlite',
                   'webob'],
    cmdclass={'test': PyTest},
    zip_safe=True,
    classifiers='''Development Status :: 2 - Pre-Alpha
Environment :: Console
Environment :: Web Environment
Framework :: Paste
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: GNU General Public License (GPL)
Operating System :: OS Independent
Programming Language :: Python
Topic :: Internet
Topic :: Internet :: WWW/HTTP :: WSGI
Topic :: Scientific/Engineering
Topic :: Software Development :: Libraries :: Python Modules'''.split('\n')
)
