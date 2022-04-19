from gi.repository import Gtk

from meteorax.core.radar import Radar
from meteorax.gui.productos.producto import Producto


class GeoTIFF(Producto):
    def __init__(self, **kwargs):
        super(GeoTIFF, self).__init__(kwargs['titulo'])

        self.__spins = {
            'min': None,
            'max': None
        }

        self.__spins_signals = {
            'min': None,
            'max': None
        }

        self.mostrar()

    def dibujar(self):
        box = self.window.get_box_output()

        contenido_frame = None

        if Radar.cantidad_de_elevaciones() == 1:
            contenido_frame = Gtk.Label(
                'Sólo hay una elevación (%s°)' % Radar.grado_primera_elevacion())
            contenido_frame.set_margin_bottom(10)
            contenido_frame.set_margin_top(5)
        else:
            hbox = Gtk.HBox()

            for n_input in [{
                'type': 'min',
                'label': 'Primera elevación: '
            }, {
                'type': 'max',
                'label': 'Última elevación: '
            }]:
                adj = Gtk.Adjustment(
                    value=1,
                    lower=1,
                    upper=Radar.cantidad_de_elevaciones(),
                    step_increment=1,
                    page_increment=0,
                    page_size=0
                )

                spin = Gtk.SpinButton()
                spin.set_adjustment(adj)
                spin.set_numeric(True)
                self.__spins_signals[n_input['type']] = spin.connect(
                    'value-changed', self.value_changed_elevaciones, n_input['type'])
                self.__spins[n_input['type']] = spin

                hbox.add(Gtk.Label(label=n_input['label']))
                hbox.add(spin)

            hbox.set_spacing(10)
            hbox.set_margin_bottom(10)
            hbox.set_margin_top(5)
            hbox.set_margin_start(10)
            hbox.set_margin_end(10)
            contenido_frame = hbox

        frame = Gtk.Frame()
        frame.set_label('Elevaciones a exportar')
        frame.label_xalign = 0
        frame.label_yalign = 0.5
        frame.add(contenido_frame)
        frame.add(contenido_frame)

        button = Gtk.Button(label='Exportar')
        button.connect('clicked', self.click_generar)

        box.pack_end(button, True, True, 0)
        box.pack_end(frame, True, True, 0)

    def click_generar(self, widget=None):
        chooser_dialog = Gtk.FileChooserDialog(
            title='Seleccionar carpeta para exportar',
            transient_for=self.window.get_window(),
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        chooser_dialog.add_button('Cancelar', Gtk.ResponseType.CANCEL)
        chooser_dialog.add_button('Aceptar', Gtk.ResponseType.ACCEPT)

        chooser_dialog.set_modal(True)
        chooser_dialog.connect('response', self.response_carpeta_seleccionada)
        chooser_dialog.show()

    def response_carpeta_seleccionada(self, dialog, response_id):

        if response_id == int(Gtk.ResponseType.ACCEPT):
            carpeta = dialog.get_file().get_path()
            dialog.destroy()

            elevaciones = range(self.__min() - 1, self.__max())

            self.exportar(elevaciones, carpeta)

            confirm_dialog = Gtk.MessageDialog(transient_for=self.window.get_window(),
                                               message_type=Gtk.MessageType.INFO,
                                               buttons=Gtk.ButtonsType.OK,
                                               text="Imágenes exportadas con éxito")
            confirm_dialog.run()
            confirm_dialog.destroy()

    def exportar(self, elevaciones, carpeta_destino):
        Radar.exportar_tif(elevaciones, carpeta_destino)

    def value_changed_elevaciones(self, widget, tipo):
        min_actual = self.__spins['min'].get_value()
        max_actual = self.__spins['max'].get_value()

        self.__spins['min'].disconnect(self.__spins_signals['min'])
        self.__spins['max'].disconnect(self.__spins_signals['max'])

        r_cantidad_e = int(Radar.cantidad_de_elevaciones())

        if tipo == 'min':
            self.__spins['max'].set_adjustment(
                Gtk.Adjustment(
                    value=max_actual if max_actual in range(
                        int(widget.get_value()),
                        r_cantidad_e + 1
                    ) else min_actual,

                    lower=int(widget.get_value()),
                    upper=r_cantidad_e,
                    step_increment=1,
                    page_increment=1,
                    page_size=0
                )
            )
        else:
            self.__spins['min'].set_adjustment(
                Gtk.Adjustment(
                    value=min_actual if min_actual in range(
                        1, int(widget.get_value()) + 1) else max_actual,
                    lower=1,
                    upper=int(widget.get_value()),
                    step_increment=1,
                    page_increment=1,
                    page_size=0
                )
            )

        self.__spins_signals['min'] = self.__spins['min'].connect(
            'value-changed', self.value_changed_elevaciones, 'min')
        self.__spins_signals['max'] = self.__spins['max'].connect(
            'value-changed', self.value_changed_elevaciones, 'max')

    def __min(self):
        return int(self.__spins['min'].get_value())

    def __max(self):
        return int(self.__spins['max'].get_value())
