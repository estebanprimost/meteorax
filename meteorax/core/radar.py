'''
    TODO: DOC
'''
import shutil
import tempfile
from os import path, remove

from osgeo import gdal
from pyart.aux_io import read_rainbow_wrl
from pyart.io import write_grid_geotiff
from pyart.map import grid_from_radars
from wradlib.io.rainbow import read_rainbow

from meteorax.config import config as MeteoraxConfig
from meteorax.core.radarutil import RadarUtil


class Radar(object):
    __instance = None

    def __new__(cls):
        if Radar.__instance is None:
            Radar.__instance = object.__new__(cls)

        Radar.__instance.pyart = None
        Radar.__instance.wradlib = None
        Radar.__instance.archivo = None
        Radar.__instance.cache_elevaciones = {}

        return Radar.__instance

    @classmethod
    def leer(cls, archivo=''):
        '''
            Lee los datos mediante las dos librerías (PyArt y Wradlib)
        '''
        Radar.__instance.archivo = archivo
        Radar.leer_pyart()
        Radar.leer_wradlib()

    @classmethod
    def leer_pyart(cls):
        Radar.__instance.pyart = read_rainbow_wrl(Radar.__instance.archivo)

    @classmethod
    def leer_wradlib(cls):
        Radar.__instance.wradlib = read_rainbow(Radar.__instance.archivo,
                                                False)

    @classmethod
    def __campo_wl(cls, campos=None):
        if campos is None:
            campos = []

        campo = Radar.__instance.wradlib

        for field in campos:
            campo = campo.get(field)
        return campo

    @classmethod
    def radar_pyart(cls):
        return cls.__instance.pyart

    @classmethod
    def radar_wradlib(cls):
        return cls.__instance.wradlib

    @classmethod
    def nombre(cls):
        '''Nombre de la estación de radar'''
        return MeteoraxConfig.NOMBRES_RADAR[Radar.__campo_wl(
            ['volume', 'radarinfo', 'name'])]

    @classmethod
    def nombre_variable_extendido(cls):
        return MeteoraxConfig.VARIABLES[Radar.__instance.variable().lower()][
            'human']

    @classmethod
    def nombre_variable(cls):
        return MeteoraxConfig.VARIABLES[Radar.__instance.variable().lower()][
            'name']

    @classmethod
    def datos_de_variable(cls):
        return MeteoraxConfig.VARIABLES[Radar.__instance.variable().lower()][
            'data']

    @classmethod
    def longitud_de_onda(cls):
        return round(
            float(Radar.__campo_wl(['volume', 'radarinfo', 'wavelen'])) *
            int(100), 2)

    @classmethod
    def ancho_de_haz(cls):
        return Radar.__campo_wl(['volume', 'radarinfo', 'beamwidth'])

    @classmethod
    def ubicacion(cls):
        return {
            'latitud': Radar.__campo_wl(['volume', 'radarinfo', '@lat']),
            'longitud': Radar.__campo_wl(['volume', 'radarinfo', '@lon'])
        }

    @classmethod
    def altura(cls):
        return round(float(Radar.__campo_wl(['volume', 'radarinfo', '@alt'])))

    @classmethod
    def parametros(cls):
        return Radar.__campo_wl(['volume', 'scan', 'pargroup'])

    @classmethod
    def tipo_de_escaneo(cls):
        return Radar.__campo_wl(['volume', '@type'])

    @classmethod
    def nombre_tipo_de_escaneo(cls):
        return MeteoraxConfig.NOMBRES_TIPOS_DE_ESCANEO[
            Radar.__instance.tipo_de_escaneo()]

    @classmethod
    def fecha(cls):
        return Radar.__instance.pyart.time['units'].split(' ')[-1]

    @classmethod
    def hora(cls):
        return Radar.__instance.pyart.time['units'].split(' ')[-1]

    @classmethod
    def tiempo_de_escaneo(cls):
        return Radar.__campo_wl(['volume', 'scan', 'scantime'])

    @classmethod
    def radio_de_escaneo(cls):
        return int(Radar.__instance.parametros().get('stoprange'))

    @classmethod
    def cortes(cls):
        if Radar.__instance.escaneo_en_volumen():
            return Radar.__campo_wl(['volume', 'scan', 'slice'])

        return [Radar.__campo_wl(['volume', 'scan', 'slice'])]

    @classmethod
    def escaneo_en_volumen(cls):
        return Radar.__instance.tipo_de_escaneo() == 'vol'

    @classmethod
    def variable(cls):
        return Radar.__instance.cortes()[0].get('slicedata').get(
            'rawdata').get('@type')

    @classmethod
    def cantidad_de_elevaciones(cls):
        return int(Radar.__instance.pyart.nsweeps)

    @classmethod
    def grado_primera_elevacion(cls):
        return Radar.__instance.parametros().get('firstele')

    @classmethod
    def grado_ultima_elevacion(cls):
        return Radar.__instance.parametros().get('lastele')

    @classmethod
    def grado_elevacion_escaneo_azimut(cls):
        return Radar.__instance.parametros().get('posele')

    @classmethod
    def grado_primer_azimut(cls):
        return Radar.__instance.parametros().get('startazi')

    @classmethod
    def grado_ultimo_azimut(cls):
        return Radar.__instance.parametros().get('stopazi')

    @classmethod
    def grado_elevacion(cls, elevacion):
        return Radar.__instance.pyart.fixed_angle['data'][elevacion]

    @classmethod
    def grilla_cartesiana(cls, numero_elevacion):
        radar = Radar.__instance

        if not numero_elevacion in radar.cache_elevaciones:

            ele = radar.pyart.extract_sweeps([numero_elevacion])

            metros = 1000.0
            ubicacion = radar.ubicacion()
            radio_kms = radar.radio_de_escaneo()
            radio_mts = radio_kms * metros
            bins = radio_kms * 2
            grado_elevacion = radar.grado_elevacion(numero_elevacion)

            grid_shape = (1, bins, bins)
            grid_limits = ((200, 4 * metros), (-radio_mts, radio_mts),
                           (-radio_mts, radio_mts))
            weighting_function = 'Cressman'
            fields = [radar.nombre_variable()]
            nb = grado_elevacion
            bsp = RadarUtil.calcular_bsp(radar.radio_de_escaneo(),
                                         grado_elevacion)
            roi_func = 'dist_beam'
            grid_origin = (float(ubicacion['latitud']),
                           float(ubicacion['longitud']))

            grid = grid_from_radars(
                (ele, ),
                grid_shape=grid_shape,
                grid_limits=grid_limits,
                grid_origin=grid_origin,
                weighting_function=weighting_function,
                fields=fields,
                nb=nb,
                bsp=bsp,
                roi_func=roi_func)

            radar.cache_elevaciones[numero_elevacion] = grid

        return radar.cache_elevaciones[numero_elevacion]

    @classmethod
    def exportar_tif(cls, elevaciones, carpeta=None):
        carpeta = tempfile.gettempdir() if carpeta is None else carpeta

        radar = Radar.__instance

        fecha = RadarUtil.formatear_fecha(radar.fecha(), '%Y%m%d')
        hora = RadarUtil.formatear_fecha(radar.hora(), '%H%M%S')
        nombre_radar = radar.nombre()['abrev'].lower()

        archivos = []

        for elevacion in elevaciones:
            datos_archivo_salida = (
                nombre_radar, radar.variable().lower(), fecha, hora, elevacion + 1)

            archivo = '%s_%s_%s_%s_elevacion_%s' % datos_archivo_salida

            write_grid_geotiff(
                Radar.grilla_cartesiana(elevacion),
                filename=path.join(carpeta, '%s.tif' % archivo),
                field=radar.nombre_variable(),
                warp=False
            )

            archivos.append(archivo)

        return archivos

    @classmethod
    def exportar_ascii(cls, archivos, carpeta_origen, carpeta_destino):
        for archivo in archivos:
            archivo_origen = gdal.Open(
                path.join(carpeta_origen, '%s.tif' % archivo))

            driver = gdal.GetDriverByName("AAIGrid")

            archivo_ascii_temp = path.join(
                tempfile.gettempdir(), '%s.asc' % archivo)

            archivo_destino = driver.CreateCopy(
                archivo_ascii_temp, archivo_origen, 0)

            shutil.copyfile(archivo_ascii_temp, path.join(
                carpeta_destino, '%s.asc' % archivo))

            archivo_destino = None
            archivo_origen = None

        for archivo in archivos:
            for extension in [
                    '.asc',
                    '.asc.aux.xml',
                    '.prj',
                    '.tif'
                ]:
                    try:
                        remove(path.join(tempfile.gettempdir(), '%s%s' % (archivo, extension)))
                    except OSError:
                        pass
