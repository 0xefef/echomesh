from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Config
from echomesh.base import GetPrefix
from echomesh.base import MergeConfig
from echomesh.base import Yaml
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def _set(_, *values):
  if values:
    assignment = GetPrefix.leafs(Config.assign(values))
    for address, value in six.iteritems(assignment):
      LOGGER.info('Set %s=%s', '.'.join(address), value)
  elif MergeConfig.LOCAL_CHANGES:
    LOGGER.info(Yaml.encode_one(MergeConfig.LOCAL_CHANGES))
  else:
    LOGGER.info('You have made no changes.')

FUNCTION = _set

HELP = """
  Sets one or more configuration variables.  These changes are only present in
  memory and will be lost when the program ends - you need to use config save
  to make them permanent.

Examples:
  set speed=50%
  set speed=10% light.period=40ms
"""

