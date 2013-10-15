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

import os


# url to the database server:
DB_URL = 'sqlite:////var/tmp/faitout_dev.sqlite'


# The cron job can be set with any frequency but fedocal_cron
CRON_FREQUENCY = 30

# URL at which the application is made available
URL = 'http://127.0.0.1:5000'
