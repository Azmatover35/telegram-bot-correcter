import openai
from aiogram import Bot, Dispatcher, executor, types

openai.api_key = 'YOUR_OPENAI_API_KEY'
bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
dp = Dispatcher(bot)
client = openai.OpenAI(api_key=openai.api_key)

user_modes = {}  # user_id: mode

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I can correct, translate, or teach. Use /mode to switch modes. Default is correcting.")

@dp.message_handler(commands=['mode'])
async def change_mode(message: types.Message):
    try:
        _, mode = message.text.split()
        if mode.lower() not in ['correct', 'translate', 'teach']:
            await message.reply("Invalid mode. Please choose between 'correct', 'translate', or 'teach'.")
            return
        user_modes[message.from_user.id] = mode.lower()
        await message.reply(f"Mode changed to {mode.lower()}.")
    except ValueError:
        await message.reply("Usage: /mode [correct/translate/teach]")

@dp.message_handler(commands=['translate'])
async def translate_text(message: types.Message):
   
    if user_modes.get(message.from_user.id) != 'translate':
        await message.reply("Switch to translate mode first using /mode translate.")
        return
    

@dp.message_handler()
async def handle_message(message: types.Message):
    mode = user_modes.get(message.from_user.id, 'correct')  
    if mode == 'correct':
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", 
                prompt=f"Correct the following text: {message.text}",
                temperature=0.5,
            )
            corrected_text = response['choices'][0]['text'].strip()
            await message.reply(corrected_text if corrected_text else "Sorry, I couldn't correct the text.")
        except Exception as e:
            await message.reply(f"An error occurred: {str(e)}")
    elif mode == 'translate':
    
        await message.reply("Please use the /translate command for translations.")
    elif mode == 'teach':
 
        await message.reply("Teaching mode is not implemented yet.")
    else:
        await message.reply("Unknown mode. Use /mode to set a correct mode.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
