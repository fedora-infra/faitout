#-*- coding: utf-8 -*-

"""
faitoutlib - the backend library performing the actual work of this project.

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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class FaitoutException(Exception):
    """ Top level exceptions for all the customs exception of Faitout.
    """
    pass


class TooManyConnection(FaitoutException):
    """ Exception thrown when the user has requested to many database
    connection within a certain time frame.
    """
    pass


def create_session(db_url, debug=False, pool_recycle=3600):
    """ Create the Session object to use to query the database.

    :arg db_url: URL used to connect to the database. The URL contains
    information with regards to the database engine, the host to connect
    to, the user and password and the database name.
      ie: <engine>://<user>:<password>@<host>/<dbname>
    :arg debug: a boolean specifying wether we should have the verbose
        output of sqlalchemy or not.
    :return a Session that can be used to query the database.
    """
    engine = create_engine(db_url, echo=debug, pool_recycle=pool_recycle)
    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession


def get_new_connection(session, remote_ip, outformat='text'):
    """ Create a new connection to the database for the specified IP
    address.

    In case the IP address provided is not part of the whitelist and has
    required more than 3 connection over the last X minutes, the method
    will throw a TooManyConnection exception.

    A FaitoutException is thrown if something went wrong at the database
    level.

    :arg session: the session with which to connect to the database.
    :arg remote_ip: the IP address of the user that requested a new
        connection.
    :kwarg outformat: specify the return format of the connection
        information. At the moment 'text' and 'json' are supported, 'text'
        being the default.
    :raise TooManyConnection: if the user requested too many connection too
        quickly.
    :raise FaitoutException: generic exception raised in case of problem.
    :return: a string of the URL to connect to the database if outformat
        is 'text', a dictionnary of the same information if outformat is
        'json'.

    """

    if outformat == 'json':
        return {
            "dbname": "dbname",
            "username": "username",
            "password": "password",
            "port": 123,
            "host": "host"
        }
    else:
        return 'postgres://user:password@host/db'
