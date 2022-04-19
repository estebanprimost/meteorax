'''
    TODO: DOC
'''

import os
import numpy as np

from pyart.graph import RadarDisplay, RadarMapDisplayBasemap

from matplotlib import pyplot as plot
from matplotlib.backends import backend_gtk3, backend_gtk3agg

from gi.repository import Gtk

from meteorax.gui.productos.producto import Producto
from meteorax.gui.util import Util as GuiUtil
from meteorax.core.radar import Radar
from meteorax.core.radarutil import RadarUtil

NavigationToolbar = backend_gtk3.NavigationToolbar2GTK3
FigureCanvas = backend_gtk3agg.FigureCanvasGTK3Agg


class RHI(Producto):
    '''
        TODO: DOC
    '''

    def __init__(self, azimut=0, **kwargs):
        super(RHI, self).__init__(kwargs['titulo'])

        self.__azimut = azimut
        self.__indicador_azimut = None

        self.__figura = plot.figure(figsize=(10, 5))

        self.__grafico = plot.subplot2grid(
            (4, 4), (0, 0), colspan=4, rowspan=2)
        self.__grafico_ppi = plot.subplot2grid(
            (4, 4), (2, 0), colspan=3, rowspan=2)

        self.__radar_display = RadarDisplay(Radar.radar_pyart())
        self.__radar_display_ppi = RadarMapDisplayBasemap(Radar.radar_pyart())
        self.__archivo_mapa = '%s/../shapes/departamental' % os.path.dirname(
            __file__)

        self.mostrar()

    def dibujar(self):
        '''
            TODO: DOC
        '''

        box = self.window.get_box_output()

        self.plotear_rhi()
        self.plotear_ppi()
        self.plotear_azimut_en_ppi()

        plot.tight_layout()
        plot.subplots_adjust(right=1, left=0.12)

        canvas = FigureCanvas(self.__figura)
        canvas.props.height_request = 550
        canvas.props.width_request = 710

        box.pack_end(canvas, True, True, 0)

        NavigationToolbar.toolitems = GuiUtil.botones_barra()

        toolbar = NavigationToolbar(canvas, self.window.get_window())

        box.pack_end(toolbar, False, False, 0)

        self.rango_azimut()

    def rango_azimut(self):
        '''
            TODO: DOC
        '''
        box = self.window.get_box_output()

        adjustment = Gtk.Adjustment(
            value=self.__azimut,
            lower=0,
            upper=359,
            step_increment=1,
            page_increment=1,
            page_size=0)

        scale = Gtk.HScale()
        scale.set_adjustment(adjustment)
        scale.set_digits(0)
        scale.set_round_digits(True)
        scale.set_hexpand(True)
        scale.set_draw_value(False)
        scale.set_margin_top(5)
        scale.set_margin_bottom(10)
        scale.set_margin_start(5)
        scale.set_margin_end(5)
        scale.set_restrict_to_fill_level(False)
        scale.set_show_fill_level(False)
        scale.set_fill_level(0)
        scale.set_has_origin(False)

        for tick in range(0, 361, 45):
            scale.add_mark(tick, Gtk.PositionType.BOTTOM, '%s°' % tick)

        scale.connect('value-changed', self.value_changed_azimut)

        frame = Gtk.Frame()
        frame.set_label('Azimut')
        frame.label_xalign = 0
        frame.label_yalign = 0.5
        frame.add(scale)

        box.pack_end(frame, True, True, 0)

    def value_changed_azimut(self, widget):
        '''
            TODO: DOC
        '''
        azimut = int(widget.get_value())
        if self.__azimut != azimut:
            self.__azimut = azimut
            self.actualizar_grafico()

    def actualizar_grafico(self):
        '''
            TODO: DOC
        '''

        self.__radar_display.cbs[0].remove()

        self.__grafico.cla()

        self.plotear_rhi()
        self.plotear_azimut_en_ppi()

        self.__figura.canvas.flush_events()
        self.__figura.canvas.draw()

    def plotear_rhi(self):
        '''
            TODO: DOC
        '''
        variable = Radar.variable()
        datos_variable = Radar.datos_de_variable()
        nombre_variable = Radar.nombre_variable_extendido()
        titulo = '%s (%s)\nAzimut: %s°' % (
            nombre_variable,
            variable,
            self.__azimut
        )

        self.__radar_display = RadarDisplay(Radar.radar_pyart())

        self.__radar_display.plot_azimuth_to_rhi(
            # edges=True,
            field=Radar.nombre_variable(),
            target_azimuth=self.__azimut,
            vmin=datos_variable['vmin'],
            vmax=datos_variable['vmax'],
            cmap=datos_variable['colormap'],
            axislabels=[
                'Distancia desde el radar en Km (Horizontal)',
                'Altura en Km'
            ],
            ax=self.__grafico,
            fig=self.__figura,
            colorbar_label='',
            title=titulo
        )

        self.__grafico.set_ylim(None, 30)

    def plotear_ppi(self):
        '''
            TODO: DOC
        '''
        datos_variable = Radar.datos_de_variable()
        titulo = 'PPI - 1° Elevación (%s°)' % (
            Radar.grado_elevacion(0)
        )

        basemap = self.__radar_display_ppi.basemap

        self.__radar_display_ppi = RadarMapDisplayBasemap(Radar.radar_pyart())

        self.__radar_display_ppi.plot_ppi_map(
            field=Radar.nombre_variable(),
            sweep=0,
            vmin=datos_variable['vmin'],
            vmax=datos_variable['vmax'],
            cmap=datos_variable['colormap'],
            ax=self.__grafico_ppi,
            fig=self.__figura,
            colorbar_label='',
            title=titulo,
            shapefile=self.__archivo_mapa,
            basemap=basemap
        )

    def plotear_azimut_en_ppi(self):
        '''
            TODO: DOC
        '''

        radio = Radar.radio_de_escaneo() * 1000

        cartesianas = RadarUtil.polares_a_cartesianas(radio, self.__azimut)
        coord_x, coord_y = [
            radio,
            radio + cartesianas['x']
        ], [
            radio,
            radio + cartesianas['y']
        ]

        if self.__indicador_azimut:
            self.__indicador_azimut.set_xdata(coord_x)
            self.__indicador_azimut.set_ydata(coord_y)
            return

        self.__indicador_azimut, = self.__grafico_ppi.plot(
            coord_x,
            coord_y,
            '-',
            linewidth=10,
            alpha=0.5
        )
