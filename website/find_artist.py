from flask import Blueprint, render_template_string

find_artist_bp = Blueprint('find_artist', __name__)

@find_artist_bp.route('/find_artist/<filename>')
def find_artist(filename=None):
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Find Artist</title>
    </head>
    <body>
        This is the find artist page. The filename is {{ filename }}
    </body>
    </html>
    ''', filename=filename)