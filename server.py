from flask import Flask, request, jsonify
from math import sqrt, pow, radians

app = Flask(__name__)


def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return str(e)


def handle_hypot(a, b):
    try:
        result = sqrt(pow(a, 2) + pow(b, 2))
        return result
    except Exception as e:
        return str(e)
    

def handle_radians(degree):
    try:
        result = radians(degree)
        return result
    except Exception as e:
        return str(e)

@app.route('/post', methods=['POST'])
def post():
    req = request.json

    user_input = req['request']['command']

    if "гипотенуза" in user_input:
        user_input = user_input.replace(
            "гипотенуза", "").replace(" ", "").strip()
        response_text = handle_hypot(int(user_input[0]), int(user_input[1]))
    if "радианы" in user_input:
        user_input = user_input.replace(
            "радианы", "").replace(" ", "").strip()
        response_text = handle_radians(int(user_input[0]))




    response = {
        "version": req['version'],
        "session": req['session'],
        "response": {
            "text": response_text,
            "end_session": False
        }
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
