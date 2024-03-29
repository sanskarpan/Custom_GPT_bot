# Custom GPT Bot

This is a simple chat interface powered by OpenAI's GPT-3.5 model. Users can interact with the AI by typing messages into the text input field, and the AI will respond accordingly based on the conversation history.

## Features

**Customizable:** Users can set their names for a personalized experience.

**Persistent Conversations:** Conversation history is stored for each user.

**Easy-to-Use Interface:** Simple and intuitive design for smooth interaction.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install openai, dotenv and gradio.

**openai**-> For running the API that will connect user to GPT model;

**dotenv**-> To use your api_key that will be securely stored in a .env file;

**gradio**-> Used in this project to create a simple web-based GUI.


```bash
pip install openai python--dotenv gradio
```
OR you can directly run following command in your terminal which contain all dependencies.

```bash
pip install -r requirements.txt
```

## Usage
Obtain an API key from OpenAI and store it in a .env file as api_key=YOUR_API_KEY. Then import all the desired libraries. 

```python
import openai 
import gradio as gr 
import os # used for getenv() to load api_key
import json # used to read and write user profiles in .json file
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('api_key')
```
Further utility functions are created for loading and saving user profiles stored in a JSON file. The **load_user_profiles** function reads the JSON file at the specified file_path and returns the loaded data. 


The **save_user_profiles function** writes the user_profiles dictionary to the JSON file at the specified file_path, formatting it with an indentation of 4 spaces for better readability.

```python
def load_user_profiles(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_user_profiles(file_path, user_profiles):
    with open(file_path, 'w') as file:
        json.dump(user_profiles, file, indent=4)

user_profiles_file = "user_profiles.json"
user_profiles = load_user_profiles(user_profiles_file)
messages = []
```

Next,a function CustomChatGPT, is created which would be responsible for handling user interactions with the chatbot. It first checks if the user ID is present in the user_profiles dictionary. If not, it initializes a new user profile with default values such as an empty name, an empty list of conversations, empty preferences, and an empty resume history.

If the user profile does not have a name set (user_profile["name"]), it sets the user's input as their name and returns a greeting message welcoming the user by their name.

Otherwise, it appends the user's input to the conversation history in the user's profile and adds the input to the global messages list. This messages list keeps track of all conversations, including both user inputs and responses from the chatbot.

```python
def CustomChatGPT(user_input, user_id):
    if user_id not in user_profiles:
        user_profiles[user_id] = {"name": "", "conversations": [], "preferences": {}, "resume_history": []}
    user_profile = user_profiles[user_id]

    if not user_profile["name"]:
        user_profile["name"] = user_input
        return f"Hello {user_input}, how can I assist you today?"

    user_profile["conversations"].append({"role": user_profile["name"], "content": user_input})
    messages.append({"role": user_profile["name"], "content": user_input})
```

now, use OpenAI's Chat Completion API to generate a response from the chatbot model based on the messages exchanged so far. The response is extracted from the API's JSON output. The generated reply is then added to the user's conversation history in their profile and appended to the global messages list. Finally, the updated user profiles are saved to a JSON file, and the reply is returned.
```python

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response["choices"][0]["message"]["content"]

    user_profile["conversations"].append({"role": "assistant", "content": reply})
    messages.append({"role": "assistant", "content": reply})
    save_user_profiles(user_profiles_file, user_profiles)
    return reply
```
Finally, initialize Gradio interface using the CustomChatGPT function as the backend, taking text input and producing text output. The title of the interface is set to **Custom GPT**. By calling __demo.launch(share=True)__, the interface is launched,making the chatbot accessible via a web-based GUI.
```python
demo = gr.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Custom GPT")
demo.launch(share=True)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
