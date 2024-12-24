from contextlib import contextmanager
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    a_sound = cdll.LoadLibrary('libasound.so')
    a_sound.snd_lib_error_set_handler(c_error_handler)
    yield
    a_sound.snd_lib_error_set_handler(None)
