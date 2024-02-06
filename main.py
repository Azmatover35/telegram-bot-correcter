import openai
from aiogram import Bot, Dispatcher, executor, types
openai.api_key = 'YOUR_OPENAI_API_KEY'
client = openai.OpenAI(api_key=openai.api_key)

bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! Send me some text, and I'll try to correct its mistakes.")

@dp.message_handler()
async def correct_text(message: types.Message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106", 
            prompt=f"Correct the following text: {message.text}",
            temperature=0.5,
        )
        corrected_text = response['choices'][0]['text'].strip()
        await message.reply(corrected_text if corrected_text else "Sorry, I couldn't correct the text.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
