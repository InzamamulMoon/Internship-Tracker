from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return "Hello, World! Welcome to Flask!"

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
