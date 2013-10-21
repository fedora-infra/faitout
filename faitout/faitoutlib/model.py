# -*- coding: utf-8 -*-

"""
model - an object mapper to a SQL database representation of the data
        stored in this project.

 (c) 2013 - Copyright Red Hat Inc.

 Authors:
 - Pierre-Yves Chibon <pingou@pingoured.fr>

 Distributed under License GPLv3 or later
 You can find a copy of this license on the website
 http://www.gnu.org/licenses/gpl.html

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 MA 02110-1301, USA.
"""

__requires__ = ['SQLAlchemy >= 0.7']
import pkg_resources

from datetime import datetime
from datetime import timedelta

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relation as relationship

BASE = declarative_base()


def create_tables(db_url, alembic_ini=None, debug=False):
    """ Create the tables in the database using the information from the
    url obtained.

    :arg db_url, URL used to connect to the database. The URL contains
        information with regards to the database engine, the host to
        connect to, the user and password and the database name.
          ie: <engine>://<user>:<password>@<host>/<dbname>
    :kwarg alembic_ini, path to the alembic ini file. This is necessary to
        be able to use alembic correctly, but not for the unit-tests.
    :kwarg debug, a boolean specifying wether we should have the verbose
        output of sqlalchemy or not.
    :return a session that can be used to query the database.
    """
    engine = sa.create_engine(db_url, echo=debug)
    BASE.metadata.create_all(engine)

    if alembic_ini is not None:  # pragma: no cover
        # then, load the Alembic configuration and generate the
        # version table, "stamping" it with the most recent rev:
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config(alembic_ini)
        command.stamp(alembic_cfg, "head")

    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession


class Connection(BASE):
    """ Connection table.

    Define the connections made available to users.
    """

    __tablename__ = 'connections'
    connection_id = sa.Column(sa.Integer, primary_key=True)
    connection_user = sa.Column(sa.String(20), nullable=False)
    connection_mdp = sa.Column(sa.String(40), nullable=False)
    connection_db_name = sa.Column(sa.String(15), nullable=False,
                                   unique=True, index=True)
    connection_ip = sa.Column(sa.String(20), nullable=False, index=True)
    connection_active = sa.Column(sa.Boolean, nullable=False, default=True)
    creation_date = sa.Column(sa.DateTime, nullable=False,
                              default=sa.func.current_timestamp())

    def __init__(self, user, mdp, db, ip):
        """ Constructor instanciating the defaults values. """
        self.connection_user = user
        self.connection_mdp = mdp
        self.connection_db_name = db
        self.connection_ip = ip

    def __repr__(self):
        """ Representation of the Calendar object when printed.
        """
        return "<Connection('%s' ip:'%s' date:'%s' db:'%s')>" % (
            self.connection_id, self.connection_ip, self.creation_date,
            self.connection_db_name)

    def save(self, session):
        """ Save the object into the database. """
        session.add(self)

    def delete(self, session):
        """ Remove the object into the database. """
        session.delete(self)

    @classmethod
    def search(cls, session, active=None, cnt=False):
        """ Retrieve all the connections matching the provided criterias.

        :arg session: the session with which to connect to the database.
        :kwarg active: Boolean specifying wether the active connections
            should be active or not. It defaults to None, which will not
            filter the returned connection on their status (thus include
            both active and inactive connections).
        :kwarg cnt: Boolean specifying to return either the list of
            connections or the number of connections matching the criterias.

        """
        query = session.query(cls)

        if active is not None:
            query = query.filter(cls.connection_active == active)

        query = query.order_by(cls.connection_id)

        if cnt:
            return query.count()
        else:
            return query.all()

    @classmethod
    def cnt_unique_ip(cls, session, active=None, cnt=False):
        """ Retrieve the number of unique IP registered in the application.

        :arg session: the session with which to connect to the database.

        """
        query = session.query(sa.func.distinct(cls.connection_ip))

        return query.count()

    @classmethod
    def by_ip(cls, session, ip, cnt=False):
        """ Retrieve all the active Connection associated with the
        specified IP.

        :arg session: the session with which to connect to the database.
        :arg remote_ip: the IP address of the user that requested a new
            connection.
        :kwarg cnt: a boolean to specify wether to return the list of
            connection associated with this IP or just the number of
            entries.

        """
        query = session.query(
            cls
        ).filter(
            cls.connection_ip == ip
        ).filter(
            cls.connection_active == True
        )

        if cnt:
            return query.count()
        else:
            return query.all()

    @classmethod
    def by_db_name(cls, session, db_name):
        """ Retrieve the Connection associated with the specified database
        name.

        :arg session: the session with which to connect to the database.
        :arg db_name: the name of the database to retrieve.

        """
        query = session.query(
            cls
        ).filter(
            cls.connection_db_name == db_name
        )

        return query.one()

    @classmethod
    def older_than(cls, session, limit):
        """ Retrieve all the active Connection that have been created
        before the specified limit.

        :arg session: the session with which to connect to the database.
        :arg limit: a datetime object specifying the datetime limit after
            which the connections are returned.

        """
        return session.query(
            cls
        ).filter(
            cls.creation_date <= limit
        ).filter(
            cls.connection_active == True
        ).all()
