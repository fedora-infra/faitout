FROM fedora:25
ENV FAITOUT_CONFIG /etc/faitout/config.py
RUN dnf install -y --setopt=tsflags=nodocs \
        python-flask \
        python-sqlalchemy \
        python-psycopg2 \
        fedmsg \
        httpd \
        mod_wsgi \
        postgresql-server \
        findutils \
        net-tools && \
    dnf autoremove -y && \
    dnf clean all -y --setopt=tsflags=nodocs

RUN touch /var/log/psql.log && \
    chown postgres:postgres /var/log/psql.log && \
    mkdir /etc/faitout/

USER postgres
COPY ./docker .
RUN export PGDATA=/var/lib/pgsql/data && \
    pg_ctl -D /var/lib/pgsql/data initdb && \
    pg_ctl -w -D /var/lib/pgsql/data -l /var/log/psql.log start && \
    pg_ctl status && \
    psql < ./setup_db.sql

COPY ./ /srv/faitout
WORKDIR /srv/faitout/

USER root
RUN rm -f /etc/httpd/conf.d/welcome.conf && \
    echo "listen_addresses = '*'" >> /var/lib/pgsql/data/postgresql.conf && \
    cp /srv/faitout/docker/apache.conf /etc/httpd/conf.d/faitout.conf && \
    cp /srv/faitout/docker/faitout.cfg /etc/faitout/faitout.cfg && \
    chown -R apache:apache /srv/faitout && \
    chmod +x /srv/faitout/docker/run.sh

EXPOSE 80
EXPOSE 5432
ENTRYPOINT /srv/faitout/docker/run.sh
