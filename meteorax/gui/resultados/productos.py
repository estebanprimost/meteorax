'''
    TODO: DOC
'''

from meteorax.gui.productos.ppi import PPI
from meteorax.gui.productos.rhi import RHI
from meteorax.gui.productos.geotiff import GeoTIFF
from meteorax.gui.productos.ascii import ASCII
from meteorax.gui.util import Util
from meteorax.core.radar import Radar
from meteorax.gui.resultados.resultado import Resultado

class Productos(Resultado):
    def mostrar(self):
        if Radar.escaneo_en_volumen():
            Util.agregar_boton('PPI', self.box_data, self.on_click_ppi)

        Util.agregar_boton('RHI', self.box_data, self.on_click_rhi)
        Util.agregar_boton('GeoTIFF', self.box_data, self.on_click_geotiff)
        Util.agregar_boton('Grilla ASCII', self.box_data, self.on_click_ascii_grid)

        self.frame.show()

    def on_click_ppi(self, widget=None):
        PPI(elevacion=0, titulo='PPI')

    def on_click_rhi(self, widget):
        RHI(titulo='RHI', azimut=0)

    def on_click_ascii_grid(self, widget):
        ASCII(titulo='ASCII')

    def on_click_geotiff(self, widget):
        GeoTIFF(titulo='GeoTIFF')
