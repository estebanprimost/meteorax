'''
    TODO: DOC
'''

import os

from gi.repository import Gtk

from pyart.graph import RadarMapDisplayBasemap

from matplotlib import pyplot as plot
from matplotlib.backends import backend_gtk3, backend_gtk3agg

from meteorax.gui.productos.producto import Producto
from meteorax.gui.util import Util as GuiUtil
from meteorax.core.radar import Radar

NavigationToolbar = backend_gtk3.NavigationToolbar2GTK3
FigureCanvas = backend_gtk3agg.FigureCanvasGTK3Agg


class PPI(Producto):
    '''
        TODO: DOC
    '''

    def __init__(self, elevacion=0, **kwargs):
        super(PPI, self).__init__(kwargs['titulo'])

        self.__elevacion = int(elevacion)
        self.__figura = plot.figure(figsize=(10, 10))
        self.__figura.subplots_adjust(top=0.97, bottom=0.02)
        self.__grafico = self.__figura.add_subplot(1, 1, 1, aspect=1.0)
        self.__radar_display = RadarMapDisplayBasemap(Radar.radar_pyart())
        self.__archivo_mapa = '%s/../shapes/departamental' % os.path.dirname(
            __file__)
        # print(self.__radar_display.basemap.)

        self.mostrar()

    def dibujar(self):
        '''
            TODO: DOC
        '''

        box = self.window.get_box_output()

        self.make_ppi_plot()

        canvas = FigureCanvas(self.__figura)
        canvas.props.height_request = 550
        canvas.props.width_request = 710

        box.pack_end(canvas, True, True, 0)

        NavigationToolbar.toolitems = GuiUtil.botones_barra()

        toolbar = NavigationToolbar(canvas, self.window.get_window())

        box.pack_end(toolbar, False, False, 0)

        if Radar.cantidad_de_elevaciones() > 1:
            adjustment = Gtk.Adjustment(
                value=1,
                lower=1,
                upper=Radar.cantidad_de_elevaciones(),
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

            for tick in range(1, Radar.cantidad_de_elevaciones() + 1):
                scale.add_mark(tick, Gtk.PositionType.BOTTOM, '%s' % tick)
                scale.add_mark(tick,
                               Gtk.PositionType.TOP,
                               '%s°' % Radar.grado_elevacion(tick - 1))

            scale.connect('value-changed', self.value_changed_elevacion)

            frame = Gtk.Frame()
            frame.set_label('Elevación')
            frame.label_xalign = 0
            frame.label_yalign = 0.5
            frame.add(scale)

            box.pack_end(frame, True, True, 0)

    def make_ppi_plot(self):
        '''
            TODO: DOC
        '''
        variable = Radar.variable()
        datos_variable = Radar.datos_de_variable()
        nombre_variable = Radar.nombre_variable_extendido()
        titulo = '%s (%s)\n%s° Elevación (%s°)' % (
            nombre_variable,
            variable,
            self.__elevacion + 1,
            Radar.grado_elevacion(self.__elevacion)
        )

        basemap = self.__radar_display.basemap

        self.__radar_display = RadarMapDisplayBasemap(Radar.radar_pyart())

        self.__radar_display.plot_ppi_map(
            field=Radar.nombre_variable(),
            sweep=self.__elevacion,
            vmin=datos_variable['vmin'],
            vmax=datos_variable['vmax'],
            cmap=datos_variable['colormap'],
            ax=self.__grafico,
            fig=self.__figura,
            colorbar_label='',
            title=titulo,
            shapefile=self.__archivo_mapa,
            basemap=basemap
        )

        radio_de_escaneo = int(Radar.radio_de_escaneo())
        circulos_rango = [100]

        if radio_de_escaneo == 240:
            circulos_rango = circulos_rango + [200, 300]

        if radio_de_escaneo == 480:
            circulos_rango = circulos_rango + [400, 500]

        self.__radar_display.plot_range_rings(
            circulos_rango, lw=0.5, ls='dotted')
        self.__radar_display.basemap.fillcontinents(
            color='#cccccc', lake_color='aqua', alpha=0.2)

        for distancia_circulo in circulos_rango:
            self.__grafico.text(
                (radio_de_escaneo + distancia_circulo) * 1000,
                radio_de_escaneo * 1000,
                '%sKm' % distancia_circulo,
                fontsize=8,
                clip_on=True
            )

    def actualizar_grafico(self):
        '''
            TODO: DOC
        '''

        self.__radar_display.cbs[0].remove()

        plot.gca().cla()
        self.make_ppi_plot()

        self.__figura.canvas.flush_events()
        self.__figura.canvas.draw()

    def value_changed_elevacion(self, widget):
        '''
            TODO: DOC
        '''
        sweep = int(widget.get_value() - 1)
        if self.__elevacion != sweep:
            self.__elevacion = sweep
            self.actualizar_grafico()
