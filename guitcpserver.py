import socket
import threading
import PySimpleGUI as sg
import socketserver

LISTEN_PORT = 8080


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


def start_thread(window, tcpd):
    tcpd.serve_forever()


def end_thread(tcpd):
    tcpd.shutdown()


def main():
    """
    The demo will display in the multiline info about the event and values dictionary as it is being
    returned from window.read()
    Every time "Start" is clicked a new thread is started
    Try clicking "Dummy" to see that the window is active while the thread stuff is happening in the background
    """

    layout = [[sg.Text('Received messages..', font='Any 15')],
              [sg.Multiline(size=(65, 20), key='-ML-', autoscroll=True,
                            reroute_stdout=True, write_only=True, reroute_cprint=True)],
              [sg.Text('Listen Port:'), sg.Input(key='-PORT-', size=(8, 1), default_text=LISTEN_PORT, disabled=True),
               sg.Button('Start', disabled=False), sg.Button('Stop', disabled=True)]]

    window = sg.Window('UDP Server', layout)

    tcpd = ThreadingTCPServer(('localhost', LISTEN_PORT), MyTCPHandler)

    while True:             # Event Loop
        event, values = window.read()
        sg.cprint(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event.startswith('Start'):
            window['Start'].update(disabled=True)
            window['Stop'].update(disabled=False)

            udpserverThread = threading.Thread(target=start_thread, args=(
                window, tcpd), daemon=True)
            udpserverThread.start()

        if event.startswith('Stop'):
            threading.Thread(target=end_thread, args=(
                tcpd, ), daemon=True).start()
            window['Start'].update(disabled=False)
            window['Stop'].update(disabled=True)

    window.close()


if __name__ == '__main__':
    main()
