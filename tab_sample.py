

import PySimpleGUI as sg


def main():

    main_tab = [[sg.Text("main setting"), sg.InputText("default value")],
                [sg.Button("Run"), sg.Button("Exit")],
                [sg.HSep()],
                [sg.Multiline(size=(65, 20), key='-ML-', autoscroll=True,
                              reroute_stdout=True, write_only=True, reroute_cprint=True)],
                ]

    config_tab = [[sg.Text("param1"), sg.InputText("default param")],
                  [sg.Text("param2"), sg.InputText("default param")],
                  ]

    layout = [[sg.Text("Sample")],
              [sg.TabGroup([
                  [sg.Tab('Main', main_tab), sg.Tab('config', config_tab)]
              ])],
              ]

    window = sg.Window("Tab Sample", layout=layout)

    while True:             # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    window.close()


if __name__ == '__main__':
    main()
