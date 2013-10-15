#!/usr/bin/python

## These two lines are needed to run on EL6
__requires__ = ['SQLAlchemy >= 0.7', 'jinja2 >= 2.4']
import pkg_resources

from faitout import APP
from faitout.faitoutlib import model

path_alembic = None
if 'PATH_ALEMBIC_INI' in APP.config \
        and APP.config['PATH_ALEMBIC_INI']:
    path_alembic = APP.config['PATH_ALEMBIC_INI']
model.create_tables(APP.config['DB_URL'], path_alembic, True)
