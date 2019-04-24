import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__),"README.md"),"r") as readme_file:
  README            = readme_file.read()

setup(
  name              = "channels-websocket-utils",
  version           = "0.1",
  packages          = find_packages(),
  include_package_data = True,
  liscense          = "MIT",
  description       = "Django Channels App for managing websocket connections both in python and JS land ",
  long_description  = README,
  url               = "https://github.com/David-Jianguang-Ran/channels-websocket-utils",
  author            = "David Ran",
  author_email      = "jianguang.ran@gmail.com",
  classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: ECMA Script 2015',
    ],
)
