import threading
import PySimpleGUI as sg
import socket


def start_thread(window, values):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        msg = values['-Data-']
        ip = values['-Addr-']
        port = int(values['-Port-'])
        sock.sendto(msg.encode('utf-8'), (ip, port))
        res, dist = sock.recvfrom(1024)
        print(dist, res.decode('utf-8'))
        window['-Data-'].update(value='')
    except Exception as e:
        print(e)
    finally:
        sock.close()
        window['Send'].update(disabled=False)
        window['-Data-'].update(disabled=False, background_color="white")


def main():
    """
    The demo will display in the multiline info about the event and values dictionary as it is being
    returned from window.read()
    Every time "Start" is clicked a new thread is started
    Try clicking "Dummy" to see that the window is active while the thread stuff is happening in the background
    """

    layout = [[sg.Text('Distination Addr:'), sg.Input(key='-Addr-', size=(16, 1), default_text="127.0.0.1"), sg.Text('Distination Port:'), sg.Input(key='-Port-',
                                                                                                                                                    size=(8, 1), default_text="8080")],
              [sg.Text('Data:'), sg.Multiline(key='-Data-',
                                              size=(58, 5),)],
              [sg.Button('Send')],
              [sg.Text('Response messages', font='Any 15')],
              [sg.Multiline(size=(65, 20), key='-ML-', autoscroll=True,
                            reroute_stdout=True, write_only=True, reroute_cprint=True)],
              ]

    window = sg.Window('UDP Sender', layout)

    while True:             # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event.startswith('Send'):
            window['Send'].update(disabled=True)
            window['-Data-'].update(disabled=True, background_color="gray")
            th = threading.Thread(target=start_thread, args=(
                window, values), daemon=True)
            th.start()

    window.close()


if __name__ == '__main__':
    main()
