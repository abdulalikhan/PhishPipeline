# PhishPipeline

A custom phishing site and message generator with deployment support.

## Disclaimer
PhishPipeline was developed as part of an Ethical Hacking course and is intended for educational purposes only. It demonstrates how modern phishing attacks can be automated using Generative AI including the use of Large Language Models (LLMs) like Cohere to create highly convincing bait messages.

PhishPipeline is designed to help cybersecurity professionals understand the potential dangers of AI-driven phishing attacks and improve defenses against them. It should only be used in controlled environments, such as penetration testing or training scenarios, with explicit permission from all involved parties.

## About
Recently published threat reports indicate that phishing attacks have become more rampant in recent times. There has also been a dramatic shift from generic, bulk phishing attacks to more sophisticated, targeted phishing attacks.

This page proposes the use of a tool – **PhishPipeline** to serve as a custom phishing site generator that will automate the entire process of carrying out a phishing attack. The attack process is referred to as the *"Phishing Pipeline"* i.e. the set of stages from researching the target and setting up the phishing page to deploying the site and then crafting a message to trick the victim. The attacker enters a target URL into the application and PhishPipeline creates and deploys a phishing site using the content from the entered URL. The application also asks the attacker for the victim‘s interests, and uses those interests to generate a phishing message using a large language model with the phishing link embedded in it, to persuade the victim to supply their credentials.

## Diagrams and screenshots
### Illustration

<img src="https://github.com/abdulalikhan/PhishPipeline/blob/main/diagram.png?raw=true" alt="System Diagram" width="65%">

### Menu screen
<img src="https://github.com/abdulalikhan/PhishPipeline/blob/main/screenshots/menu_screen.png?raw=true" alt="Menu Screen" width="65%">

### Generating a phishing page
<img src="https://github.com/abdulalikhan/PhishPipeline/blob/main/screenshots/s1_generation.jpeg?raw=true" alt="Generation" width="65%">

### Deploying the phishing page
<img src="https://github.com/abdulalikhan/PhishPipeline/blob/main/screenshots/s2_deployment.png?raw=true" alt="Generation" width="65%">

### Generating a bait message
<img src="https://github.com/abdulalikhan/PhishPipeline/blob/main/screenshots/s3_baitmsg.png?raw=true" alt="Bait message generation" width="65%">

<img src="https://github.com/abdulalikhan/PhishPipeline/blob/main/screenshots/s3_baitmsg2.png?raw=true" alt="Bait message generation 2" width="65%">

### Modifying the landing page
<img src="https://github.com/abdulalikhan/PhishPipeline/blob/main/screenshots/settings.png?raw=true" alt="Settings" width="65%">

### Previously created phishing sites
<img src="https://github.com/abdulalikhan/PhishPipeline/blob/main/screenshots/sites_list.png?raw=true" alt="Settings" width="65%">

### Quick Start

To get the necessary dependencies, run the following command in cmd:

```
pip install -r requirements.txt
```

To run the application locally, run the following command in cmd:

```
py app.py
```

### Requirements

- The tool uses **Vercel CLI** for automatically deploying generated phishing pages. You can install it by following the instructions at: [Vercel CLI Documentation](https://vercel.com/docs/cli).
- **Cohere API Key** is required for generating bait messages. You need to set it as an environment variable for the tool to pick it up:
  - On **Linux/macOS**:
    ```
    export COHERE_API_KEY="your-secret-key"
    ```
  - On **Windows** (CMD):
    ```
    setx COHERE_API_KEY "your-secret-key"
    ```
  - On **Windows (PowerShell)**:
    ```
    [System.Environment]::SetEnvironmentVariable("COHERE_API_KEY", "your-secret-key", "User")
    ```

For more details on setting environment variables, see: [Setting Environment Variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).


