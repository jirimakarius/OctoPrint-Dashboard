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

  pip install git+https://github.com/meadowfrey/OctoPrint-Dashboard.git --process-dependency-links
  # or
  pip install octoprint_dashboard --process-dependency-links

Set environment, flask runs application by **FLASK_APP** environment variable

.. code:: bash

  export FLASK_APP=octoprint_dashboard

Get OAuth client and secret key from `here <https://auth.fit.cvut.cz/manager/index.xhtml>`_.
Create new project and app of type **Web application**, with redirect uri of your host name or IP.

Configure application:

.. code:: bash

  python -m flask config

* Password for token encryption - is only hash for token, you don't have to remember it
* Client refresh - seconds between data refresh for user
* Server refresh - seconds between data refresh on server side
* Client ID - Client ID from given by OAuth server
* Client secret - given by OAuth server
* Redirect URI - same as given to OAuth server, it has to equal yu hostname

Make yourself superadmin

.. code:: bash

  python -m flask add_superadmin [yourusername]


Run server

.. code:: bash

  python -m flask run --host=0.0.0.0 [--port=]
