import shutil
import PySimpleGUI as sg
import create_form as cf
import mysites_form as msf
import settings_form as sf
from constants import VERCEL_INSTALL_URL, GUI_THEME
    
if shutil.which("vercel") is None:
    print("⚠️ Vercel CLI is not installed.")
    print(f"➡️ Please install it by following the instructions at: {VERCEL_INSTALL_URL}")
    user_input = input("Would you like to open the installation page? (yes/no): ").strip().lower()
    if user_input in ("yes", "y"):
        import webbrowser
        webbrowser.open(VERCEL_INSTALL_URL)
    else:
        print("You can install it later by running: npm install -g vercel")
    exit()

sg.theme(GUI_THEME)
sg.set_options(background_color='#000000', text_color='#00ff00',
               button_color=('#00ff00', '#000000'))

my_sites_button = sg.Button(key='my_sites', tooltip='My Phishing Sites', image_filename='icons/my_sites.png',
                            image_size=(100, 100), pad=(10, 10), button_color=('#00ff00', '#0ea10e'), border_width=0)
new_site_button = sg.Button(key='new_site', tooltip='Create a New Phishing Site', image_filename='icons/create.png',
                            image_size=(100, 100), pad=(10, 10), button_color=('#00ff00', '#0ea10e'), border_width=0)
settings_button = sg.Button(key='settings', tooltip='Settings', image_filename='icons/settings.png',
                            image_size=(100, 100), pad=(10, 10), button_color=('#00ff00', '#0ea10e'), border_width=0)
layout = [
    [sg.Text('PhishPipeline v1.0', font=(
        'Consolas', 16), pad=((10, 10), (10, 0)))],
    [sg.Text('Select an option', font=('Consolas', 14),
             size=(30, 1), pad=((10, 10), (10, 10)))],
    [sg.Column([
        [my_sites_button,
         new_site_button,
         settings_button]
    ], justification='center', element_justification='center')],
]

window = sg.Window('PhishPipeline', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "my_sites":
        # Navigate to My Phishing Sites window
        msf.open_window()
    elif event == "new_site":
        # Navigate to Create a New Phishing Site window
        cf.open_window()
    elif event == "settings":
        # Navigate to Settings window
        sf.open_window()

window.close()