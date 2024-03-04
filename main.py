from flask import Flask, render_template, request
import requests
import smtplib
from smtplib import SMTPException
import os
from datetime import datetime

url = "https://api.npoint.io/674f5423f73deab1e9a7"

EMAIL = os.getenv("my_email")
PASSWORD = os.getenv("my_password")
app = Flask(__name__)
today = datetime.now().strftime("%B %d, %Y")
posts = requests.get(url=url).json()


def send_email(name, email, phone, message):
	mail_to_send = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
	with smtplib.SMTP("smtp.gmail.com") as connection:
		connection.starttls()
		connection.login(user=EMAIL, password=PASSWORD)
		msg = f"Subject: New Message\n\n{mail_to_send}"
		connection.sendmail(
			from_addr=email,
			to_addrs=EMAIL,
			msg=msg.encode("utf-8")
		)


@app.route("/")
def home():
	return render_template("index.html", posts=posts, today=today)


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/contact", methods=["GET","POST"])
def contact():
	if request.method == 'GET':
		notify = False
		return render_template("contact.html", notify=notify)
	else:
		name = request.form["name"]
		email = request.form["email"]
		phone_number = request.form["phone number"]
		message = request.form["message"]
		try:
			send_email(name,email,phone_number,message)
		except SMTPException:
			notify = True
			notification = "Error sending email message! Sending failed."
			return render_template("contact.html", notify=notify, notification=notification)
		notify = True
		notification = "Successfully sent your message!"
		return render_template("contact.html", notify=notify, notification=notification)


@app.route("/post/<int:num>")
def post(num):
	the_post = posts[num]
	day = today
	return render_template("post.html", the_post=the_post, day=day)


if __name__ == "__main__":
	app.run(debug=True)
