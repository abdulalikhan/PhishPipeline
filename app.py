import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Replace <login_page_url> with the actual login page URL
login_url = "https://flexstudent.nu.edu.pk/"
base_url = "/".join(login_url.split("/")[:-1])

# Create a session to handle cookies and authentication
session = requests.Session()

# Get the login page HTML
response = session.get(login_url)
html = response.content

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all the forms in the HTML
forms = soup.find_all("form")

# Edit the forms to add the method and action attributes
for form in forms:
    form["method"] = "post"
    form["action"] = "/login"

# Find all the assets (images, CSS, and JavaScript) in the HTML
assets = soup.find_all(["img", "link"])

# Resolve the URLs of the assets
for asset in assets:
    if asset.has_attr("src"):
        asset["src"] = urljoin(base_url, asset["src"])
    elif asset.has_attr("href"):
        asset["href"] = urljoin(base_url, asset["href"])

# Save the updated HTML to a new file
with open("build/templates/index.html", "w") as f:
    f.write(str(soup))

# Define the command to run
command = "vercel --cwd build/ --yes --name ehcp-test"

# Run the command and capture the output
output = subprocess.check_output(command, shell=True)

# Print the output
print(output.decode())
