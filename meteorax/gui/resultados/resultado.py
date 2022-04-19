'''
    TODO: DOC
'''
import abc


class Resultado(object):
    '''
        TODO: DOC
    '''
    __metaclass__ = abc.ABCMeta

    box_data = None
    frame = None

    def __init__(self, box, frame):
        super(Resultado, self).__init__()
        self.box_data = box
        self.frame = frame

    @abc.abstractmethod
    def mostrar(self):
        '''
            TODO: DOC
        '''

        return

