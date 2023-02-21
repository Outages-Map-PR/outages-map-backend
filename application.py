from flask import Flask, jsonify

application = Flask(__name__)

@application.route('/hello', methods=['GET'])
def hello_world():
    res = "Hello, World!"
    return jsonify(res)

if __name__ == '__main__':
    application.run()