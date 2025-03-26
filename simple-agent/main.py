from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, trace
from bs4 import BeautifulSoup
import chainlit as cl
from dotenv import load_dotenv
from IPython.display import display, Markdown
import os
from menu import MENU_PRICES
import requests
from typing import Optional


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@function_tool
async def get_weather(city: str) -> str:
    url = f"{WEATHER_BASE_URL}?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        condition = data['weather'][0]['main']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        weather_report = (
            f"🌍 Weather in {city.capitalize()}\n"
            f"🌡 Temperature: {temperature}°C\n"
            f"🌤 Condition: {condition}\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind Speed: {wind_speed} m/s"
        )

        return weather_report
    
    else:
        return "❌ Error: City not found or API request failed!"

@function_tool
def fetch_portfolio_data() -> dict:
    """Fetches details from the given portfolio website URL."""
    url = "https://my-portfolio-eta-one-97.vercel.app/"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Failed to fetch portfolio. Status Code: {response.status_code}"
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract key information
    name = soup.find("h1").text if soup.find("h1") else "Name not found"
    bio = soup.find("p").text if soup.find("p") else "Bio not found"
    about = soup.find(id="about").text if soup.find(id="about") else "About not found"
    projects = soup.find(id="projects").text if soup.find(id="projects") else "Projects not found"
    skills = soup.find(id="skills").text if soup.find(id="skills") else "Skills not found"
    
    return {"name": name, "bio": bio, "about": about, "projects": projects, "skills": skills}

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=provider,
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model=model,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    model=model,
)

weather_agent = Agent(
    name="Weather agent",
    instructions="If the user asks for weather report for a city, provide the weather report, by using the get_weather tool, user will likey say something like: What's the weather like in New York? and the agent will respond with the weather report for New York, similarly if the user asks for the weather report in London, the agent will respond with the weather report for London, And so on.",
    model=model,
    tools=[get_weather],
)

cashier_agent = Agent(
    name="Cashier",
    instructions=f"You are a helpful server at a Burger restuarant respond to questions based on the menu below: \n\n{MENU_PRICES}, if the customer ask for the price first quote the price without taxes then add the tax to the total price. Also you have to be able to persued the customer to buy more items, by suggesting other items from the menu. Also if customer provide his/her name call him by his name",
    model=model,
)

personal_agent = Agent(
    name="Personal Assistant",
    instructions="You are my personal agent, you will answer questions about me, my skills, my interests, my hobbies, etc. You will try to answer and deliver the best answers about me to the user, by using the fetch_portfolio_data tool, user will likey say something like: What's my name? and the agent will respond with the name of the portfolio, similarly if the user asks for the bio of the portfolio, the agent will respond with the bio of the portfolio, And so on.",
    model=model,
    tools=[fetch_portfolio_data],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=f"You determine which agent to use based on the user's query. If the user is asking about me i.e 'Taha Siraj' then you should use the personal agent. If the user is asking about the weather, then you should use the weather agent. If the user is asking about the history related stuff, then you should use the history tutor agent. If the user is asking about math related stuff, then you should use the math tutor agent. If the user is asking about the food menu or the price of an item from the menu below: {MENU_PRICES}, then you should use the cashier agent. And if the user ask anything other then the above mentioned queries, then you should respond with 'I am sorry, I'm an AI Agent with: mention you capabilites'.",
    handoffs=[history_tutor_agent, math_tutor_agent, weather_agent, cashier_agent, personal_agent],
    model=model,
)

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
    await cl.Message(content="Welcome to the Triage Agent, I will help you with your queries, regarding my developer: 'Taha Siraj', Ask me anything about him, his skills, and his work. Further I can help you with: history lessons, math lessobs, live weather forecast, and our delicious food menu.").send()
    

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get('history')
    history.append({'role': 'user', 'content': message.content})
    
    formated_history = []
    for msg in history:
        role = 'user' if msg['role'] == 'user' else 'assistant'
        formated_history.append({'role': role, 'parts': [{'text': msg['content']}]})
    
    response = await cl.make_async(Runner.run_sync)(triage_agent, message.content)
    response_text = response.final_output
    await cl.Message(content=response_text).send()
    history.append({'role': 'assistant', 'content': response_text})

    
    cl.user_session.set('history', history)