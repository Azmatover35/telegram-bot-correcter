import openai
from aiogram import Bot, Dispatcher, executor, types


openai.api_key = 'YOUR_OPENAI_API_KEY'
bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
dp = Dispatcher(bot)
client = openai.OpenAI(api_key=openai.api_key)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! Send me some text, and I'll try to correct its mistakes. Use /translate to translate text.")

@dp.message_handler(commands=['translate'])
async def translate_text(message: types.Message):

    try:
        _, src_lang, tgt_lang, *text_parts = message.text.split(maxsplit=3)
        text_to_translate = " ".join(text_parts) if text_parts else ""
        if not text_to_translate: 
            await message.reply("Please provide the text to translate after the command, e.g., `/translate en fr Hello World`.")
            return
        

        prompt = f"Translate the following text from {src_lang} to {tgt_lang}: {text_to_translate}"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            prompt=prompt,
            temperature=0.5,
        )
        translated_text = response['choices'][0]['text'].strip()
        await message.reply(translated_text if translated_text else "Sorry, I couldn't translate the text.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

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
