from display import Display
from flask import Flask, request, abort

display = Display()
app = Flask(__name__)

@app.route('/display', methods=['POST'])
def display_handler():
    body = request.get_json()
    if body['text'] is None:
        abort(400)

    display.draw_text(body['text'])
    return "OK"

@app.route('/clear', methods=['POST', 'GET'])
def clear_handler():
    display.clear()
    return "OK"

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", port=3000)
    except KeyboardInterrupt:
        display.clear()
