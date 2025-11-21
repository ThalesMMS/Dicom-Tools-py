from DICOM_reencoder.core.network import VerificationServer, send_c_echo


def test_pynetdicom_echo_roundtrip():
    with VerificationServer() as server:
        status = send_c_echo(server.host, server.port)
        assert status == 0x0000
