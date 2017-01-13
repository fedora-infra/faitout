#!/bin/bash
# Remove any remnants of apache if it didn't shut down properly
rm -f /var/run/httpd/httpd.pid

# Allow connection from the outside world
echo "host    all             all             0.0.0.0/0               md5" >> /var/lib/pgsql/data/pg_hba.conf
echo "host    all             all             ::1/128                 md5" >> /var/lib/pgsql/data/pg_hba.conf

# Start postgresql before we create the DB
su - postgres -c 'pg_ctl -w -D /var/lib/pgsql/data -l /var/log/psql.log start'

# This if statement should only run on the first time the container is spun up
if [ ! -f /.db_created ]; then

    IP=$(ifconfig | grep "inet "| awk '{print $2}' |grep -v '127.0.0.1')
    echo "DB_HOST = '$IP'" >> /etc/faitout/faitout.cfg

    echo "SECRET_KEY = '$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 24 | head -n 1)'" >> /etc/faitout/faitout.cfg

    FAITOUT_CONFIG=/etc/faitout/faitout.cfg python /srv/faitout/createdb.py
    touch /.db_created
fi

# Start apache and let it speak to us
exec /usr/sbin/httpd -D FOREGROUND
