from flask import Flask, render_template
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from db import mongo
from routes import routes_bp





# Load environment variables
load_dotenv()

app = Flask(__name__)
# MongoDB Config
app.config["MONGO_URI"] = os.getenv("MONGO_URI") # Load MongoDB URI from environment variables
# Initialize MongoDB 
mongo.init_app(app)

# JWT Secret Key
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Initialize JWT
jwt = JWTManager(app)

# Register application routes
app.register_blueprint(routes_bp)

@app.route("/")
def home():
   return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")




if __name__ == "__main__":
    app.run(debug=True)




