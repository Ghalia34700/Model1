from openai import OpenAI
from django.conf import settings

class ContentClient():
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_APIKEY)

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content