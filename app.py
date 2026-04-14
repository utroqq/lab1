from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'secret123'  # нужно для хранения ответа

def generate_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    session['answer'] = a + b
    return f"{a} + {b}"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""

    if request.method == 'POST':
        user_answer = request.form.get('captcha')

        if user_answer and int(user_answer) == session.get('answer'):
            message = "Ты не робот ✅"
        else:
            message = "Неправильно ❌"

    captcha = generate_captcha()
    return render_template('index.html', captcha=captcha, message=message)

if __name__ == '__main__':
    app.run(debug=True)

#http://127.0.0.1:5000