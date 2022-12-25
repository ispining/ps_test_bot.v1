import datetime

import configurer
import texts
from config import *
import stg

sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_catlink(
ident_id TEXT PRIMARY KEY,
item_id TEXT,
cat_id TEXT
)""")
db.commit()


@bot.message_handler(commands=['admin'])
def start_command(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        if configurer.Lang(chat_id).get() in [None, "None"]:
            stg.set_lang(chat_id)
        else:
            stg.admin_panel(chat_id)


@bot.message_handler(content_types=['text'])
def glob_texts(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        stage = Stages(chat_id).get()
        if stage.split("||")[0] == "admin_set_new_item_name":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.item_name = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        elif stage.split("||")[0] == "admin_set_new_item_barcode":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.barcode = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        elif stage.split("||")[0] == "admin_set_new_item_firm":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.item_firm = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        elif stage.split("||")[0] == "admin_set_new_item_input_cost":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.input_cost = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        elif stage.split("||")[0] == "admin_set_new_item_output_cost":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.output_cost = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        elif stage.split("||")[0] == "admin_set_new_item_count":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.item_count = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        elif stage == "admin_add_category":
            cat_source = configurer.new_category_text(message.text)
            try:
                configurer.Categories(cat_id=str(cat_source["cat_id"]), ru=str(cat_source["ru"])).add()
            except:
                pass

            try:
                configurer.Categories(cat_id=str(cat_source["cat_id"]), he=str(cat_source["he"])).add()
            except:
                pass

            try:
                configurer.Categories(cat_id=str(cat_source["cat_id"]), en=str(cat_source["en"])).add()
            except:
                pass

            try:
                configurer.Categories(cat_id=str(cat_source["cat_id"]), ar=str(cat_source['ar'])).add()
            except:
                pass

            Stages(chat_id).set("None")
            stg.admin_items_add(chat_id)


@bot.message_handler(content_types=['photo'])
def glob_photo(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        stage = Stages(chat_id).get()
        if stage.split("||")[0] == "admin_set_new_item_picture":
            item_id = stage.split('||')[2]
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)

            filepath = f"sources/items_photo/{item_id}||{str(datetime.datetime.now()).split('.')[0]}.jpg"

            with open(filepath, 'wb') as new_file:
                new_file.write(downloaded_file)

            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.picture = filepath
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")
        elif stage.split("||")[0] == "admin_edit_item_picture":
            item_id = stage.split("||")[1]
            fileID = message.photo[-1].file_id

            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)
            filepath = f"sources/items_photo/{item_id}||{str(datetime.datetime.now()).split('.')[0]}.jpg"
            with open(filepath, 'wb') as new_file:
                new_file.write(downloaded_file)

            st = configurer.Stock()
            st.set(search_value=item_id, column="picture", value=filepath)

            send(chat_id, texts.get_text(chat_id, "new_value_setted_msg"), reply_markup=kmarkup().row(stg.back(chat_id, "admin_item")))


@bot.callback_query_handler(func=lambda m:True)
def glob_calls(call):
    chat_id = call.message.chat.id

    def dm():
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass

    call_category = call.data.split('_')
    cd = call.data.split("||")
    call_value = cd[0]

    if call.message.chat.type == "private":

        if call_value == "set_lang":
            configurer.Lang(chat_id).set(cd[1])

            stg.admin_panel(chat_id)
            dm()

        elif "admin" in call_value:

            # Admin home page
            if call_value == "admin":
                stg.admin_panel(chat_id)
                dm()

            # Admin items page
            elif call_value == "admin_item":
                stg.admin_items(chat_id)
                dm()

            # Admin item panel
            elif call_value == "admin_item_panel":
                item_id = cd[1]
                back_btn = cd[2]

                stg.admin_item_panel(chat_id, item_id, back_btn)
                dm()

            # Admin add item page
            elif call_value == "admin_items_add":
                stg.admin_items_add(chat_id)
                dm()

            # Admin add name for item
            elif call_value == "admin_add_item_panel":
                cat_id = cd[1]
                if len(cd) == 3:
                    stg.admin_add_item_panel(chat_id, cat_id, cd[2])
                else:
                    stg.admin_add_item_panel(chat_id, cat_id)
                dm()

            # Admin add category when add new item
            elif call_value == "admin_add_category":
                stg.admin_add_category(chat_id)
                dm()

            # item panel content
            elif "admin_set_new_item" in call_value:
                cat_id = cd[1]
                item_id = "None"
                if len(cd) == 3:
                    item_id = cd[2]

                if call_value == "admin_set_new_item_name":

                    stg.admin_set_new_item_name(chat_id, cat_id, item_id)
                    dm()

                elif call_value == "admin_set_new_item_picture":
                    stg.admin_set_new_item_picture(call, cat_id, item_id)
                    dm()

                elif call_value == "admin_set_new_item_firm":
                    stg.admin_set_new_item_firm(call, cat_id, item_id)
                    dm()

                elif call_value == "admin_set_new_item_barcode":
                    stg.admin_set_new_item_barcode(call, cat_id, item_id)
                    dm()

                elif call_value == "admin_set_new_item_input_cost":
                    stg.admin_set_new_item_input_cost(call, cat_id, item_id)
                    dm()

                elif call_value == "admin_set_new_item_output_cost":
                    stg.admin_set_new_item_output_cost(call, cat_id ,item_id)
                    dm()

                elif call_value == "admin_set_new_item_count":
                    stg.admin_set_new_item_count(call, cat_id, item_id)
                    dm()

                elif call_value == "admin_set_new_item_done":
                    tgi = configurer.TG_item_pre_add(cd[2])

                    if all((tgi.show()['item_name'] != "None", tgi.show()['item_firm'] != "None")):
                        tgi.send_to_main_db()
                        configurer.Catlinks(item_id=item_id, cat_id=cat_id, ident_id=configurer.Randomizer().lower_with_int()).add()

                        bot.answer_callback_query(call.id, texts.get_text(chat_id, "admin_set_new_item_done_call"), show_alert=True)
                        dm()
                        stg.admin_items(chat_id)

                    else:

                        bot.answer_callback_query(call.id, texts.get_text(chat_id, "admin_set_new_item_no_important_call"), show_alert=True)

            # remove item picture
            elif call_value == "admin_remove_item_picture":
                item_id = cd[1]
                stg.admin_remove_item_someshit(chat_id, item_id, 'picture')
                dm()

            # set item picture
            elif call_value == "admin_edit_item_picture":
                item_id = cd[1]
                stg.admin_edit_item_picture(chat_id, item_id)
                dm()

            # set item values
            elif "admin_item_panel_set" in call_value:
                item_id = cd[1]
                # set item name
                if call_value == "admin_item_panel_set_name":
                    stg.admin_item_panel_set(chat_id, item_id, set="name")
                    dm()
                # set item picture
                elif call_value == "admin_item_panel_set_item_picture":
                    stg.admin_item_panel_set(chat_id, item_id, set="picture")
                    dm()
                # set item firm
                elif call_value == "admin_item_panel_set_item_firm":
                    stg.admin_item_panel_set(chat_id, item_id, set="item_firm")
                    dm()
                # set item barcode
                elif call_value == "admin_item_panel_set_item_barcode":
                    stg.admin_item_panel_set(chat_id, item_id, set="barcode")
                    dm()
                # set item input cost
                elif call_value == "admin_item_panel_set_item_input_cost":
                    stg.admin_item_panel_set(chat_id, item_id, set="input_cost")
                    dm()
                # set item output cost
                elif call_value == "admin_item_panel_set_item_output_cost":
                    stg.admin_item_panel_set(chat_id, item_id, set="output_cost")
                    dm()
                # set item count
                elif call_value == "admin_item_panel_set_item_count":
                    stg.admin_item_panel_set(chat_id, item_id, set="item_count")
                    dm()
                # set item in stock
                elif call_value == "admin_item_panel_set_item_in_stock":
                    stg.admin_item_panel_set(chat_id, item_id, set="in_stock")
                    dm()
                # set item special files
                elif call_value == "admin_item_panel_set_item_special_files":
                    pass


            if "admin_find" in call_value:
                if call_value == "admin_find_by_category":
                    # Category list
                    if len(cd) == 1:
                        stg.admin_find_by_category(chat_id)
                        dm()

                    # Selected category
                    elif len(cd) == 2:
                        stg.admin_find_by_category(chat_id, cat_id=cd[1])
                        dm()

        # Agent back office
        elif call_category == "agent":
            #
            pass

        # Customer back office
        elif call_category == "customer":
            #
            pass



        else:
            send(chat_id, texts.get_text(chat_id, "in_Dev"))

bot.polling(timeout=10000)