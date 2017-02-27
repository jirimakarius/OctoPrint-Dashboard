from flask import Flask, send_from_directory, request

app = Flask(__name__)


@app.route('/')
def frontend():
    # return "Hello"
    # return render_template('index.html')
    return send_from_directory('dist', 'index.html')


@app.route('/<text>.js')
def neco(text):
    return send_from_directory('dist', text+".js")


@app.route('/auth', methods=['POST'])
def auth():
    print(request.data)
    return 'parek',200


if __name__ == '__main__':
    app.run(port=3000)
