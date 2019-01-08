from hornstone.alchemy import make_sqlite_session

from .database import Base

dbfilename = 'mcjudicial.sqlite'
Session = make_sqlite_session(dbfilename, create_all=True, baseclass=Base)
