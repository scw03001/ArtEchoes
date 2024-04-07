from flask import Blueprint, render_template_string, request

make_animation_bp = Blueprint('make_animation', __name__)

path = './uploads/'

@make_animation_bp.route('/make_animation/<filename>', methods=['GET', 'POST'])
def make_animation(filename=None):
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