#-*- coding: utf-8 -*-

"""
faitoutlib - Unit-tests librairy.

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

import unittest
#import shutil
import sys
import os

from datetime import datetime
from datetime import timedelta

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy.orm import scoped_session

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from faitout.faitoutlib import model

DB_PATH = 'sqlite:///:memory:'

try:
    import requests
    req = requests.get('http://209.132.184.152/faitout/new')
    if req.status_code == 200:
        DB_PATH = req.text
    else:
        print req.text
except:
    pass

print "using: %s" % DB_PATH


class Modeltests(unittest.TestCase):
    """ Model tests. """

    def __init__(self, method_name='runTest'):
        """ Constructor. """
        unittest.TestCase.__init__(self, method_name)
        self.session = None

    # pylint: disable=C0103
    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        self.session = model.create_tables(DB_PATH, debug=False)

    # pylint: disable=C0103
    def tearDown(self):
        """ Remove the test.db database if there is one. """
        if os.path.exists(DB_PATH):
            os.unlink(DB_PATH)

        self.session.rollback()

        ## Empty the database if it's not a sqlite
        if self.session.bind.driver != 'pysqlite':
            self.session.execute('DROP TABLE "connections" CASCADE;')
            self.session.commit()


def create_connections(session):
    """ Create some connections for testing. """
    connection = model.Connection(
        user='user1',
        mdp='pass1',
        db='db1',
        ip='127.0.0.1',
    )
    session.add(connection)

    connection = model.Connection(
        user='user2',
        mdp='pass2',
        db='db2',
        ip='127.0.0.1',
    )
    connection.creation_date = datetime.utcnow() - timedelta(minutes=15)
    session.add(connection)

    connection = model.Connection(
        user='user3',
        mdp='pass3',
        db='db3',
        ip='127.0.0.1',
    )
    connection.creation_date = datetime.utcnow() - timedelta(minutes=45)
    session.add(connection)

    connection = model.Connection(
        user='user4',
        mdp='pass4',
        db='db4',
        ip='127.0.0.2',
    )
    connection.creation_date = datetime.utcnow() - timedelta(minutes=45)
    connection.connection_active = False
    session.add(connection)

    session.commit()


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(Modeltests)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
