'''
    TODO: DOC
'''

from gi.repository import Gtk
import matplotlib.pyplot as plot

class Window(object):
    __gladefile_window = 'meteorax/gui/glade/output.glade'

    def __init__(self, titulo, draw_callback):
        super(Window, self).__init__()

        builder = Gtk.Builder()
        builder.add_from_file(self.__gladefile_window)

        self.__box_output = builder.get_object('box-output')

        self.window = builder.get_object('window_output')
        self.window.set_title(titulo)
        self.window.connect('destroy', self.__destroy)

        self.__draw_callback = draw_callback

    def mostrar(self):
        self.__draw_callback()
        self.window.show_all()
        Gtk.main()

    def __destroy(self, widget=None, data=None):
        # pylint: disable=unused-argument
        plot.gcf().clear()
        Gtk.main_quit()

    def get_box_output(self):
        return self.__box_output

    def get_window(self):
        return self.window
