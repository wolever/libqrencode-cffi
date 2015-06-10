import libqrencode as qr

def test_version():
    assert qr.api_version_string() == b"3.4.4"
    assert qr.api_version() == (3, 4, 4)

def test_qrcode_simple():
    qrc = qr.QRCode("hunter2")
    print qrc.data_raw
