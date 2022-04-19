'''
    TODO: DOC
'''

import warnings
warnings.filterwarnings("ignore")

from gi.repository import Gtk

from meteorax.gui.resultados.productos import Productos
from meteorax.gui.resultados.radar import Radar as ResultadosRadar
from meteorax.gui.resultados.escaneo import Escaneo as ResultadosEscaneo
from meteorax.gui.util import Util
from meteorax.core.radar import Radar


class MainWindow():
    '''
        TODO: DOC
    '''

    __box_data_escaneo = None
    __box_data_radar = None
    __box_main = None
    __builder = None
    __frame_escaneo = None
    __frame_radar = None
    __frame_productos = None
    __gladefile_box_data = 'meteorax/gui/glade/box_data.glade'
    __gladefile_main = 'meteorax/gui/glade/main.glade'

    def __init__(self):
        super(MainWindow, self).__init__()

        builder = Gtk.Builder()
        builder.add_from_file(self.__gladefile_main)

        Util(builder, self.__gladefile_box_data)

        window = builder.get_object('window_main')
        window.connect('destroy', self.__destroy)

        file_chooser_button = builder.get_object(
            'filechooserbutton_volumen')
        file_chooser_button.connect('file-set', self.__archivo_seleccionado)

        self.__builder = builder
        self.__set_items()

        self.__frame_radar.hide()
        self.__frame_escaneo.hide()
        self.__frame_productos.hide()

        window.show()
        Gtk.main()

    def __set_items(self):
        get_object = self.__builder.get_object
        self.__box_data_radar = get_object('box-data-radar')
        self.__box_data_escaneo = get_object('box-data-escaneo')
        self.__box_data_productos = get_object('box-data-productos')
        self.__frame_radar = get_object('frame-radar')
        self.__frame_escaneo = get_object('frame-escaneo')
        self.__frame_productos = get_object('frame-productos')
        self.__box_main = get_object('box-main')

    def __archivo_seleccionado(self, file_chooser):
        '''
            TODO: DOC
        '''
        archivo = file_chooser.get_filename()
        self.selecionar_archivo(archivo)

    def selecionar_archivo(self, archivo=''):
        '''
            TODO: DOC
        '''
        Radar().leer(archivo)
        self.mostrar_resultados()

    def mostrar_resultados(self):
        '''
            TODO: DOC
        '''
        self.__limpiar()

        ResultadosRadar(self.__box_data_radar, self.__frame_radar).mostrar()
        ResultadosEscaneo(self.__box_data_escaneo, self.__frame_escaneo).mostrar()
        Productos(self.__box_data_productos, self.__frame_productos).mostrar()

    def __limpiar(self):
        def borrar(elemento):
            '''
                TODO: DOC
            '''
            elemento.get_parent().remove(elemento)

        self.__box_data_radar.foreach(borrar)
        self.__box_data_escaneo.foreach(borrar)
        self.__box_data_productos.foreach(borrar)

    def __destroy(self, widget=None, data=None):
        # pylint: disable=unused-argument
        Gtk.main_quit()


if __name__ == '__main__':
    MainWindow()
