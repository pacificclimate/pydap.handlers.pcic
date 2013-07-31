import sys
import string
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-v', '-v']
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)                                                                        

__version__ = (0, 0, 2)

sw_path = 'hg+ssh://medusa.pcic.uvic.ca//home/data/projects/comp_support/software'

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
    dependency_links = ['{0}/pydap.handlers.sql@9d5d7347ef67#egg=pydap.handlers.sql-0.6dev'.format(sw_path),
                        '{0}/PyCDS@0.0.12#egg=pycds-0.0.12'.format(sw_path),
                        '{0}/Pydap-3.2@c604b6780699#egg=Pydap-3.2.1dev'.format(sw_path),
                        '{0}/pydap.responses.html@d8689fab1694#egg=pydap.responses.html-0.2dev'.format(sw_path)],
    install_requires = ['pydap.handlers.sql==0.6dev',
                        'pycds>=0.0.12',
                        'pydap.responses.html==0.2dev'],
    tests_require=['pytest',
                   'sqlalchemy',
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
