import string
from setuptools import setup

__version__ = (0, 0, 1)

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
    install_requires=['pydap.handlers.sql'],
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
