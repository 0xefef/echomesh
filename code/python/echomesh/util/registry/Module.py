from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from echomesh.util.registry.Registry import Registry

EXPORTED_ATTRIBUTES = ()  # 'entry', 'function', 'get_help', 'keys', 'join_keys'

def register(class_path, *modules, **kwds):
  module = sys.modules[class_path]
  registry = Registry(class_path, class_path=class_path, **kwds)

  for sub in modules:
    registry.register(sub, sub.lower())

  for a in EXPORTED_ATTRIBUTES:
    setattr(module, a, getattr(registry, a))

  return registry
