'''
    TODO: DOC
'''

from pyart.config import get_field_colormap, get_field_limits

NOMBRES_RADAR = {
    'INTA_Parana': {
        'completo': 'Paraná - Entre Ríos',
        'abrev': 'PAR'
    },
    'INTA_Anguil': {
        'completo': 'Anguil - La Pampa',
        'abrev': 'ANG'
    },
    'INTA_Pergamino': {
        'completo': 'Pergamino - Buenos Aires',
        'abrev': 'PER'
    },
}

NOMBRES_TIPOS_DE_ESCANEO = {
    'vol': 'Escaneo en volumen',
    'azi': 'Escaneo en azimuth'
}

VARIABLES = {
    'dbz': {
        'name': 'reflectivity',
        'human': 'Reflectividad',
        'data': {
            'vmin': get_field_limits('reflectivity')[0],
            'vmax': get_field_limits('reflectivity')[1],
            'colormap': get_field_colormap('reflectivity')
        }},
    'dbuz': {
        'name': 'uncorrected-reflectivity',
        'human': 'Reflectividad (sin corrección)',
        'data': {
            'vmin': get_field_limits('reflectivity')[0],
            'vmax': get_field_limits('reflectivity')[1],
            'colormap': get_field_colormap('reflectivity')
        }},
    'v': {
        'name': 'velocity',
        'human': 'Velocidad',
        'data': {
            'vmin': get_field_limits('velocity')[0],
            'vmax': get_field_limits('velocity')[1],
            'colormap': get_field_colormap('velocity')
        }},
    'w': {
        'name': 'spectrum_width',
        'human': 'Ancho espectral',
        'data': {
            'vmin': get_field_limits('spectrum_width')[0],
            'vmax': get_field_limits('spectrum_width')[1],
            'colormap': get_field_colormap('spectrum_width')
        }},
    'zdr': {
        'name': 'differential_reflectivity',
        'human': 'Reflectividad diferencial',
        'data': {
            'vmin': get_field_limits('differential_reflectivity')[0],
            'vmax': get_field_limits('differential_reflectivity')[1],
            'colormap': get_field_colormap('differential_reflectivity')
        }},
    'rhohv': {
        'name': 'cross_correlation_ratio',
        'human': 'Coeficiente de co-relación polar',
        'data': {
            'vmin': get_field_limits('cross_correlation_ratio')[0],
            'vmax': get_field_limits('cross_correlation_ratio')[1],
            'colormap': get_field_colormap('cross_correlation_ratio')
        }},
    'uphidp': {
        'name': 'uncorrected_differential_phase',
        'human': 'Fase de propagación diferencial (sin corrección)',
        'data': {
            'vmin': get_field_limits('differential_phase')[0],
            'vmax': get_field_limits('differential_phase')[1],
            'colormap': get_field_colormap('differential_phase')
        }},
}
