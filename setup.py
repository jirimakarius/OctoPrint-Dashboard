from setuptools import setup, find_packages

setup(
    name='octoprint_dashboard',
    version='0.1',
    description='Runs server application for controlling multiple 3D printers',
    author='Jiří Makarius',
    packages=['octoprint_dashboard'],
    include_package_data=True,
    zip_safe=False,
    url='',
    install_requires=[
        'flask', 'requests', 'pyjwt', 'flask-sqlalchemy', 'flask-restful', 'apscheduler', 'octoclient', 'flask-cors'
    ],
    dependency_links=['https://github.com/hroncok/octoclient/tarball/master#egg=octoclient-0.1.dev1']
)