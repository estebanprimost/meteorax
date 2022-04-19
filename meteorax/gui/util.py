'''
    TODO: DOC
'''

from gi.repository import Gtk


class Util(object):
    '''
        TODO: DOC
    '''
    # gladefile_box_data = None
    __instance = None
    builder = None

    def __new__(cls, builder, box_data_file):
        if Util.__instance is None:
            Util.__instance = object.__new__(cls)

        Util.__instance.builder = builder
        Util.__instance.gladefile_box_data = box_data_file
        Util.__instance.box_data_radar = builder.get_object('box-data-radar')
        Util.__instance.box_data_escaneo = builder.get_object('box-data-escaneo')
        Util.__instance.box_data_productos = builder.get_object('box-data-productos')

        return Util.__instance

    @classmethod
    def agregar_box_datos(cls, label, value, parent=None, options=None):
        '''
            TODO: DOC
        '''
        if options is None:
            options = []

        builder = Util.__instance.builder
        builder.add_from_file(Util.__instance.gladefile_box_data)

        box_data = builder.get_object('box-data')
        box_label = builder.get_object('label')
        box_value = builder.get_object('value')

        box_label.set_text(label)
        box_value.set_markup('<b>%s</b>' % value)

        (parent if parent is not None else Util.__instance.box_data_radar).add(
            box_data)

    @classmethod
    def agregar_boton(cls, label, parent, action):
        '''
            TODO: DOC
        '''
        button = Gtk.Button(label=label)
        button.set_visible(True)

        if action is not None:
            button.connect('clicked', action)

        parent.add(button)

    @classmethod
    def botones_barra(cls):
        '''
            TODO: DOC
        '''
        return (
            ('Home', 'Volver a la vista original', 'home', 'home'),
            ('Back', 'Ir a la vista previa', 'back', 'back'),
            ('Forward', 'Ir a la vista siguiente', 'forward', 'forward'),
            (None, None, None, None),
            # ('Pan', 
            #   'Mover presionando el click izquierdo,
            #   acercar con el derecho', 'move', 'pan'),
            ('Zoom', 'Acercar al rectángulo seleccionado', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'Configurar sub-plots', 'subplots', 'configure_subplots'),
            ('Save', 'Guardar como imagen', 'filesave', 'save_figure'),
        )
