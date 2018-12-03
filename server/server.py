from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/json2')
def ret_jsonjson():
    return jsonify({"aaa": 12, "bbb": ["bbb", 12, 12]})


if __name__ == '__main__':
    app.run()
