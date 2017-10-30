===================
OctoPrint Dashboard
===================
This application serves as web server for controlling multiple printers running `OctoPrint <http://octoprint.org/>`_,
this application uses Flask framework.

`GitHub <https://github.com/meadowfrey/OctoPrint-Dashboard>`_

Instalation
-----------
Be sure to have `virtualenv` installed

.. code:: bash

  virtualenv octoprint_dashboard
  . octoprint_dashboard/bin/activate

Now you should be in virtual enviroment, you should see `(octoprint-dashboard)` at start of command line

.. code:: bash

  pip install octoprint_dashboard

Set environment, flask runs application by **FLASK_APP** environment variable

.. code:: bash

  export FLASK_APP=octoprint_dashboard

  export FLASK_DB=absolute_path_to_db_files      (file will be created)

If you choose ČVUT OAuth2, get OAuth client and secret key from `here <https://auth.fit.cvut.cz/manager/index.xhtml>`_.
Create new project and app of type **Web application**, with redirect uri of your host name or IP.

Run server

.. code:: bash

  python -m flask run --host=0.0.0.0 [--port=]
