Using faitout on docker
=======================


.. warning:: The Dockerfile and the files provided here are only meant to be use
             for local development, do not run a production instance of faitout
             in docker using these files without at least changing the passwords
             in ``setup_db.sql`` and ``faitout.cfg``.
             You have been warned :)


Build the docker image
----------------------

In the main folder of the project run:

::

    sudo docker build -t faitout .

Run the resulting image:

::

    sudo docker run -i -t faitout


Retrieve the IP address of the container:

* List all the running image:

::

    sudo docker ps

There retrieve the container ID of the faitout container you have running.

* Retrieve the IP:

::

    sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' <container_id>

Alternatively, if the faitout container was the last container you started you
can run in a single command:

::

    sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(sudo docker ps -q)

``docker ps -q`` will return the container ID of the last container created.


Debug the docker image
----------------------

To gain a shell access to the image to debug your faitout instance, you can
simply do

::

    sudo docker run -i -t --entrypoint="/bin/bash" faitout

And once inside the container, you can try running manuall the default entry
point:

::

    sh /srv/faitout/docker/run.sh


