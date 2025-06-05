from flask import Flask
from flask_cors import CORS
from auth import auth  # your blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS globally

# Register your blueprint
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
