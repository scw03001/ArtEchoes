'''
Page for the chatbot
'''
from flask import Blueprint, render_template_string, request
from googleVision import detect_web


path = './uploads/'


chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot/<filename>', methods=['GET', 'POST'])
def chatbot(filename=None):
    # This happens after the best_guesses and descriptions are extracted. When the user firstly visits the page,
    # it uses googleVision to extract best_guesses
    if request.method == 'POST':
        if request.form.get('correct') == 'yes':
            # start chatbot
            pass
        else:
            # ask the user to write the correct title
            pass
    else:
        # extract the best_guesses
        best_guesses, descriptions = detect_web(path + filename)

        return render_template_string('''
        <!doctype html>
        <html>
        <head>
            <title>Chatbot</title>
        </head>
        <body>
            This is the chatbot page. The filename is {{ filename }}<br>
            Best guesses: {{ best_guesses }}<br>
            Descriptions: {{ descriptions }}<br>
            <form method="post">
                Is this correct? <br>
                <input type="radio" name="correct" value="yes"> Yes<br>
                <input type="radio" name="correct" value="no"> No<br>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        ''', filename=filename, best_guesses=best_guesses, descriptions=descriptions)