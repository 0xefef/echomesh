from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing

from command import Processor
from command import Router
from config import Config
from graphics import Display
from graphics import Tasks
from graphics import ImagePath
from network import Clients
from network import Discovery
from sound import Microphone

from util import Log
from util import Openable

IMAGE = '/development/echomesh/data/ball.gif'

LOGGER = Log.logger(__name__)

class Echomesh(Openable.Openable):
  def __init__(self):
    Openable.Openable.__init__(self)
    self.config = Config.CONFIG
    self.clients = Clients.Clients(self)
    callbacks = Router.router(self, self.clients)
    self.discovery = Discovery.Discovery(self.config, callbacks)
    self.process = Processor.process
    self.display = Display.Display(self.config)
    p = ImagePath.ImagePath(IMAGE, 45, 10.0, self.display)
    self.display.add_sprite(p)
    self.mic_thread = Microphone.run_mic_levels_thread(print, self.config)

  def send(self, data):
    self.discovery.send(data)

  def run(self):
    with closing(self):
      self.discovery.start()
      self.clients.start()
      self.display.start()
      self.mic_thread.start()

      if self.config.get('control_program', False):
        while self.is_open:
          if not self.process(raw_input('echomesh: ').strip(), self):
            self.close()

      else:
        self._join()

  def close(self):
    if self.is_open:
      Openable.Openable.close(self)
      LOGGER.info('echomesh closing')
      self.discovery.close()
      self.mic_thread.close()
      self.display.close()
      self._join()

  def _join(self):
    self.display.join()
    self.close()
    self.discovery.join()
    self.mic_thread.join()

if __name__ == '__main__':
  Echomesh().run()
