import os
import subprocess
from os import path
from glob import glob
from distutils.core import setup
from setuptools import find_packages

#-----------------------------------------------------------------------------
# Project
#-----------------------------------------------------------------------------

project = "airbus"
summary = "Define inheritable methodologies"
author = "Ryan Morshead"
email = "ryan.morshead@gmail.com"

#-----------------------------------------------------------------------------
# Details
#-----------------------------------------------------------------------------

username = "rmorshea"
url = "https://github.com/%s/%s" % (username, project)
keywords = ["async", "workers"]
platforms = "Linux, Mac OS X, Windows"
license = "MIT"

#-----------------------------------------------------------------------------
# Packages
#-----------------------------------------------------------------------------

packages = find_packages(project)

#-----------------------------------------------------------------------------
# Base Paths
#-----------------------------------------------------------------------------

here = path.abspath(path.dirname(__file__))
root = path.join(here, name)
scripts = path.join(here, "scripts", "*")

#-----------------------------------------------------------------------------
# Info From Project Files
#-----------------------------------------------------------------------------

version_namespace = {}
with open(path.join(root, 'version.py'), "r") as f:
    exec(f.read(), {}, version_namespace)

with open(path.join(here, "README.rst"), "r") as f:
    description = f.read()

#-----------------------------------------------------------------------------
# Finalize Arguments
#-----------------------------------------------------------------------------

setup_arguments = dict(name=project, packages=packages, description=summary,
    long_description=description, version=version_namespace["__version__"],
    author_email=email, keywords=keywords, license=license, author=author,
    platforms=platforms, url=url, scripts=glob(scripts),
)

#-----------------------------------------------------------------------------
# Requirements Installation Command
#-----------------------------------------------------------------------------

install_requirements = "pip install -r %s" % path.join(here, "requirements.txt")

#-----------------------------------------------------------------------------
# Setup
#-----------------------------------------------------------------------------

if __name__ == "__main__":
    subprocess.run(install_requirements.split())
    setup(**setup_arguments)
