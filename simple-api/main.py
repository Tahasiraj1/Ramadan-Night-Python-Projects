from fastapi import FastAPI
import random


app = FastAPI()

side_hustles = [
    "Freelance Web Development",
    "Automating Tasks & Scripting",
    "Building and Selling APIs",
    "Data Analysis & Visualization",
    "AI & Machine Learning Projects",
    "Stock Market & Crypto Bots",
    "Web Scraping Services",
    "Selling Digital Products (Scripts, Tools)",
    "Teaching Python (Online Courses, YouTube)",
    "Writing Tech Blogs & Tutorials",
    "Building and Selling SaaS Applications",
    "Django/Flask Backend Development",
    "Creating Chatbots with AI",
    "Developing Chrome Extensions with Python",
    "Cybersecurity & Ethical Hacking",
    "Creating Python Plugins for Software",
    "Automating Excel & Google Sheets",
    "Building IoT Projects with Python",
    "Game Development with Pygame",
    "Developing AI-Powered Chatbots",
    "Creating and Selling Python Libraries",
    "E-commerce Automation (Scraping Prices, Bots)",
    "Contributing to Open Source (Can Get Sponsorships)",
    "Selling Python-Based No-Code Tools",
    "Developing API Integrations for Businesses",
    "NFT & Blockchain Development with Python",
    "Podcast Transcription Automation with AI",
    "Building Personal Finance or Budgeting Tools",
    "Creating a Resume Parsing Tool with NLP",
    "Social Media Automation (Twitter, Instagram Bots)"
]

motivational_quotes = [
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "Don't watch the clock; do what it does. Keep going. – Sam Levenson",
    "Opportunities don't happen. You create them. – Chris Grosser",
    "Do what you can, with what you have, where you are. – Theodore Roosevelt",
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "It always seems impossible until it’s done. – Nelson Mandela",
    "Success usually comes to those who are too busy to be looking for it. – Henry David Thoreau",
    "The way to get started is to quit talking and begin doing. – Walt Disney",
    "Hardships often prepare ordinary people for an extraordinary destiny. – C.S. Lewis",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Sometimes later becomes never. Do it now.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn’t just find you. You have to go out and get it.",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Don’t stop when you’re tired. Stop when you’re done.",
    "It’s going to be hard, but hard does not mean impossible.",
    "Dream bigger. Do bigger."
]

@app.get('/side_hustles')
async def get_hustles(apikey: str):
    if apikey != 'taha':
        return {'error': 'Invalid API key'}
    return {"side_hustle": random.choice(side_hustles)}

@app.get('/motivational_quotes')
async def get_motivational_quotes(apikey: str):
    if apikey != 'taha':
        return {'error': 'Invalid API key'}
    return {"motivational_quote": random.choice(motivational_quotes)}