'''
    TODO: DOC
'''

from meteorax.gui.util import Util
from meteorax.core.radar import Radar as RadarMeteorax
from meteorax.gui.resultados.resultado import Resultado

class Radar(Resultado):
    '''
        TODO: DOC
    '''

    def mostrar(self):
        '''
            TODO: DOC
        '''
        agregar_box = Util.agregar_box_datos

        agregar_box('Radar', RadarMeteorax.nombre()['completo'])
        agregar_box('Longitud de onda', '%s cm' % RadarMeteorax.longitud_de_onda())
        agregar_box('Ancho del haz', '%s°' % RadarMeteorax.ancho_de_haz())
        agregar_box('Latitud', '%s°' % RadarMeteorax.ubicacion().get('latitud'))
        agregar_box('Longitud', '%s°' % RadarMeteorax.ubicacion().get('longitud'))
        agregar_box('Altura de antena', '%s m' % RadarMeteorax.altura())

        self.frame.show()
