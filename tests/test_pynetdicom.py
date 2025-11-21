import threading
import time
import sys
from pynetdicom import AE, evt, debug_logger
from pynetdicom.sop_class import Verification

# debug_logger()

def test_pynetdicom_echo():
    # Define the AE
    ae = AE()
    ae.add_supported_context(Verification)
    ae.add_requested_context(Verification)

    # Callback for when a verification request is received
    def handle_echo(event):
        return 0x0000

    handlers = [(evt.EVT_C_ECHO, handle_echo)]

    # Start the SCP in a separate thread
    port = 11112
    print(f"Starting SCP on port {port}...")
    scp = ae.start_server(('', port), block=False, evt_handlers=handlers)

    try:
        # Give the server a moment to start
        time.sleep(1)

        # Send C-ECHO
        print("Sending C-ECHO...")
        assoc = ae.associate('127.0.0.1', port)

        if assoc.is_established:
            status = assoc.send_c_echo()
            print(f"C-ECHO response status: 0x{status.Status:04x}")
            assoc.release()

            if status.Status == 0x0000:
                print("SUCCESS: C-ECHO successful.")
            else:
                print("FAILURE: C-ECHO failed.")
                sys.exit(1)
        else:
            print("FAILURE: Association rejected, aborted or never connected")
            sys.exit(1)

    finally:
        print("Stopping SCP...")
        scp.shutdown()

if __name__ == "__main__":
    test_pynetdicom_echo()
