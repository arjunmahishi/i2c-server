from display import Display
from flask import Flask, request

display = Display()


app = Flask(__name__)

@app.route('/display', methods=['POST'])
def display_handler():
    body = request.get_json()
    if body['text'] is None:
       return "ERROR: No text provided" 

    display.draw_text(body['text'])
    return "OK"

@app.route('/clear')
def clear_handler():
    display.clear()
    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
