import chainlit as cl
from dotenv import load_dotenv
import google.generativeai as genai
import os
from typing import Optional

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token: str,
  raw_user_data: dict[str, str],
  default_user: cl.User,
) -> Optional[cl.User]:   
    print(f"Provider: {provider_id}") 
    print(f"User data: {raw_user_data}")
    return default_user

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set('history', [])
    

@cl.on_message
async def handle_message(message: cl.Message):
    
    history = cl.user_session.get('history')
    
    history.append({'role': 'user', 'content': message.content})
    
    formated_history = []
    for msg in history:
        role = 'user' if msg['role'] == 'user' else 'assistant'
        formated_history.append({'role': role, 'parts': [{'text': msg['content']}]})
        
    
    response = model.generate_content(formated_history)
    
    response_text = response.text if hasattr(response, 'text') else 'Sorry, I am not sure how to help with that.'
    
    history.append({'role': 'assistant', 'content': response_text})
    cl.user_session.set('history', history)
    await cl.Message(content=response_text).send()
                            
                                


