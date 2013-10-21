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

from datetime import datetime
from datetime import timedelta

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from faitout.faitoutlib import model
from tests import Modeltests, create_connections


class FaitoutModeltests(Modeltests):
    """ Model tests. """

    def test_search(self):
        """ Test the search method of Connection. """
        create_connections(self.session)

        connections = model.Connection.search(self.session, active=True)
        self.assertEqual(len(connections), 3)
        self.assertTrue(connections[0].__repr__().startswith(
            "<Connection('1' ip:'127.0.0.1'"))
        self.assertTrue(connections[1].__repr__().startswith(
            "<Connection('2' ip:'127.0.0.1'"))
        self.assertTrue(connections[2].__repr__().startswith(
            "<Connection('3' ip:'127.0.0.1'"))

        connections = model.Connection.search(self.session, active=False)
        self.assertEqual(len(connections), 1)
        self.assertTrue(connections[0].__repr__().startswith(
            "<Connection('4' ip:'127.0.0.2'"))

        connections = model.Connection.search(
            self.session, active=True, cnt=True)
        self.assertEqual(connections, 3)

    def test_cnt_unique_ip(self):
        """ Test the cnt_unique_ip method of Connection. """
        create_connections(self.session)

        unique_ip = model.Connection.cnt_unique_ip(self.session)
        self.assertEqual(unique_ip, 2)

    def test_by_ip(self):
        """ Test the by_ip method of Connection. """
        create_connections(self.session)

        connections = model.Connection.by_ip(self.session, '127.0.0.2')
        self.assertEqual(len(connections), 0)
        self.assertEqual(connections, [])

        connections = model.Connection.by_ip(self.session, '127.0.0.1')
        self.assertEqual(len(connections), 3)
        self.assertTrue(connections[0].__repr__().startswith(
            "<Connection('1' ip:'127.0.0.1'"))
        self.assertTrue(connections[1].__repr__().startswith(
            "<Connection('2' ip:'127.0.0.1'"))
        self.assertTrue(connections[2].__repr__().startswith(
            "<Connection('3' ip:'127.0.0.1'"))

        connections = model.Connection.by_ip(
            self.session, '127.0.0.1', cnt=True)
        self.assertEqual(connections, 3)

    def test_by_db_name(self):
        """ Test the by_db_name method of Connection. """
        create_connections(self.session)

        connection = model.Connection.by_db_name(self.session, 'db2')
        self.assertTrue(connection.__repr__().startswith(
            "<Connection('2' ip:'127.0.0.1'"))

    def test_older_than(self):
        """ Test the older_than method of Connection. """
        create_connections(self.session)

        limit = datetime.utcnow() - timedelta(minutes=30)
        connections = model.Connection.older_than(self.session, limit)
        self.assertEqual(len(connections), 1)
        self.assertTrue(connections[0].__repr__().startswith(
            "<Connection('3' ip:'127.0.0.1'"))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(FaitoutModeltests)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
