import numpy as np
import scipy.signal

class IIRFilter:
    def __init__(self, **kwargs):
        if kwargs.pop('design', False):
            self.sos = scipy.signal.iirdesign(output='sos', analog=False, **kwargs)
        elif 'sos' in kwargs:
            self.sos = kwargs['sos']
        elif 'tf' in kwargs:
            self.sos = scipy.signal.tf2sos(*kwargs['tf'])
        elif 'zpk' in kwargs:
            self.sos = scipy.signal.zpk2sos(*kwargs['zpk'])
        else:
            raise NotImplementedError()
        self.axis = kwargs.pop('axis', -1)
        self.dtype = kwargs.pop('dtype', np.complex128)
        self.zi_shape = list(kwargs.pop('shape', (None,)))
        self.zi_shape[self.axis] = 2
        self.reset()
    def reset(self):
        self.zi = np.zeros((self.sos.shape[0],) + tuple(self.zi_shape), self.dtype)
    @staticmethod
    def lowpass(freq):
        return IIRFilter(design=True, wp=freq*2, ws=freq*2*1.2, gpass=.021, gstop=30, ftype='butter')
    def __call__(self, x):
        y, self.zi = scipy.signal.sosfilt(self.sos, x, axis=self.axis, zi=self.zi)
        return y
