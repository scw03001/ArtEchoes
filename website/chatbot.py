from flask import Blueprint, render_template_string, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
import os

# Assuming detect_web is a function from googleVision.detectWeb that returns best_guesses and descriptions
# from googleVision.detectWeb import detect_web


load_dotenv()
chatbot_api = os.getenv('chatbot_api')

path = './uploads/'

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot/<filename>', methods=['GET', 'POST'])
def chatbot(filename=None):
    if request.method == 'POST':
        if request.form.get('correct') == 'yes':
            artwork_info = session.get('best_guesses', '')
        elif request.form.get('correct') == 'no' and request.form.get('correct_title'):
            # Process the correct title as needed
            artwork_info = request.form.get('correct_title')
        session['artwork_info'] = artwork_info
        return redirect(url_for('chatbot.chat_feature'))
    else:
        # Use Google Vision API to get the best_guesses and descriptions
        # best_guesses, descriptions = detect_web(path + filename)
        best_guesses = "The Starry Night"  # Placeholder for demonstration
        descriptions = "Example Descriptions"  # Placeholder for demonstration

        session['best_guesses'] = best_guesses 
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
                <input type="radio" name="correct" value="yes" id="yes"> Yes<br>
                <input type="radio" name="correct" value="no" id="no"> No<br>
                <div id="correct_title_input" style="display:none;">
                    Correct title: <input type="text" name="correct_title"><br>
                </div>
                <input type="submit" value="Submit">
            </form>
            <script>
                document.getElementById('no').onchange = function() {
                    document.getElementById('correct_title_input').style.display = 'block';
                };
                document.getElementById('yes').onchange = function() {
                    document.getElementById('correct_title_input').style.display = 'none';
                };
            </script>
        </body>
        </html>
        ''', filename=filename, best_guesses=best_guesses, descriptions=descriptions)


from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=chatbot_api,
)

# @chatbot_bp.route('/chat_feature', methods=['GET', 'POST'])
# def chat_feature():
#     # 세션에서 artwork_info 검색
#     artwork_info = session.get('artwork_info')
    
#     if request.method == 'POST':
#         user_message = request.form['message']
#         # OpenAI API를 사용하여 챗봇 응답 생성
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": f"This is a conversation about an artwork: {artwork_info}."},
#                 {"role": "user", "content": user_message}
#             ]
#         )
#         return jsonify({'response':response.choices[0].message.content})
#     else:
#         return render_template_string('''
#         <!doctype html>
#         <html>
#         <head>
#             <title>Chat Feature</title>
#         </head>
#         <body>
#             <h2>Discussing: {{ artwork_info }}</h2>
#             <form action="" method="post">
#                 <input type="text" name="message" placeholder="Your message" />
#                 <input type="submit" />
#             </form>
#         </body>
#         </html>
#         ''', artwork_info=artwork_info)


# Endpoint for getting session artwork
@chatbot_bp.route('/chat_artwork', methods=['GET'])
def get_artwork():
    print("Session keys:", session.keys())
    artwork_info = session.get('best_guesses', 'Server: No artwork info available')

    return {'artwork': artwork_info}


# Endpoint for saving/updating the artwork piece in the session
@chatbot_bp.route('/chatbot/<filename>', methods=['GET', 'POST'])
def chatbot2(filename=None):
    if request.method == 'POST':
        if request.form.get('correct') == 'yes':
            artwork_info = session.get('best_guesses', '')
        elif request.form.get('correct') == 'no' and request.form.get('correct_title'):
            # Process the correct title as needed
            artwork_info = request.form.get('correct_title')
        session['artwork_info'] = artwork_info
        return redirect(url_for('chatbot.chat_feature'))
    else:
        # Use Google Vision API to get the best_guesses and descriptions
        # best_guesses, descriptions = detect_web(path + filename)
        best_guesses = "The Starry Night"  # Placeholder for demonstration
        descriptions = "Example Descriptions"  # Placeholder for demonstration

        session['best_guesses'] = best_guesses 


@chatbot_bp.route('/chat_feature', methods=['GET', 'POST'])
def chat_feature():
    # Assuming 'artwork_info' is stored in the session
    artwork_info = session.get('artwork_info', 'No artwork info available')
    
    if request.method == 'POST':
        user_message = request.json.get('message', '')
        # Generate chatbot response using OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"This is a conversation about an artwork: {artwork_info}."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({'response': response.choices[0].message.content})
        
    # For GET request, simply return the chat interface
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Chat Feature</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script>
            $(document).ready(function(){
                $('form').submit(function(event){
                    event.preventDefault();  // Prevent form from reloading the page
                    $.ajax({
                        type: 'POST',
                        url: '/chat_feature',
                        contentType: 'application/json',
                        data: JSON.stringify({'message': $('input[name="message"]').val()}),
                        success: function(response) {
                            $('#chat').append('<p>You: ' + $('input[name="message"]').val() + '</p>');
                            $('#chat').append('<p>Bot: ' + response.response + '</p>');
                            $('input[name="message"]').val('');  // Clear input field
                        }
                    });
                });
            });
        </script>
    </head>
    <body>
        <h2>Discussing: {{ artwork_info }}</h2>
        <div id="chat"></div>
        <form action="" method="post">
            <input type="text" name="message" placeholder="Your message" />
            <input type="submit" value="Send" />
        </form>
    </body>
    </html>
    ''', artwork_info =  artwork_info)