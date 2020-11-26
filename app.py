from flask import Flask, render_template, jsonify, request
import scratch

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/2fa')
def do2FA():
    print(request.args.get('phone'))
    result = scratch.do2FA(str(request.args.get('phone')))
    return jsonify(result)


@app.route('/addNumber')
def addNumber():
    phone_number = request.args.get('phone')
    code = request.args.get('code')
    scratch.addPhoneNumberWith2FACode(phone_number, code)
    return jsonify({"test": "yes"})


if __name__ == "__main__":
    app.run(debug=True)