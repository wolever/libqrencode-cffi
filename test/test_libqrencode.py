import libqrencode as qr

def test_version():
    assert qr.api_version_string() == b"3.4.4"
