# Import the necessary modules for the Flask application and logging.
from flask import Flask, jsonify
import logging

# Initialize the Flask application and configure logging to debug level.
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Define the home endpoint. Logs a message and returns a welcome message when accessed.
@app.route('/')
def home():
    app.logger.info('Home endpoint was reached')
    return "Welcome to the Flask App"

# Define the status endpoint. Logs a message and returns the running status in JSON format when accessed.
@app.route('/status')
def status():
    app.logger.info('Status endpoint was reached')
    return jsonify({"status": "running"})

# Error handling for 404 errors. Logs the error and returns a JSON response with the error details.
@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('Page not found: %s', (e))
    return jsonify(error=404, text=str(e)), 404

# Run the application if this script is executed as the main program.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

