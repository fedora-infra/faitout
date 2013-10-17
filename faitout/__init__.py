#-*- coding: utf-8 -*-

"""
faitout - a flask application generating PostgreSQL databases on the fly
          and for a limited time allowing people to test their code against
          an actual PostgreSQL database.

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

## These two lines are needed to run on EL6
__requires__ = ['SQLAlchemy >= 0.7', 'jinja2 >= 2.4']
import pkg_resources

__version__ = '0.0.1'

import json
import os
import sys

import flask
import faitoutlib


# Create the application.
APP = flask.Flask(__name__)
APP.config.from_object('faitout.default_config')

if 'FAITOUT_CONFIG' in os.environ:
    APP.config.from_envvar('FAITOUT_CONFIG')

SESSION = faitoutlib.create_session(APP.config['DB_URL'])
ADMIN_ENGINE = faitoutlib.get_engine(APP.config['ADMIN_DB_URL'])


def is_ip_allowed(remote_ip):
    """ Returns wether a provided IP is allowed to ask for a new connections or
    not. This relies on the IP_ONLY and the IP_BLOCKED fields set in the
    configuration.

    :arg remote_ip: the IP address of the user asking for a new connection.

    """
    if APP.config['IP_BLOCKED'] and remote_ip in APP.config['IP_BLOCKED']:
        return False
    if APP.config['IP_ONLY']:
        if remote_ip in APP.config['IP_ONLY']:
            return True
        else:
            return False
    return True


## Flask application
@APP.route('/')
def index():
    """ Displays the index page which contains the basic information.
    """
    return flask.render_template('index.html')


@APP.route('/new/')
@APP.route('/new')
def token():
    """ Returns the URL to the database with user and password information.
    """
    status = 200
    outformat = 'text'

    if 'Accept' in flask.request.headers:
        if flask.request.headers['Accept'] == 'application/json':
            outformat = 'json'
    elif 'Content-Type' in flask.request.headers:
        if flask.request.headers['Content-Type'] == 'application/json':
            outformat = 'json'

    if outformat == 'json':
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'

    if not is_ip_allowed(flask.request.remote_addr):
        return flask.Response(
            response=json.dump(
                    {'ERROR': 'NotAuthorizedException', 'description', 'IP '
                    'address %s is not authorized to request new connections.' %
                    flask.request.remote_addr}
                ),
            status=403,
            mimetype='application/json'
        )

    try:
        output = faitoutlib.get_new_connection(
            SESSION,
            ADMIN_ENGINE,
            remote_ip=flask.request.remote_addr,
            host=APP.config['DB_HOST'],
            port=APP.config['DB_PORT'],
            max_con=APP.config['MAX_CONNECTIONS'],
            outformat=outformat,
            unlimited=flask.request.remote_addr in APP.config['IP_UNLIMITED']
        )
    except faitoutlib.TooManyConnectionException as err:
        output = {
            'ERROR': err.__class__.__name__,
            'description': err.message
        }
        status = 400
        mimetype = 'application/json'
    except faitoutlib.FaitoutException as err:
        print >> sys.stderr, err
        output = {
            'ERROR': err.__class__.__name__,
            'description': err.message
        }
        status = 500
        mimetype = 'application/json'

    if outformat == 'json' or mimetype == 'application/json':
        output = json.dumps(output)

    return flask.Response(
        response=output,
        status=status,
        mimetype=mimetype
    )


@APP.route('/clean/<db_name>/')
@APP.route('/clean/<db_name>')
def clean_database(db_name):
    """ Clean the provided database.
    """
    status = 200
    outformat = 'text'
    mimetype = 'text/plain'

    try:
        output = faitoutlib.clean_connection(
            SESSION,
            ADMIN_ENGINE,
            flask.request.remote_addr,
            db_name
        )
    except faitoutlib.NoDatabaseException as err:
        output = {
            'ERROR': err.__class__.__name__,
            'description': err.message
        }
        status = 404
        mimetype = 'application/json'
    except faitoutlib.WrongOriginException as err:
        output = {
            'ERROR': err.__class__.__name__,
            'description': err.message
        }
        status = 403
        mimetype = 'application/json'
    except faitoutlib.FaitoutException as err:
        print >> sys.stderr, err
        output = {
            'ERROR': err.__class__.__name__,
            'description': err.message
        }
        status = 500
        mimetype = 'application/json'

    if outformat == 'json' or mimetype == 'application/json':
        output = json.dumps(output)

    return flask.Response(
        response=output,
        status=status,
        mimetype=mimetype
    )
