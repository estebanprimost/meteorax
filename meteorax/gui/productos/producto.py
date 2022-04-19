'''
    TODO: DOC
'''

import abc
from meteorax.gui.productos.window import Window


class Producto(object):
    '''
        TODO: DOC
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, title):
        super(Producto, self).__init__()

        self.titulo = title
        self.window = None

    @abc.abstractmethod
    def dibujar(self):
        '''
            TODO: DOC
        '''
        return

    def mostrar(self):
        '''
            TODO: DOC
        '''

        self.window = Window(self.titulo, self.dibujar)
        self.window.mostrar()
        return
