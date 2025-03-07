from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

@app.route('/')
def index():
    # Check if max_number has been defined
    max_number = session.get('max_number')
    if max_number:
        message = session.get('message', f"")
    else:
        message = session.get('message', "Set a maximum number to start the game.")
    return render_template('index.html', message=message, game_over=session.get('game_over', False), max_number=max_number)

@app.route('/set_max', methods=['POST'])
def set_max():
    try:
        max_number = int(request.form.get('max_number'))
    except (TypeError, ValueError):
        session['message'] = "Please enter a valid maximum number!"
        return redirect(url_for('index'))

    if max_number <= 1:
        session['message'] = "Please enter a number greater than 1."
        return redirect(url_for('index'))

    session['max_number'] = max_number
    session['number'] = random.randint(1, max_number)
    session['attempts'] = 0
    session['game_over'] = False
    session['message'] = f"Let's Start!"
    return redirect(url_for('index'))

@app.route('/guess', methods=['POST'])
def guess():
    if 'max_number' not in session:
        session['message'] = "Please set the maximum number first!"
        return redirect(url_for('index'))

    try:
        user_guess = int(request.form.get('guess'))
    except (TypeError, ValueError):
        session['message'] = "Please enter a valid number!"
        return redirect(url_for('index'))

    session['attempts'] += 1
    target_number = session.get('number')
    max_number = session.get('max_number')

    if user_guess < target_number:
        session['message'] = "Higher!"
        session['game_over'] = False
    elif user_guess > target_number:
        session['message'] = "Lower!"
        session['game_over'] = False
    else:
        session['message'] = f"Correct! You guessed it ({target_number}) in {session['attempts']} attempts."
        session['game_over'] = True

    return redirect(url_for('index'))

@app.route('/new_game')
def new_game():
    # Clear all session variables including max_number
    session.pop('number', None)
    session.pop('attempts', None)
    session.pop('game_over', None)
    session.pop('message', None)
    session.pop('max_number', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
