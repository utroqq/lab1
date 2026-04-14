from flask import Flask, render_template, request, session, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


def new_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    session["answer"] = a + b
    session["captcha_text"] = f"{a} + {b}"


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        user_answer = request.form.get("captcha")

        if user_answer and session.get("answer") is not None:
            if int(user_answer) == session["answer"]:
                return redirect(url_for('success'))
            else:
                message = "Неправильно"

        new_captcha()

    if "answer" not in session:
        new_captcha()

    return render_template(
        "index.html",
        captcha=session["captcha_text"],
        message=message
    )


@app.route("/success")
def success():
    return redirect("https://google.com")


if __name__ == "__main__":
    app.run(debug=True)

#http://127.0.0.1:5000