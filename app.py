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
    result = scratch.addPhoneNumberWith2FACode(phone_number, code)
    return jsonify({'Result': result})


@app.route('/removeNumber')
def removeNumber():
    phone_number = request.args.get('phone')
    result = scratch.removeNumber(phone_number)
    return jsonify({'Result': result})


@app.route('/betingelser')
def legal():
    return render_template('legal.html')


if __name__ == "__main__":
    app.run(debug=True)