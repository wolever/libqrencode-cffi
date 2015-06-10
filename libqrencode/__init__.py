try:
    import PIL
except ImportError:
    PIL = None

from ._ffi import ffi, lib

MODE_NUL = lib.QR_MODE_NUL
MODE_NUM = lib.QR_MODE_NUM
MODE_AN = lib.QR_MODE_AN
MODE_8 = lib.QR_MODE_8
MODE_KANJI = lib.QR_MODE_KANJI
MODE_STRUCTURE = lib.QR_MODE_STRUCTURE
MODE_ECI = lib.QR_MODE_ECI
MODE_FNC1FIRST = lib.QR_MODE_FNC1FIRST
MODE_FNC1SECOND = lib.QR_MODE_FNC1SECOND

ECLEVEL_L = lib.QR_ECLEVEL_L
ECLEVEL_M = lib.QR_ECLEVEL_M
ECLEVEL_Q = lib.QR_ECLEVEL_Q
ECLEVEL_H = lib.QR_ECLEVEL_H

# Raw QR code data bitmask
#   76543210 LSB
#   |||||||`- 1=black/0=white
#   ||||||`-- data and ecc code area
#   |||||`--- format information
#   ||||`---- version information
#   |||`----- timing pattern
#   ||`------ alignment pattern
#   |`------- finder pattern and separator
#   `-------- non-data modules (format, timing, etc.)
DATA_BW = 1 << 0
DATA_DATA_AND_ECC = 1 << 1
DATA_FORMAT_INFO = 1 << 2
DATA_VERSION_INFO = 1 << 3
DATA_TIMING_PATTERN = 1 << 4
DATA_ALIGNMENT_PATTERN = 1 << 5
DATA_FINDER_PATTERN = 1 << 6
DATA_NON_DATA = 1 << 7


def api_version_string():
    return ffi.string(lib.QRcode_APIVersionString())

def api_version():
    ver = ffi.new("int[3]")
    lib.QRcode_APIVersion((ver + 0), (ver + 1), (ver + 2))
    return tuple(ver[0:3])


class QRCode(object):
    def __init__(self, data, mode=None, version=None, error_correction=None):
        to_free = []
        try:
            input = lib.QRinput_new()
            if input == ffi.NULL:
                raise MemoryError("Couldn't allocate memory for QR code")
            to_free.append((lib.QRinput_free, input))

            if version is not None:
                err = lib.QRinput_setVersion(input, version)
                if err:
                    raise ValueError("Invalid version: %r" %(version, ))

            if error_correction is not None:
                err = lib.QRinput_setErrorCorrectionLevel(input, error_correction)
                if err:
                    raise ValueError("Invalid error_correction: %r" %(error_correction, ))

            if mode is None:
                mode = MODE_8
            self.mode = mode

            err = lib.QRinput_append(input, mode, len(data), data)
            if err:
                if ffi.errno == lib.ENOMEM:
                    raise MemoryError("Couldn't allocate memory for QR code")
                raise ValueError("Invalid QR code mode (%r) or data" %(mode, ))

            qrc = lib.QRcode_encodeInput(input)
            if qrc == ffi.NULL:
                if ffi.errno == lib.ENOMEM:
                    raise MemoryError("Couldn't allocate memory for QR code")
                raise ValueError("Invalid QR code input")
            to_free.append((lib.QRcode_free, qrc))
            self.width = qrc.width
            self.raw_data = list(qrc.data[0:self.width * self.width])
        finally:
            for func, arg in to_free:
                func(arg)

    def get_raw_data(self):
        return self.raw_data

    def get_im(self, border=None, module_size=None):
        if PIL is None:
            raise ImportError("PIL must be installed to use get_im")
        border = 4 if border is None else border
        module_size = 3 if module_size is None else module_size
        bytes = []
