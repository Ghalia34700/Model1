from openai import OpenAI
from django.conf import settings

class ContentClient():

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_APIKEY)

    def generate(self, prompt, system =None):

        messages=[]
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
        )
        print("response", response)
        return response.choices[0].message.content