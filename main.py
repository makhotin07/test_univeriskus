import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async def determine_mood(text: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Дай мне объективную оценку вопроса: '{text}'. "
                           f"Твоя задача - дать ясную и объективную оценку "
                           f"настроения вопроса. Если ты считаешь, что "
                           f"настроение вопроса позитивное и он является "
                           f"хорошим, ответь словом 'Хороший'. Если настроение "
                           f"вопроса негативное и он неудачный или не имеет "
                           f"четкой формулировки, ответь словом 'Плохой'."

            }
        ]
    )
    print(response.choices[0].message.content.lower())
    return response.choices[0].message.content.lower()



async def mood_request(text: str) -> str:
    mood = await determine_mood(text)
    if 'хороший' in mood:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Ответь на вопрос '{text}' как Бэтмен"
                }
            ]
        )
    else:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Ответь на вопрос '{text}' как Джокер"
                }
            ]
        )

    return response.choices[0].message.content.strip()


async def main():
    for i in range(10):
        user_input = input("Введите ваш запрос: ")
        response = await mood_request(user_input)
        print("Ответ GPT:", response)


asyncio.run(main())
