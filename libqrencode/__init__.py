from ._ffi import ffi, lib

def api_version_string():
    return ffi.string(lib.QRcode_APIVersionString())
