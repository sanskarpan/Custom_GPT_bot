import openai
import gradio as gr
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('api_key')

def load_user_profiles(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_user_profiles(file_path, user_profiles):
    with open(file_path, 'w') as file:
        json.dump(user_profiles, file, indent=4)

user_profiles_file = "user_profiles.json"
user_profiles = load_user_profiles(user_profiles_file)
messages = []

def CustomChatGPT(user_input, user_id):
    if user_id not in user_profiles:
        user_profiles[user_id] = {"name": "", "conversations": [], "preferences": {}, "resume_history": []}
    user_profile = user_profiles[user_id]

    if not user_profile["name"]:
        user_profile["name"] = user_input
        return f"Hello {user_input}, how can I assist you today?"

    user_profile["conversations"].append({"role": user_profile["name"], "content": user_input})
    messages.append({"role": user_profile["name"], "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response["choices"][0]["message"]["content"]

    user_profile["conversations"].append({"role": "assistant", "content": reply})
    messages.append({"role": "assistant", "content": reply})
    save_user_profiles(user_profiles_file, user_profiles)
    return reply

demo = gr.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Custom GPT")
demo.launch(share=True)
