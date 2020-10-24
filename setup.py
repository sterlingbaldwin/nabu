from setuptools import find_packages, setup
from nabu.version import __version__

setup(
    name="nabu",
    version=__version__,
    author="Sterling Baldwin",
    author_email="sterling16@mac.com",
    description="An interactive fiction reader",
    entry_points={'console_scripts':
                  ['nabu = nabu.__main__:main']},
    packages=['nabu'],
    package_dir={'nabu': 'nabu'},
    package_data={'nabu': ['LICENSE']},
    include_package_data=True)