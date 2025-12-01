"""
Config package init. This file ensures a pure-Python MySQL driver (PyMySQL)
is available as a drop-in replacement for MySQLdb if installed.
This keeps the project portable for developers who cannot build the native
`mysqlclient` C extension on systems like Raspberry Pi.
"""

try:
	import pymysql
	pymysql.install_as_MySQLdb()
except Exception:
	# If PyMySQL is not installed, fallback to system-provided mysqlclient.
	pass
