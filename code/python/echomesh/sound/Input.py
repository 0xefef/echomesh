from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

MAX_INPUT_DEVICES = 6

# TODO: a better way to identify that stream.
def get_pyaudio_stream(rate, use_default, sample_bytes):
  import pyaudio

  pyaud = pyaudio.PyAudio()
  FORMAT_NAMES = {1: pyaudio.paInt8, 2: pyaudio.paInt16, 3:
                  pyaudio.paInt24, 4: pyaudio.paInt32}
  format = FORMAT_NAMES.get(sample_bytes, 0)
  if not format:
    LOGGER.error("Didn't understand sample_bytes=%s", sample_bytes)
    format = FORMAT_NAMES[1]

  def _make_stream(i):
    stream = pyaud.open(format=format, channels=1, rate=rate,
                        input_device_index=i, input=True)
    LOGGER.info('Opened pyaudio stream %d', i)
    return stream

  if use_default:
    index = pyaud.get_default_input_device_info()['index']
    return _make_stream(index)
  else:
    for i in range(MAX_INPUT_DEVICES):
      try:
        stream = _make_stream(i)
        return stream
      except:
        pass

  LOGGER.error("Couldn't create pyaudio input stream %d", rate)

def get_mic_level(data, length=-1, dtype=None):
  import analyse
  import numpy

  if dtype is None:
    dtype = numpy.int16

  samps = numpy.fromstring(data, dtype=dtype, count=length)
  return analyse.loudness(samps)