import PySimpleGUI as sg
import webbrowser
import json
from constants import GUI_THEME

sg.theme(GUI_THEME)
sg.set_options(background_color='#000000', text_color='#00ff00',
               button_color=('#00ff00', '#000000'))


def delete_site(site_id):
    with open('sites.json', 'r') as f:
        data = json.load(f)
    for i, site in enumerate(data):
        if str(site['id']) == str(site_id):
            del data[i]
            break
    with open('sites.json', 'w') as f:
        json.dump(data, f, indent=2)


def open_window():
    with open('sites.json', 'r') as f:
        data = json.load(f)
    headings = ['ID', 'URL', 'Log URL', 'Creation Date']

    data_rows = [[site['id'], site['url'], site['log_url'],
                  site['creation_date']] for site in data]

    table = sg.Table(values=data_rows, headings=headings,
                     auto_size_columns=False, num_rows=min(25, len(data)),
                     col_widths=[5, 30, 30, 15], justification='left',
                     font=('Consolas', 12), enable_events=True,
                     key='-TABLE-', background_color='#363434', alternating_row_color='#1f1e1e', row_height=35)
    screen_layout = [
        [sg.Text('My Phishing Sites', font=(
            'Consolas', 16), pad=((10, 10), (10, 20)))],
        [table],
        [sg.Text('Delete a Phishing Site', font=(
            'Consolas', 14), pad=((10, 20), (20, 20)))],
        [sg.Text('Site ID: '), sg.Input(key='-DELETE-ID-'),
         sg.Button('Delete', key='-DELETE-BUTTON-')]
    ]

    layout = [
        [sg.Column(screen_layout, key='screen_layout')],
    ]

    window = sg.Window('PhishPipeline', layout, size=(800, 600))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-TABLE-':
            row = values['-TABLE-'][0]
            url = data[row]['log_url']
            webbrowser.open(url)
        elif event == '-DELETE-BUTTON-':
            site_id = values['-DELETE-ID-']
            delete_site(site_id)
            with open('sites.json', 'r') as f:
                data = json.load(f)
            data_rows = [[site['id'], site['url'], site['log_url'],
                          site['creation_date']] for site in data]
            table.update(values=data_rows, num_rows=min(25, len(data)))
    window.close()


if __name__ == '__main__':
    open_window()
