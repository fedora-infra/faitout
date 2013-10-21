#-*- coding: utf-8 -*-

"""
faitoutlib - Tests the model.

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
import sys
import os

import mock

from datetime import datetime
from datetime import timedelta

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from faitout import faitoutlib
from faitout.faitoutlib import model
from tests import Modeltests, create_connections


class FaitoutLibtests(Modeltests):
    """ Faitoutlib tests. """

    def test_get_stats(self):
        """ Test the get_stats method of faitoutlib. """
        create_connections(self.session)

        output = faitoutlib.get_stats(self.session)
        self.assertEqual(
            output,
            {
                'total_connections': 4,
                'active_connections': 3,
                'unique_ip': 2,
            }
        )

    def test_get_new_connection(self):
        """ Test the get_new_connection method of faitoutlib. """
        create_connections(self.session)

        faitoutlib.create_database = mock.MagicMock()

        self.assertEqual(model.Connection.by_ip(
            self.session, '127.0.0.1', cnt=True), 3)
        # Fails as 127.0.0.1 already has 3 active connections
        self.assertRaises(
            faitoutlib.TooManyConnectionException,
            faitoutlib.get_new_connection,
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.1',
            host='localhost',
            port=5432,
            max_con=3,
            outformat='text',
            unlimited=False
            )
        self.assertEqual(model.Connection.by_ip(
            self.session, '127.0.0.1', cnt=True), 3)

        self.assertEqual(model.Connection.by_ip(
            self.session, '127.0.0.2', cnt=True), 0)
        connection = faitoutlib.get_new_connection(
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.2',
            host='localhost',
            port=5432,
            max_con=3,
            outformat='text',
            unlimited=False
            )
        self.assertTrue(connection.startswith('postgresql://'))
        self.assertTrue('localhost:5432' in connection)
        self.assertEqual(model.Connection.by_ip(
            self.session, '127.0.0.2', cnt=True), 1)

        self.assertEqual(model.Connection.by_ip(
            self.session, '127.0.0.2', cnt=True), 1)
        connection = faitoutlib.get_new_connection(
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.2',
            host='localhost',
            port=5432,
            max_con=3,
            outformat='json',
            unlimited=False
            )
        self.assertEqual(
            sorted(connection.keys()),
            ['dbname', 'host', 'password', 'port', 'username'])
        self.assertEqual(connection['host'], 'localhost')
        self.assertEqual(connection['port'], 5432)
        self.assertEqual(model.Connection.by_ip(
            self.session, '127.0.0.2', cnt=True), 2)

        self.assertEqual(model.Connection.by_ip(
            self.session, '127.0.0.1', cnt=True), 3)
        connection = faitoutlib.get_new_connection(
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.1',
            host='localhost',
            port=5432,
            max_con=3,
            outformat='json',
            unlimited=True
            )
        self.assertEqual(model.Connection.by_ip(
            self.session, '127.0.0.1', cnt=True), 4)
        self.assertEqual(
            sorted(connection.keys()),
            ['dbname', 'host', 'password', 'port', 'username'])
        self.assertEqual(connection['host'], 'localhost')
        self.assertEqual(connection['port'], 5432)

    def test_clean_connection(self):
        """ Test the clean_connection method of faitoutlib. """
        create_connections(self.session)

        faitoutlib.clean_database = mock.MagicMock()

        # Fails as dbTest does not exists
        self.assertRaises(
            faitoutlib.NoDatabaseException,
            faitoutlib.clean_connection,
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.1',
            db_name='dbTest'
            )

        # Fails as db4 is not active
        self.assertRaises(
            faitoutlib.NoDatabaseException,
            faitoutlib.clean_connection,
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.2',
            db_name='db4'
            )

        # Fails as db1 was requested by 127.0.0.1
        self.assertRaises(
            faitoutlib.WrongOriginException,
            faitoutlib.clean_connection,
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.2',
            db_name='db1'
            )

        output = faitoutlib.clean_connection(
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.1',
            db_name='db1'
            )
        self.assertEqual(output, 'Database db1 has been cleaned')

    def test_drop_connection(self):
        """ Test the drop_connection method of faitoutlib. """
        create_connections(self.session)

        faitoutlib.drop_database = mock.MagicMock()

        # Fails as dbTest does not exists
        self.assertRaises(
            faitoutlib.NoDatabaseException,
            faitoutlib.drop_connection,
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.1',
            db_name='dbTest'
            )

        # Fails as db4 is not active
        self.assertRaises(
            faitoutlib.NoDatabaseException,
            faitoutlib.drop_connection,
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.2',
            db_name='db4'
            )

        # Fails as db1 was requested by 127.0.0.1
        self.assertRaises(
            faitoutlib.WrongOriginException,
            faitoutlib.drop_connection,
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.2',
            db_name='db1'
            )

        output = faitoutlib.drop_connection(
            self.session,
            admin_engine=None,
            remote_ip='127.0.0.1',
            db_name='db1'
            )
        self.assertEqual(output, 'Database db1 has been dropped')


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(FaitoutLibtests)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
