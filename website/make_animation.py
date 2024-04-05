from flask import Blueprint, render_template_string, request

make_animation_bp = Blueprint('make_animation', __name__)

path = './uploads/'

@make_animation_bp.route('/make_animation/<filename>', methods=['GET', 'POST'])
def make_animation(filename=None):
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
        <title>Make Animation</title>
    </head>
    <body>
        This is the make animation page. The filename is {{ filename }}
    </body>
    </html>
    ''', filename=filename)