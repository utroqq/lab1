import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from deep_translator import GoogleTranslator

API_TOKEN = "8718435549:AAELa86EgISzXjfuZbAWkJncV0Qxr41GSMk"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def translate_to_en(text):
    return GoogleTranslator(source='ru', target='en').translate(text)

def translate_to_ru(text):
    return GoogleTranslator(source='en', target='ru').translate(text)

def get_recipe(ingredient_en):
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient_en}"
    data = requests.get(url).json()

    if not data["meals"]:
        return "😕 Рецептов по этому ингредиенту не найдено"

    meal = data["meals"][0]
    meal_id = meal["idMeal"]

    url2 = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    data2 = requests.get(url2).json()

    meal_info = data2["meals"][0]

    name_ru = translate_to_ru(meal_info["strMeal"])
    instr_ru = translate_to_ru(meal_info["strInstructions"])

    return f"""
🍽 Блюдо: {name_ru}

📖 Рецепт:
{instr_ru}
"""

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Напиши ингредиенты на русском 🍲\n"
        "Например: курица, рис"
    )

@dp.message_handler()
async def handle(message: types.Message):

    text = message.text.split(",")[0].strip()

    ingredient_en = translate_to_en(text)

    result = get_recipe(ingredient_en)

    await message.answer(result)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)