import base64
from openai import OpenAI

# https://platform.openai.com/docs/guides/vision
# Further Prompt Engineering might be required. Sometimes API refuses to provide names (for safety reason supposedly). 


# Replace 'your_api_key' with your actual OpenAI API key
API_KEY = 'your_api_key'

# Initializing the OpenAI client with the provided API key
client = OpenAI(api_key=API_KEY)

def encode_image_to_base64(image_path):
    """
    Converts an image file to a base64-encoded string.
    
    Args:
        image_path (str): The file path of the image to encode.
        
    Returns:
        str: The base64-encoded string of the image.
    """
    # Open the image file in binary-read mode and encode it to base64
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def create_completion_request(image_path=None, image_url=None):
    """
    Creates a request for an AI completion, optionally including an image.
    
    Args:
        image_path (str): Path to a local image file.
        image_url (str): URL to an image.
        
    Returns:
        object: The response object from the OpenAI API.
    """
    # Initialize the message for the request
    messages = [{
        "role": "user",
        "content": [{"type": "text", "text": "Reply in the following format: [Artist, Artwork]"}],
    }]

    # If a local image path is provided, encode it and add to the request
    if image_path:
        encoded_image = encode_image_to_base64(image_path)
        messages[0]['content'].append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
        })
    # If an image URL is provided, directly add it to the request
    elif image_url:
        messages[0]['content'].append({
            "type": "image_url",
            "image_url": {"url": image_url}
        })

    # Send the request to the OpenAI API and receive the response
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=300
    )

    # Return the first choice from the response
    return response.choices[0]


# Example usage of the function with a local image
print(create_completion_request(image_path="mona.png"))

# Example usage of the function with an image URL
# print(create_completion_request(image_url="https://img.etimg.com/thumb/msid-83663367,width-650,height-488,imgsize-866221,resizemode-75/this-copy-is-known-as-the-hekking-mona-lisa-.jpg"))
