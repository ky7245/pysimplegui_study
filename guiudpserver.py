import socket
import threading
import PySimpleGUI as sg
import socketserver

LISTEN_PORT = 8080


class ThreadingUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{}:{} wrote:".format(
            self.client_address[0], self.client_address[1]))
        print(data.decode('utf-8'))
        socket.sendto(data.upper(), self.client_address)


def start_thread(window, udpd):
    udpd.serve_forever()


def end_thread(udpd):
    udpd.shutdown()


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

    udpd = ThreadingUDPServer(('localhost', LISTEN_PORT), MyUDPHandler)

    while True:             # Event Loop
        event, values = window.read()
        sg.cprint(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event.startswith('Start'):
            window['Start'].update(disabled=True)
            window['Stop'].update(disabled=False)

            udpserverThread = threading.Thread(target=start_thread, args=(
                window, udpd), daemon=True)
            udpserverThread.start()

        if event.startswith('Stop'):
            threading.Thread(target=end_thread, args=(
                udpd, ), daemon=True).start()
            window['Start'].update(disabled=False)
            window['Stop'].update(disabled=True)

    window.close()


if __name__ == '__main__':
    main()
