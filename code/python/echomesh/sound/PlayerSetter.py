from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.sound import Util
from echomesh.expression import Expression
from echomesh.util import Log

LOGGER = Log.logger(__name__)

INF = float('inf')

def set_player(self, element,
               level=1, pan=0, loops=1, begin=0, end=INF, length=INF, **kwds):
  self._element = element
  self._file = kwds.pop('file')
  self._filename = Util.DEFAULT_AUDIO_DIRECTORY.expand(self._file)
  if kwds:
    LOGGER.error('Unused keywords %s', kwds)
  self._passthrough = (level == 1 and pan == 0)

  self._length = length
  self._level = Expression.expression(level, element)
  self._pan = Expression.expression(pan, element)
  self._loops = loops
  self._begin = begin
  self._end = end

