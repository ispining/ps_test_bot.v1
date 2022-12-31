import datetime
import os, asyncio

import configurer
import texts
from config import *
import stg


@bot.message_handler(commands=['admin'])
def admin_command(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        s = configurer.Staff(str(chat_id))

        if s.get() != None:
            if configurer.Staff(str(chat_id)).get()['status'] == "admin":
                if configurer.Lang(chat_id).get() in [None, "None"]:
                    stg.set_lang(chat_id, 'admin')
                else:
                    stg.admin_panel(chat_id)


@bot.message_handler(commands=['agent'])
def agent_command(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        if configurer.Lang(chat_id).get() in [None, "None"]:
            stg.set_lang(chat_id, "agent")
        else:
            stg.agent_panel(chat_id)


@bot.message_handler(commands=['start'])
def customer_command(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        if configurer.Lang(chat_id).get() in [None, "None"]:
            stg.set_lang(chat_id, "customer")
        else:
            stg.customer_panel(chat_id)


@bot.message_handler(content_types=['text'])
def glob_texts(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        stage = Stages(chat_id).get()

        # set name for new item
        if stage.split("||")[0] == "admin_set_new_item_name":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.item_name = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        # set barcode for new item
        elif stage.split("||")[0] == "admin_set_new_item_barcode":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.barcode = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        # set firm for new item
        elif stage.split("||")[0] == "admin_set_new_item_firm":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.item_firm = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        # set input cost for new item
        elif stage.split("||")[0] == "admin_set_new_item_input_cost":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.input_cost = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        # set output for new item
        elif stage.split("||")[0] == "admin_set_new_item_output_cost":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.output_cost = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        # set count for new item
        elif stage.split("||")[0] == "admin_set_new_item_count":
            ctg = configurer.TG_item_pre_add()
            ctg.item_id = stage.split("||")[2]
            ctg.item_count = message.text
            ctg.add()
            stg.admin_add_item_panel(chat_id, stage.split("||")[1], stage.split("||")[2])
            Stages(chat_id).set("None")

        # add new category
        elif stage.split('||')[0] == "admin_add_category":
            cat_source = configurer.new_category_text(message.text)
            unknown = True
            try:
                configurer.Categories(cat_id=str(cat_source["cat_id"]), ru=str(cat_source["ru"])).add()
                unknown = False
            except:
                pass

            try:
                configurer.Categories(cat_id=str(cat_source["cat_id"]), he=str(cat_source["he"])).add()
                unknown = False
            except:
                pass

            try:
                configurer.Categories(cat_id=str(cat_source["cat_id"]), en=str(cat_source["en"])).add()
                unknown = False
            except:
                pass

            try:
                configurer.Categories(cat_id=str(cat_source["cat_id"]), ar=str(cat_source['ar'])).add()
                unknown = False
            except:
                pass

            if unknown:
                send(chat_id, texts.get_text(chat_id, "unknown_format_error_msg"))
            else:
                stg.admin_categories(chat_id)
                Stages(chat_id).set("None")

        #
        elif stage.split("||")[0] == f"admin_add_undercat":
            cat_id = stage.split("||")[1]
            undercat_dict = configurer.new_category_text(message.text)

            uc = configurer.UnderCats()
            uc.cat_id = cat_id
            print(undercat_dict)
            if "ru" in undercat_dict.keys():
                uc.ru = str(undercat_dict['ru'])
            if "en" in undercat_dict.keys():
                uc.en = str(undercat_dict['en'])
            if "he" in undercat_dict.keys():
                uc.he = str(undercat_dict['he'])
            if "ar" in undercat_dict.keys():
                uc.ar = str(undercat_dict['ar'])
            uc.add()

            Stages(chat_id).set("None")
            stg.admin_category_panel_select(chat_id, cat_id)


        # update item firm
        elif stage.split("||")[0] == "admin_item_panel_set_item_firm":
            item_id = stage.split("||")[1]
            firm_name = message.text
            st = configurer.Stock()
            st.set(search_value=item_id, column="item_firm", value=firm_name)

            send(chat_id, texts.get_text(chat_id, "new_value_setted_msg"), reply_markup=kmarkup().row(stg.back(chat_id, "admin_item")))
            Stages(chat_id).set("None")

        # update item barcode
        elif stage.split("||")[0] == "admin_item_panel_set_item_barcode":
            item_id = stage.split("||")[1]
            barcode = message.text
            st = configurer.Stock()
            st.set(search_value=item_id, column="barcode", value=barcode)

            send(chat_id, texts.get_text(chat_id, "new_value_setted_msg"), reply_markup=kmarkup().row(stg.back(chat_id, "admin_item")))
            Stages(chat_id).set("None")

        # update item input cost
        elif stage.split("||")[0] == "admin_item_panel_set_item_input_cost":
            item_id = stage.split("||")[1]
            input_cost = message.text
            if str_is_only_integers(input_cost):
                st = configurer.Stock()
                st.set(search_value=item_id, column="input_cost", value=input_cost)

                send(chat_id, texts.get_text(chat_id, "new_value_setted_msg"), reply_markup=kmarkup().row(stg.back(chat_id, "admin_item")))
                Stages(chat_id).set("None")

        # update item output cost
        elif stage.split("||")[0] == "admin_item_panel_set_item_output_cost":
            item_id = stage.split("||")[1]
            output_cost = message.text
            if str_is_only_integers(output_cost):
                st = configurer.Stock()
                st.set(search_value=item_id, column="output_cost", value=output_cost)

                send(chat_id, texts.get_text(chat_id, "new_value_setted_msg"), reply_markup=kmarkup().row(stg.back(chat_id, "admin_item")))
                Stages(chat_id).set("None")

        # update item count
        elif stage.split("||")[0] == "admin_item_panel_set_item_count":
            item_id = stage.split("||")[1]
            item_count = message.text
            if str_is_only_integers(item_count):
                st = configurer.Stock()
                st.set(search_value=item_id, column="item_count", value=item_count)

                send(chat_id, texts.get_text(chat_id, "new_value_setted_msg"), reply_markup=kmarkup().row(stg.back(chat_id, "admin_item")))
                Stages(chat_id).set("None")

        # admin find by id
        elif stage.split("||")[0] == "admin_find_by_id":
            st = configurer.Stock()
            if st.get(value=message.text) != None:
                stg.admin_item_panel(chat_id, message.text)

        # admin find by name
        elif stage.split("||")[0] == "admin_find_by_name":
            st = configurer.Stock()
            if st.get(by="name", value=message.text) != None:
                stg.admin_item_panel(chat_id, message.text)





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
            Stages(chat_id).set("None")


@bot.message_handler(content_types=['document'])
def doc_message(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        stage = Stages(chat_id).get()
        if stage.split("||")[0] == "admin_set_item_special_files_update":
            item_id = stage.split("||")[1]
            old_file = stage.split("||")[2]
            file_name = message.document.file_name

            os.remove(f"sources/items_files/{str(item_id)}/{str(old_file)}")

            @configurer.thread(with_timer=True)
            def down_file():
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(file_name, 'wb') as new_file:
                    new_file.write(downloaded_file)

            stg.admin_select_item_file(chat_id, item_id, file_name)
            Stages(chat_id).set("None")


@bot.callback_query_handler(func=lambda m: True)
def glob_calls(call):
    chat_id = call.message.chat.id

    def dm():
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass

    call_category = call.data.split('_')[0]
    cd = call.data.split("||")
    call_value = cd[0]

    if call.message.chat.type == "private":

        if call_value == "set_lang":
            configurer.Lang(chat_id).set(cd[1])
            if cd[2] == "admin":
                stg.admin_panel(chat_id)
                dm()
            elif cd[2] == "agent":
                stg.agent_panel(chat_id)
                dm()

        elif call_category == "admin":

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

                stg.admin_item_panel(chat_id, item_id)
                dm()

            # Admin add item page
            elif call_value == "admin_items_add":
                stg.admin_items_add(chat_id)
                dm()

            # Admin add name for item
            elif call_value == "admin_add_item_panel":
                cat_id = cd[1]
                if len(cd) == 3:
                    undercat_id = cd[2]
                    stg.admin_add_item_panel(chat_id, cat_id, undercat_id)
                else:
                    stg.admin_add_item_panel(chat_id, cat_id)
                dm()

            elif call_value == "admin_categories":
                stg.admin_categories(chat_id)
                dm()

            # Admin add category when add new item
            elif call_value == "admin_add_category":
                stg.admin_add_category(chat_id)
                dm()

            elif call_value == "admin_category_panel_select":
                cat_id = cd[1]
                stg.admin_category_panel_select(chat_id, cat_id)
                dm()

            elif call_value == "admin_add_undercat_to_cat":
                cat_id = cd[1]
                stg.admin_add_undercat_to_cat(chat_id, cat_id)
                dm()

            elif call_value == "admin_select_cat_without_undercat":
                cat_id = cd[1]
                k = kmarkup()
                msg = texts.get_text(chat_id, f"admin_add_undercat_msg")
                k.row(stg.back(chat_id, f"admin_add_category"))
                send(chat_id, msg, reply_markup=k)
                Stages(chat_id).set(f"admin_add_undercat_for_exiting_cat")


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

            #
            elif call_value == "admin_select_item_file":
                item_id = cd[1]
                file_name = cd[2]
                stg.admin_select_item_file(chat_id, item_id, file_name)
                dm()

            #
            elif call_value == "admin_firms":
                stg.admin_firms(chat_id)
                dm()

            #
            elif call_value == "admin_firm_panel":
                ident_id = cd[1]
                stg.admin_firm_panel(chat_id, ident_id)
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
                    tgi = configurer.TG_item_pre_add(item_id=cd[2])

                    if all((tgi.show()['item_name'] != "None", tgi.show()['item_firm'] != "None")):
                        tgi.send_to_main_db()
                        configurer.Catlinks(item_id=item_id, cat_id=cat_id, ident_id=configurer.Randomizer().lower_with_int()).add()

                        bot.answer_callback_query(call.id, texts.get_text(chat_id, "admin_set_new_item_done_call"), show_alert=True)
                        dm()
                        stg.admin_items(chat_id)

                    else:

                        bot.answer_callback_query(call.id, texts.get_text(chat_id, "admin_set_new_item_no_important_call"), show_alert=True)

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
                    stg.admin_item_panel_set_item_in_stock(chat_id, item_id)
                    dm()

            # set spec. files
            elif "admin_set_item_special_files" in call_value:
                item_id = cd[1]

                # set item special files
                if call_value == "admin_item_panel_set_item_special_files":
                    stg.admin_item_panel_set_item_special_files(chat_id, item_id)
                    dm()

                # download item special files
                elif call_value == "admin_set_item_special_files_download":
                    file_name = cd[2]
                    stg.admin_set_item_special_files_download(chat_id, item_id, file_name)
                    dm()

                # update item special files
                elif call_value == "admin_set_item_special_files_update":
                    file_name = cd[2]
                    stg.admin_set_item_special_files_update(chat_id, item_id, file_name)
                    dm()

                # remove item special files
                elif call_value == "admin_set_item_special_files_remove":
                    file_name = cd[2]
                    stg.admin_set_item_special_files_remove(chat_id, item_id, file_name)
                    dm()

            # find items by...
            elif "admin_find" in call_value:

                # find items by category
                if call_value == "admin_find_by_category":
                    # Category list
                    if len(cd) == 1:
                        stg.admin_find_by_category(chat_id)
                        dm()

                    # Selected category
                    elif len(cd) == 2:
                        stg.admin_find_by_category(chat_id, cat_id=cd[1])
                        dm()

                # find items by id
                elif call_value == "admin_find_by_id":
                    #
                    stg.admin_find_by_id(chat_id)
                    dm()

                # find items by name
                elif call_value == "admin_find_by_name":
                    #
                    stg.admin_find_by_name(chat_id)
                    dm()


        # Agent back office
        elif call_category == "agent":
            #
            pass

        # Customer back office
        elif call_category == "customer":
            #
            pass

        elif call_category == "generete":
            if call_value == "generete_items_csv":

                file_path = configurer.Csv("items.csv").items()

                file = open(file_path, "rb")
                bot.send_document(chat_id=chat_id, document=file)
                stg.admin_items(chat_id)


        else:
            send(chat_id, texts.get_text(chat_id, "in_Dev"))




bot.polling(timeout=10000)