import os

from cffi import FFI

ffi = FFI()

ffi.set_source("libqrencode._ffi",
    "#include <qrencode.h>",
    libraries=["qrencode"],
)
with open(os.path.join(os.path.dirname(__file__), "qrencode-3.4.4-noifdefs.h")) as f:
    ffi.cdef("""
        #define EINVAL ...
        #define ENOMEM ...
    """ + f.read())

if __name__ == "__main__":
    ffi.compile()
