import argparse
import logging
import socket


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(name='botnet_cmd')

def remote_procedure_call(server_address, cmd='ls'):
    sock = socket.create_connection(server_address)
    LOGGER.log(logging.DEBUG, msg='connecting to %s port %s' % server_address)
    # TODO: sanitize cmd

    try:
        # Send data
        LOGGER.log(logging.DEBUG, msg='sending "%s"' % cmd)
        if cmd is not None:
            sock.sendall(bytes(cmd, encoding='utf-8'))
        else:
            LOGGER.log(logging.DEBUG, msg="empty command")

        # Look for the response
        amount_received = 1
        minimal_expected = 5
        response = ''

        while amount_received:
            data = sock.recv(16).decode()
            amount_received = len(data)
            if amount_received:
                minimal_expected = 0
                response += data
            else:
                amount_received += minimal_expected
            if minimal_expected:
                minimal_expected -= 1

        LOGGER.log(logging.DEBUG, msg='received "%s"' % response)

    finally:
        LOGGER.log(logging.DEBUG, msg='closing socket')
        sock.close()


def _prepare_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        type=int,
                        default=1337,
                        help='TCP connection port number')
    parser.add_argument('--host',
                        default="127.0.0.1",
                        help='TCP connection host IP')
    parser.add_argument('--cmd',
                        default="",
                        help='command to execute on remote target')
    parser.add_argument('--file',
                        type=argparse.FileType('r'),
                        help='XML file with commands')

    return parser.parse_args()


def main():
    args = _prepare_parser()
    address = (args.host, args.port)
    if args.file is None:
        remote_procedure_call(address, args.cmd)
    else:
        with args.file as cmd_file:
            file_contents = cmd_file.readlines()
            remote_procedure_call(address, '\n'.join(file_contents))

if __name__ == "__main__":
    main()
