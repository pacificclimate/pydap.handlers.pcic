import sys
import string
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-v', '--tb=no', 'tests']
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)                                                                        

__version__ = (0, 0, 4)

setup(
    name="pydap.handlers.pcic",
    description="A custom handler for PCIC's in-situ observational database",
    keywords="sql database opendap dods dap data science climate oceanography meteorology",
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
    dependency_links = ['https://github.com/pacificclimate/pydap.handlers.sql/tarball/master#egg=pydap.handlers.sql-0.7',
                        'https://github.com/pacificclimate/pydap.handlers.csv/tarball/master#egg=pydap.handlers.csv-0.3', #This is actually a dep for pydap.handlers.sql, but pip doesn't follow dependency links past one level
                        'https://github.com/pacificclimate/pydap.responses.html/tarball/master#egg=pydap.responses.html-0.2',
                        'https://github.com/pacificclimate/pycds/tarball/master#egg=pycds',
                        'https://github.com/pacificclimate/pydap-pdp/tarball/master#egg=Pydap-3.2.2',
                        'https://github.com/pacificclimate/pysqlite/tarball/master#egg=pysqlite'],
    install_requires = ['pydap.handlers.sql',
                        'pycds',
                        'pydap.responses.html',
                        'Pydap >=3.2.1',
                        'sqlalchemy',
                        'paste'],
    tests_require=['pytest',
                   'pysqlite',
                   'webob'],
    cmdclass = {'test': PyTest},
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
