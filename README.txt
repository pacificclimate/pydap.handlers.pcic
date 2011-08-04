This is a custom python package intended to inherit from pydap.handlers.sql.
The SQL handler for pydap requires a static file to configure each dataset.  Since PCIC wants to
server data out of our database, it is far more preferable to dynamically create
the dataset config files from the database.
This package is intended to do this.  It simply generates a config file and instantiates the SQL
handler using the dynamically generated file.
