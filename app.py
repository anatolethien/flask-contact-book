import os
import sqlite3
import re
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	email = db.Column(db.String)
	phone = db.Column(db.String)

@app.route('/')
def index():
	contact_list = Contact.query.all()
	return render_template('index.html', contact_list=contact_list)

@app.route('/new', methods=['GET', 'POST'])
def new():
	if request.method == 'GET':
		return render_template('new.html')
	elif request.method == 'POST':
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		email = request.form['email']
		phone = request.form['phone']
		try:
			db.session.add(Contact(
				first_name=first_name,
				last_name=last_name,
				email=email,
				phone=phone
			))
			db.session.commit()
			return redirect('/')
		except:
			raise
			return render_template('error.html', code='500', text='Internal Server Error')
	else:
		return render_template('error.html', code='405', text='Method Not Allowed')

@app.route('/contact/<int:id>')
def contact(id):
	contact = Contact.query.get(id)
	return render_template('contact.html', contact=contact)

@app.route('/contact/<int:id>/edit', methods=['GET', 'POST'])
def edit_contact(id):
	if request.method == 'GET':
		contact = Contact.query.get(id)
		return render_template('edit.html', contact=contact)
	elif request.method == 'POST':
		contact_to_edit = Contact.query.get(id)
		contact_to_edit.first_name = request.form['first_name']
		contact_to_edit.last_name = request.form['last_name']
		contact_to_edit.email = request.form['email']
		contact_to_edit.phone = request.form['phone']
		db.session.commit()
		return redirect(f'/contact/{id}')

@app.route('/contact/<int:id>/delete')
def delete_contact(id):
	contact_to_delete = Contact.query.get_or_404(id)
	db.session.delete(contact_to_delete)
	db.session.commit()
	return redirect('/')

@app.errorhandler(404)
def not_found(error):
	return render_template('error.html', code='404', text='Not Found')

@app.errorhandler(405)
def not_found(error):
	return render_template('error.html', code='405', text='Method Not Allowed')

@app.errorhandler(500)
def not_found(error):
	return render_template('error.html', code='500', text='Internal Server Error')

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True, host='0.0.0.0')
