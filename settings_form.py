import PySimpleGUI as sg
from constants import GUI_THEME

sg.theme(GUI_THEME)
sg.set_options(background_color='#000000', text_color='#00ff00',
               button_color=('#00ff00', '#000000'))


def open_window():
    with open('build/templates/unavailable.html', 'r') as f:
        page_contents = f.read()

    screen_layout = [
        [sg.Text('Settings', font=(
            'Consolas', 16), pad=((10, 10), (10, 20)))],
        [sg.Text('Update the landing page', font=(
            'Consolas', 14), pad=((10, 10), (10, 10)))],
        [sg.Text('the victim will land on this page after logging in to the phishing site', font=(
            'Consolas', 12), pad=((10, 10), (10, 10)))],
        [sg.Multiline(key='-LANDING-PAGE-',
                      default_text=page_contents, size=(540, 20))],
        [sg.Button('Update Page', font=('Consolas', 12), key='-UPDATE-BUTTON-',
                   bind_return_key=True)]
    ]

    layout = [
        [sg.Column(screen_layout, key='screen_layout')],
    ]

    window = sg.Window('PhishPipeline', layout, size=(800, 600))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-UPDATE-BUTTON-':
            markup = values['-LANDING-PAGE-']
            with open('build/templates/unavailable.html', 'w') as f:
                f.write(values['-LANDING-PAGE-'])
    window.close()


if __name__ == '__main__':
    open_window()
