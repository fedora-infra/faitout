#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
faitoutcron - The cron job used to clean the database from old connection that
              have exceeded their time limit.

You may set it up as:
    */5 * * * * root FAITOUT_CONFIG=/etc/faitout/faitout.cfg python /usr/bin/faitoutcron.py


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



__requires__ = ['SQLAlchemy >= 0.7', 'jinja2 >= 2.4']
import pkg_resources
import os

from datetime import datetime
from datetime import timedelta

from faitout import APP, SESSION, ADMIN_ENGINE, faitoutlib

def run_cron():
    """ Runs the cleaning cron job.

    This jobs retrieves from the configuration file the interval at which it is
    ran. It then retrieves a list of all connections which are older than this
    interval and simply deletes those connections.

    """
    interval = APP.config['CRON_FREQUENCY']
    limit = datetime.utcnow() - timedelta(minutes=int(interval))

    connections = faitoutlib.model.Connection.older_than(SESSION, limit)

    for connection in connections:
        print connection
        try:
            output = faitoutlib.drop_connection(
                SESSION,
                ADMIN_ENGINE,
                connection.connection_ip,
                connection.connection_db_name,
            )
        except faitoutlib.FaitoutException as err:
            print 'Error while deleting %s' % connection.connection_db_name
            print >> sys.stderr, err


if __name__ == '__main__':
    run_cron()
