from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import Config
from echomesh.base import Path
from echomesh.expression import Expression

CLIENT_NAME = 'echomesh-client'
COMMAND = os.path.join(Path.BINARY_PATH, CLIENT_NAME)
KILLALL = '/usr/bin/killall'

def make_command():
  parts = []
  config = Config.get('network', 'client')

  parts.append(config['binary'] or COMMAND)
  parts.append(config['host_name'])
  parts.append(str(config['port']))
  timeout = Expression.convert(Config.get('network', 'timeout'))
  parts.append(str(timeout))
  parts.append(str(config['buffer_size']))
  parts.append(str(config['debug']))

  return parts

def make_kill_command():
  return [KILLALL, CLIENT_NAME]
