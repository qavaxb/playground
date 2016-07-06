'''
Script to create node of botnet
'''
import argparse
import logging
import subprocess
import socketserver
from xml.etree import ElementTree


LIST_ACCESSIBLE_COMMANDS = ['ls', 'cat', 'sleep', 'echo']
DEFAULT_TIMEOUT = 1

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(name='botnet_node')


def handle_xml_request(data_recved):
    """
    Function to process XML data and extract commands
    """
    root = ElementTree.fromstring(data_recved)
    command_list = []

    if "execute" in root.tag:

        for child in root:
            cmd_dict = {}

            if "command" in child.tag:

                if "timeout" in child.attrib:
                    cmd_dict["timeout"] = int(child.attrib["timeout"])

                else:
                    cmd_dict["timeout"] = DEFAULT_TIMEOUT

                cmd_dict["command"] = child.text.split()
                command_list.append(cmd_dict)

            else:
                LOGGER.warning("Invalid XML child")

    else:
        LOGGER.warning("Invalid XML root")

    return command_list


def run_cmd(cmd, timeout):
    """
    Function spawning processes with requested commands
    """
    result = ''.encode()
    LOGGER.debug('Executing command: %s', cmd)

    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:

        try:
            proc_stdout, proc_stderr = proc.communicate(timeout=timeout)

            if proc_stdout:
                LOGGER.debug("Received: %s", proc_stdout)
                result = proc_stdout

            if proc_stderr:
                LOGGER.error("Error occurred: %s", proc_stderr)

        except subprocess.TimeoutExpired:
            result = "Timeout expired".encode()

    return result


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    RequestHandler subclass
    """

    def handle(self):
        """
        Handler function for processing incoming data
        """

        self.data = self.request.recv(1024).strip()
        cmd = self.data.decode("utf8")
        LOGGER.debug(msg=cmd)

        # Dummy detection of xml notation
        if cmd.startswith("<"):
            LOGGER.debug(msg="Received XML format")
            command_list = handle_xml_request(cmd)

        else:
            LOGGER.debug(msg="Received raw format")
            command_list = [{"command": cmd.split()}]

        for command_args in command_list:

            if command_args["command"][0] in LIST_ACCESSIBLE_COMMANDS:
                response = run_cmd(command_args["command"],
                                   command_args["timeout"])
                self.request.sendall(response)

            else:
                LOGGER.warning(msg="Received invalid command")
                self.request.sendall(bytes("Invalid command", encoding='utf8'))


def _handle_args():
    """
    Handler function for command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--port',
                        type=int,
                        default=1337,
                        help='TCP connection port number')
    parser.add_argument('--host',
                        default="127.0.0.1",
                        help='TCP connection host IP')

    return parser.parse_args()


def main():
    """
    Main function to execute when starting script
    """
    args = _handle_args()
    address = (args.host, args.port)
    srv = socketserver.TCPServer(address, MyTCPHandler)

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.socket.close()


if __name__ == "__main__":
    main()
