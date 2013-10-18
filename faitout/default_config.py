#-*- coding: utf-8 -*-

"""
default_config - the default configuration allowing to run this project
                 quickly and easily from the sources.

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

# url to the database server:
DB_URL = 'sqlite:////var/tmp/faitout_dev.sqlite'

# url to the admin database:
ADMIN_DB_URL = 'sqlite:////var/tmp/faitout_dev_admin.sqlite'

# Default port of a postgresql server
DB_PORT = 5432

# Host of the postgresql server to return to in the db url
DB_HOST = '127.0.0.1'

# The cron job can be set with any frequency but faitout_cron
CRON_FREQUENCY = 30

# URL at which the application is made available
URL = 'http://127.0.0.1:5000'

# The maximum number of simultaneous connection allowed at the same time
MAX_CONNECTIONS = 3

# List of IPs allowed to get as many connections as they want
#  This is useful if for example you use faitout in combination with a jenkins
#  instance or some other sort of CI system.
IP_UNLIMITED = ['127.0.0.1']

# List of IPs not allowed to get any connections
IP_BLOCKED = []

# Restrict the use of faitout to those IPs only
#  This is useful either for testing or if you want to restrict your faitout
#  instance to a group of people and not make it world accessible.
IP_ONLY = []

