
from dotenv import load_dotenv
from openai import OpenAI
from .logger_configuration import logger

load_dotenv()
client = OpenAI()

def call_api(system_prompt,
             user_prompt, temp=0.2, 
             json_mode=False):
    try:
        response_format = {"type": "json_object"} if json_mode else {"type": "text"}
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temp,
            response_format=response_format
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error en API: {e}")
        return None
