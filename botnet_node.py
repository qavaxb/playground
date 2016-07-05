import argparse
import logging
import lxml
import socketserver
import subprocess

LIST_ACCESSIBLE_COMMANDS = ['ls', 'cat']

logging.basicConfig(level=logging.DEBUG)

def handle_xml_request(data_recved):
    pass

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        logging.log(logging.DEBUG, msg="{address} wrote:".format(address=self.client_address[0]))
        cmd = self.data.decode("utf8")
        logging.log(logging.DEBUG, msg=cmd)
        if cmd.startswith("<"):
            logging.log(logging.DEBUG, msg="Received XML format")
            handle_xml_request(cmd)
        else:
            logging.log(logging.DEBUG, msg="Received raw format")
            command_args = cmd.split()
            if command_args[0] in LIST_ACCESSIBLE_COMMANDS:
                with subprocess.Popen(command_args, stdout=subprocess.PIPE) as proc:
                    proc_stdout = proc.stdout.read()
                if proc_stdout:
                    self.request.sendall(bytes(proc_stdout))
            else:
                self.request.sendall(bytes("Invalid command", encoding='utf8'))


def _prepare_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--port', type=int, default=1337,
                    help='TCP connection port number')
    parser.add_argument('--host', default="127.0.0.1",
                    help='TCP connection host IP')

    return parser.parse_args()


def main():
    args = _prepare_parser()
    address = (args.host, args.port)
    srv = socketserver.TCPServer(address, MyTCPHandler)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.socket.close()


if __name__ == "__main__":
    main()