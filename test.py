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


def item_csv_to_binary(filename):
    with open(filename, "r") as file:
        result = []
        csv_file = csv.reader(file, delimiter=',')
        for row in csv_file:
            ident_id = row[0]
            item_type = row[1]
            barcode = row[2]
            item_name = row[3]
            description = row[4]
            about = row[5]
            cost1 = row[6]
            cost2 = row[7]
            cost3 = row[8]
            category = row[9]
            undercat = row[10]
            delivery_type = row[11]
            photo = row[12]
            var1 = row[13]
            var1_action = row[14]

            result.append({
                "ident_id": ident_id,
                "item_type": item_type,
                "barcode": barcode,
                "item_name": item_name,
                "description": description,
                "about": about,
                "cost1": cost1,
                "cost2": cost2,
                "cost3": cost3,
                "category": category,
                "undercat": undercat,
                "delivery_type": delivery_type,
                "photo": photo,
                "var1": var1,
                "var1_action": var1_action
            })
        return result

pprint(item_csv_to_binary("stock.csv"))