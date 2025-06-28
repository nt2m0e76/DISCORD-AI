import discord
import openai
from config import DISCORD_BOT_TOKEN, GEMMA_API_KEY
from config import TEMPERATURE, TOP_P, MAX_TOKENS, FREQUENCY_PENALTY, PRESENCE_PENALTY, PERSONA_SHAPE
print("Dang khoi tao bot...")
print("Discord Bot Token", DISCORD_BOT_TOKEN[:8], "...")
print("GEMMA API Key:", GEMMA_API_KEY[:8], "...")

# Khởi tạo intents
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Lưu lịch sử theo user
chat_history = {}

# Khởi tạo OpenAI client (AIMLAPI)
try:
    openai_client = openai.OpenAI(
        base_url="https://api.aimlapi.com/v1",
        api_key=GEMMA_API_KEY
    )
    print("O / openai_client khoi tao xong")
except Exception as e:
    print("X / Loi tao openai_client:", e)

@bot.event
async def on_ready():
    print(f"O / Bot da online duoi ten: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Nhận nếu tag bot hoặc trả lời bot
    if bot.user in message.mentions or (
        message.reference and
        hasattr(message.reference, "resolved") and
        message.reference.resolved and
        message.reference.resolved.author == bot.user
    ):
        user_id = str(message.author.id)
        prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()

        if user_id not in chat_history:
            chat_history[user_id] = []

        # Thêm câu hỏi user vào history
        chat_history[user_id].append({"role": "user", "content": prompt})
        full_messages = [PERSONA_SHAPE] + chat_history[user_id]

        try:
            await message.channel.typing()
            completion = openai_client.chat.completions.create(
                model="google/gemma-3-27b-it",
                messages=full_messages,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_tokens=MAX_TOKENS,
                frequency_penalty=FREQUENCY_PENALTY,
                presence_penalty=PRESENCE_PENALTY
            )
            reply = completion.choices[0].message.content.strip()
            chat_history[user_id].append({"role": "assistant", "content": reply})
            await message.reply(reply[:2000])
            
        except Exception as e:
            print("Loi khi goi API:", e)
            await message.reply("Loi khi goi AI")

bot.run(DISCORD_BOT_TOKEN)
