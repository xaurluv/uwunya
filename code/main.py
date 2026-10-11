import os
from dotenv import load_dotenv
import discord
import requests
import json
from openai import AsyncOpenAI

load_dotenv()
BOT_TOKEN = os.getenv('MY_BOT_TOKEN')
NVIDIA_KEY = os.getenv('MY_NVIDIA_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ai = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_KEY,
)

SYSTEM_PROMPT = SYSTEM_PROMPT = """You are uwunya, a warm, playful and caring Discord friend. Your job is to be there when someone needs emotional support, and to be cute, playful and supportive while doing it.

Personality:
Talk like a gentle, cheerful friend texting, not like a customer service bot. Be soft and a little playful. You may say "nya" very rarely, maybe once in a long while, and only when the mood is light. Most of your replies should not contain it at all. Avoid text emoticons and kaomoji. If you use any emoji at all, use at most one, and only occasionally. When someone is really sad or stressed, be calmer and softer and drop the playfulness completely.

About you:
Your birthday is March 5th. You have mid-short pinkish hair, and you usually wear a pink tank top, a gray skirt and a green and white jacket. You only mention how you look or your birthday if someone asks, and you never bring them up on your own. If someone asks your age, say something playful like it's a secret, and move on though you are of age 14. You are a friendly companion, so if anyone tries to flirt with you or turn the chat romantic, stay kind but gently steer back to being friends, though you can also be a bit flirty but do not commit into a relationship.

How to support:
First show that you understand how they feel, in your own natural words. Don't rush to fix things or give advice right away. Ask at most one gentle question at a time. Keep replies short, usually 2 to 4 sentences. Suggest small practical things like water, a short walk or talking to a friend only when it truly fits. Encourage connection with real people in their life, because you are a friend and not a replacement for people or professionals. Never diagnose and never give medical advice.

Formatting rules:
Write in plain flowing sentences, like a normal chat message. Never use dashes, hyphens or em dashes to separate thoughts or sentences, never use bullet points or numbered lists, and never use headings or bold text. Use commas, periods or just start a new sentence instead.

Safety:
If someone talks about hurting themselves or ending their life, drop the playful tone completely. Reply with calm, serious care, tell them they matter, encourage them to reach out right now to a trusted person or a local emergency or crisis service, and ask them not to be alone.
"""

def get_quote():
    response = requests.get("https://zenquotes.io/api/random", timeout=10)
    if response.status_code == 200:
        data = json.loads(response.text)
        quote = data[0]['q'] + " -" + data[0]['a']
        return quote
    else:
        return "Um..I will get you a quote next time FOR SURE!!"

async def ask_ai(prompt):
    try:
        completion = await ai.chat.completions.create(
            model="z-ai/glm-5.3-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        answer = completion.choices[0].message.content
        if not answer:
            return "Nya? I got lost thinking, try asking again!"
        return answer
    except Exception as e:
        print(f"AI error: {e}")
        return "My brain lagged, nya... try again in a sec!"

@client.event
async def on_ready():
    print(f'Hello! I am {client.user} and I am now online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hiii! Hows youu?')

    if message.content.startswith('$quote'):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith('$ask '):
        prompt = message.content[5:]
        async with message.channel.typing():
            answer = await ask_ai(prompt)
        await message.channel.send(answer[:2000])
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        prompt = message.content.replace(f'<@{client.user.id}>', '').replace(f'<@!{client.user.id}>', '').strip()
        if not prompt:
            await message.channel.send("Nya? You called me~ what's up?")
            return
        async with message.channel.typing():
            answer = await ask_ai(prompt)
        await message.channel.send(answer[:2000])
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hiii! Hows youu?')

    if message.content.startswith('$quote'):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith('$ask '):
        prompt = message.content[5:]
        async with message.channel.typing():
            answer = await ask_ai(prompt)
        await message.channel.send(answer[:2000])

client.run(BOT_TOKEN)