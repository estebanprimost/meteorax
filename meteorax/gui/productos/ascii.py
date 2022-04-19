import tempfile

from meteorax.core.radar import Radar
from meteorax.gui.productos.geotiff import GeoTIFF


class ASCII(GeoTIFF):
    def exportar(self, elevaciones, carpeta_destino):
        carpeta_origen = tempfile.gettempdir()

        archivos = Radar.exportar_tif(elevaciones, carpeta_origen)

        Radar.exportar_ascii(archivos, carpeta_origen, carpeta_destino)
