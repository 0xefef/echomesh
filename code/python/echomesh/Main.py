from __future__ import absolute_import, division, print_function, unicode_literals

USE_DIGITS_FOR_PROGRESS_BAR = False
COUNT = 0

def _main():
  import sys

  times = []

  def p(msg=''):
    """Print progress messages while echomesh loads."""
    print(msg, end='\n' if msg else '')
    global COUNT
    dot = str(COUNT % 10) if USE_DIGITS_FOR_PROGRESS_BAR else '.'
    print(dot, end='')
    COUNT += 1

    sys.stdout.flush()

    import time
    times.append(time.time())

  p('Loading echomesh ')

  from echomesh.base import Version
  if Version.TOO_NEW:
    print(Version.ERROR)

  from echomesh.base import Path
  if not Path.PROJECT_PATH:
    return
  p()


  Path.fix_home_directory_environment_variable()
  p()

  Path.fix_sys_path()
  p()

  from echomesh.base import Config
  p()

  Config.reconfigure(sys.argv[1:])
  p()

  if Config.get('autostart') and not Config.get('permission', 'autostart'):
    print()
    from echomesh.util import Log
    Log.logger(__name__).info('No permission to autostart')
    return
  p()

  from echomesh.base import Quit
  p()

  Quit.register_atexit(Config.save)
  p()

  from echomesh import Instance
  print()

  if Config.get('diagnostics', 'startup_times'):
    print()
    for i in range(len(times) - 1):
      print(i, ':', int(1000 * (times[i + 1] - times[i])))
    print()

  Instance.main()

def main():
  try:
    _main()
  except:
    import traceback
    print(traceback.format_exc())

