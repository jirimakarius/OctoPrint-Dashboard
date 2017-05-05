from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='octoprint_dashboard',
    version='0.2.dev1',
    description='Runs server application for controlling multiple 3D printers with OctoPrint',
    long_description=long_description,
    author='Jiří Makarius',
    keywords="octoprint 3Dprint dashboard python flask",
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/meadowfrey/OctoPrint-Dashboard',
    install_requires=[
        'flask', 'requests', 'pyjwt', 'flask-sqlalchemy', 'flask-restful', 'apscheduler', 'octoclient', 'flask-cors', 'zeroconf'
    ],
    dependency_links=['https://github.com/hroncok/octoclient/tarball/master#egg=octoclient-0.1.dev1'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Printing",
        "Topic :: System :: Networking :: Monitoring"
    ]
)
