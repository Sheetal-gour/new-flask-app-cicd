from flask import Flask
app = Flask(__name__)


# Home page 
@app.route('/')
def home():
  return "Hello , Happy New Year"

if __name__=="__main__":
    app.run(host='0.0.0.0')