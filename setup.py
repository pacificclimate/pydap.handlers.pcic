import string
from setuptools import setup

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
    dependency_links = ['{sw_path}/pydap.handlers.sql@780393261100#egg=pydap.handlers.sql-0.5rc1'.format(**locals()),
                        '{sw_path}/PyCDS@0.0.8#egg=pycds-0.0.8'.format(**locals())], #
    install_requires = ['setuptools==0.9.8', # for hg+ssh urls
                        'pydap.handlers.sql>0.4',
                        'pycds>=0.0.8'],
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
