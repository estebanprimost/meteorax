'''
    TODO: DOC
'''

from meteorax.gui.util import Util as GuiUtil
from meteorax.core.radar import Radar
from meteorax.core.radarutil import RadarUtil
from meteorax.gui.resultados.resultado import Resultado

class Escaneo(Resultado):
    '''
        TODO: DOC
    '''

    def mostrar(self):
        agregar_box = GuiUtil.agregar_box_datos
        box = self.box_data

        agregar_box('Fecha', RadarUtil.humanizar_fecha(Radar.fecha()), box)
        agregar_box('Hora', RadarUtil.humanizar_hora(Radar.hora()), box)
        agregar_box('Tiempo estimado', '%s s' % Radar.tiempo_de_escaneo(), box)
        agregar_box('Tipo de escaneo', '%s' % Radar.nombre_tipo_de_escaneo(), box)
        agregar_box('Radio de alcance', '%s km' % Radar.radio_de_escaneo(), box)
        agregar_box('Variable analizada', '%s - %s' % (
            Radar.variable(), Radar.nombre_variable_extendido()), box)

        if Radar.escaneo_en_volumen():
            agregar_box('Elevaciones', '%s' % Radar.cantidad_de_elevaciones(), box)
            agregar_box('Primera elevación', '%s°' % Radar.grado_primera_elevacion(), box)
            agregar_box('Última elevación', '%s°' % Radar.grado_ultima_elevacion(), box)
        else:
            agregar_box('Elevación', '%s°' % Radar.grado_elevacion_escaneo_azimut(), box)
            agregar_box('Inicio azimuth', '%s°' % Radar.grado_primer_azimut(), box)
            agregar_box('Fin azimuth', '%s°' % Radar.grado_ultimo_azimut(), box)

        self.frame.show()
