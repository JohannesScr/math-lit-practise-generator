import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_mail import Mail, Message
from math_lit import generate_template, generate_data, generate_pdf

load_dotenv()
logging.basicConfig(level=logging.DEBUG)


class Config(object):
	HOST = '127.0.0.1'
	PORT = 5000
	DEBUG = True
	TEST = 0
	ENV = 'development'

	MAIL_SERVER = os.getenv('MAIL_SERVER')
	MAIL_PORT = int(os.getenv('MAIL_PORT'))
	MAIL_USE_TLS = bool(int(os.getenv('MAIL_USE_TLS')))
	MAIL_USE_SSL = bool(int(os.getenv('MAIL_USE_SSL')))
	MAIL_USERNAME = os.getenv('MAIL_USERNAME')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


log = logging.getLogger(__name__)
mail = Mail()

app = Flask(__name__)
app.config.from_object(Config)

mail.init_app(app)


@app.route('/', methods=['POST'])
def hello_world():
	log.info(request.json)
	return jsonify(message='Welcome to the Math Lit Generator Service')


@app.route('/', methods=['GET'])
def create_template():
	data = generate_data()
	tex_string = generate_template(template='math_lit', data=data)
	filename, pdf_bytes = generate_pdf(tex_string=tex_string)

	msg = Message()
	msg.recipients = ['anelisa.dul@gmail.com']
	msg.sender = ('No Reply', 'no-reply@gmail.com')
	msg.body = 'hello there'
	msg.html = '<b>Hello There</b>'
	msg.subject = 'Mathematics Literacy Practise'
	msg.attach(filename, 'application/pdf', pdf_bytes)
	mail.send(msg)
	return jsonify(message='Created template successfully')


if __name__ == '__main__':
	app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)