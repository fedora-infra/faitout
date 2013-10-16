faitout
=======

:Author: Aurélien Bompard <abompard@fedoraproject.org>
:Author: Pierre-Yves Chibon <pingou@pingoured.fr>


faitout is a Free and Open-Source alternative to http://www.postgression.com/
This is flask application generating PostgreSQL databases on the fly
and for a limited time, allowing people to test their code against
an actual PostgreSQL database.


Get this project:
-----------------
Source:  https://github.com/fedora-infra/faitout

Documentation: http://faitout.rtfd.org

Dependencies:
-------------
* `python http://www.python.org`_
* `python-flask http://flask.pocoo.org/`_
* `python-psycopg2 http://www.initd.org/psycopg/`_


Running a development instance:
-------------------------------

Clone the source::

 git clone https://github.com/fedora-infra/faitout.git


Create the database scheme::

 python createdb.py


Run the server::

 sh runserver

You should be able to access the server at http://localhost:5000


Testing:
--------

This project contains unit-tests allowing you to check if your server
has all the dependencies correctly set.

To run them::

 ./runtests.sh

.. note:: To stop the test at the first error or failure you can try:

   ::

    ./runtests.sh -x


License:
--------

This project is licensed GPLv3+.
