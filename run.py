'''
    TODO: DOC
'''

import locale
import os
import gi
import matplotlib

gi.require_version('Gtk', '3.0')

os.environ['PYART_QUIET'] = '1'

locale.setlocale(locale.LC_ALL, '')

matplotlib.use('Cairo')

from meteorax.gui.main import MainWindow

MainWindow()
