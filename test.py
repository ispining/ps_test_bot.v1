import openai, csv
from pprint import pprint


class OpenAI:
    def get_code_response(self, question):
        openai.api_key = "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"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.5,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["|||"]

        )

        r = response["choices"][0]['text']
        r = r.replace("\n", "")
        return r.replace("\t", "")

# r = OpenAI().get_code_response("""Сайт Онлайн Магазин django + react""")
# pprint(r)

