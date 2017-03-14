from setuptools import setup

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
        'Flask', 'requests', 'jwt', 'Flask-SQLAlchemy'
    ]
)