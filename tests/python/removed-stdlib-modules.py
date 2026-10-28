import sys

# ruleid: python313-removed-stdlib-module
import pipes
# ruleid: python313-removed-stdlib-module
import telnetlib as tn
# ruleid: python313-removed-stdlib-module
from cgi import escape
# ruleid: python313-removed-stdlib-module
import audioop
# ruleid: python313-removed-stdlib-module
from lib2to3.pgen2 import token
# ruleid: python313-removed-stdlib-module
import os, xdrlib
# ok: python313-removed-stdlib-module
import shlex
# ok: python313-removed-stdlib-module
import cgitbx

try:
    # ok: python313-removed-stdlib-module
    import audioop
except ImportError:
    import audioop_lts as audioop

try:
    # ok: python313-removed-stdlib-module
    import imghdr
except (ImportError, AttributeError):
    imghdr = None

if sys.version_info < (3, 13):
    # ok: python313-removed-stdlib-module
    import crypt

# ruleid: python312-removed-stdlib-module
import asyncore
# ruleid: python312-removed-stdlib-module
from distutils.core import setup
# ruleid: python312-removed-stdlib-module
import imp
# ok: python312-removed-stdlib-module
import importlib

try:
    # ok: python312-removed-stdlib-module
    from distutils.version import LooseVersion
except ModuleNotFoundError:
    from packaging.version import Version as LooseVersion
