from datetime import datetime
from dateutil.parser import parse
from scipy.stats import linregress
import numpy as np

BSP = {
    120: {
        0.5: 2,
        1.3: 1.3,
        2.3: 1.1,
        3.5: 1.05,
        5: 1.02,
        6.9: 1,
        9.1: 0.99,
        11.8: 0.9769,
        15.1: 0.9729,
        19.2: 0.97
    },
    240: {
        0.5: 2.56,
        0.9: 1.85,
        1.3: 1.58,
        1.9: 1.36,
        2.3: 1.285,
        3: 1.2,
        3.5: 1.165,
        5: 1.1,
        6.9: 1.06,
        9.1: 1.035,
        11.8: 1.015,
        15.1: 1.004,
        19.2: 1
    },
    480: {
        0.3: 6.3
    }
}


class RadarUtil():
    @classmethod
    def formatear_fecha(cls, date, to_format):
        return datetime.strftime(parse(date), to_format)

    @classmethod
    def humanizar_fecha(cls, value):
        return RadarUtil.formatear_fecha(value, '%A %-d de %B de %Y - %d/%m/%Y').capitalize()

    @classmethod
    def humanizar_hora(cls, value):
        return RadarUtil.formatear_fecha(value, '%H:%M:%S')

    @classmethod
    def polares_a_cartesianas(cls, radius, degrees):
        return {
            'x': radius * np.cos(np.deg2rad(90 - degrees)),
            'y': radius * np.sin(np.deg2rad(90 - degrees))
        }

    @classmethod
    def calcular_bsp(cls, radio, nb):
        if nb in BSP[radio]:
            return BSP[radio][nb]
        else:
            coords_xy = {
                'x': [y for y in BSP[radio].itervalues()],
                'y': [x for x in BSP[radio].iterkeys()]
            }

            i = 0
            for coord_y in coords_xy['y']:
                coords_xy['y'][i] = coord_y * coords_xy['x'][i]
                i += 1

            coeffs = linregress(coords_xy['x'], coords_xy['y'])

            if coeffs[2] == 0.0:
                raise Exception('No se pudo crear una regresion lineal para %skm' % str(radio))

            bsp_val = (coeffs[0] * nb + coeffs[1]) / nb
            return bsp_val
