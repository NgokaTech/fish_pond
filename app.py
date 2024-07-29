from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Tunajaribu Mitambo, vipi huko Duniani Wazima!!"

if __name__ == "__main__":
    app.run()
