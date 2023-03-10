
from pprint import pprint

import configurer
import texts
from config import *


def back(user_id, callback_data):
    bt = texts.get_text(user_id, "back_btn")
    return btn(bt, callback_data=callback_data)


class Alerts:
    def __init__(self, chat_id, back_call=None):
        self.chat_id = chat_id
        self.back_call = back_call

    def no_permissions(self):
        if self.back_call == None:
            send(self.chat_id, texts.get_text(self.chat_id, "no_permissions_msg"))
        else:
            send(self.chat_id, texts.get_text(self.chat_id, "no_permissions_msg"), reply_markup=kmarkup().row(back(self.chat_id, self.back_call)))

    def stage_for_nums(self):
        if self.back_call == None:
            send(self.chat_id, texts.get_text(self.chat_id, "nums_only_msg"))
        else:
            send(self.chat_id, texts.get_text(self.chat_id, "nums_only_msg"), reply_markup=kmarkup().row(back(self.chat_id, self.back_call)))


def admin_panel(chat_id):
    s = configurer.Staff(chat_id).get()
    if s != None:
        if s['status'] in configurer.ADMIN_PANEL_ALLOWED_STATUSES:
            k = kmarkup()
            items_button = btn(texts.get_text(chat_id, "items_btn"), callback_data=f"admin_item")
            firms_button = btn(texts.get_text(chat_id, "firms_btn"), callback_data=f"admin_firms")

            categories_button = btn(texts.get_text(chat_id, "categories_btn"), callback_data=f"admin_categories")
            admins_button = btn(texts.get_text(chat_id, "admins_btn"), callback_data=f"admin_admins")
            k.row(items_button, firms_button)
            k.row(categories_button)
            k.row(admins_button)
            send(chat_id, texts.get_text(chat_id, "admin_msg"), reply_markup=k)


def set_lang(chat_id, next_call):
    k = kmarkup()

    ru_btn = btn("Русский", callback_data=f"set_lang||ru||{str(next_call)}")
    en_btn = btn("English", callback_data=f"set_lang||en||{str(next_call)}")
    he_btn = btn("עברית", callback_data=f"set_lang||he||{str(next_call)}")
    ar_btn = btn("Arabic", callback_data=f"set_lang||ar||{str(next_call)}")

    msg = """
<b>Select your language</b>    
    """


    for button in [he_btn, ru_btn, en_btn, ar_btn]:
        k.row(button)

    send(chat_id, msg, reply_markup=k)


def admin_items(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_items_msg")
    items_add = btn(texts.get_text(chat_id, "add_btn"), callback_data=f"admin_items_add")
    find_by_category = btn(texts.get_text(chat_id, "find_by_category_btn"), callback_data=f"admin_find_by_category")
    find_by_id = btn(texts.get_text(chat_id, "find_by_id_btn"), callback_data=f"admin_find_by_id")
    find_by_name = btn(texts.get_text(chat_id, "find_by_name_btn"), callback_data=f"admin_find_by_name")
    #find_by_firm = btn(texts.get_text(chat_id, "find_by_firm_btn"), callback_data=f"admin_find_by_firm")
    generete_items_csv = btn(texts.get_text(chat_id, "generete_csv_btn"), callback_data=f"generete_items_csv")
    upload_items_csv = btn(texts.get_text(chat_id, "upload_from_csv_btn"), callback_data=f"upload_items_from_csv")

    for button in [items_add, find_by_category, find_by_id, find_by_name, generete_items_csv, upload_items_csv]:
        k.row(button)

    k.row(back(chat_id, "admin"))
    send(chat_id, msg, reply_markup=k)


def admin_items_add(chat_id):
    configurer.TG_item_pre_add().remove_not_used()
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_select_category_for_add_item")
    for cat_id in configurer.Categories().list_categories_id():
        for undercat_id in configurer.UnderCats(cat_id=cat_id).list_all_id():
            b_end = configurer.UnderCats(undercat_id=undercat_id).show_content(user_id=chat_id)
            b_start = configurer.Categories(cat_id=cat_id).show_content(user_id=chat_id)
            button = btn(b_start + ' -> ' + b_end, callback_data=f"admin_add_item_panel||{undercat_id}")
            k.row(button)
    k.row(back(chat_id, "admin_item"))
    send(chat_id, msg, reply_markup=k)


def admin_add_item_panel(chat_id, cat_id, item_id="None"):
    if item_id == "None":
        ctg = configurer.TG_item_pre_add()
        ctg.item_id = configurer.Randomizer().lower_with_int()
        item_id = ctg.item_id
        ctg.add()

    k = kmarkup()

    name_btn = texts.get_text(chat_id, "set_item_name_btn")
    picture_btn = texts.get_text(chat_id, "set_item_picture_btn")
    item_firm_btn = texts.get_text(chat_id, "set_item_item_firm_btn")
    barcode_btn = texts.get_text(chat_id, "set_item_barcode_btn")
    input_cost_btn = texts.get_text(chat_id, "set_item_input_cost_btn")
    output_cost_btn = texts.get_text(chat_id, "set_item_output_cost_btn")
    item_count_btn = texts.get_text(chat_id, "set_item_item_count_btn")

    cdb = configurer.TG_item_pre_add(item_id).show()
    pprint(cdb)
    if cdb['item_name'] in [None, "None"]:
        name_btn = f"{texts.IMPORTANT_BTN} {name_btn}"
    else:
        name_btn = f"{texts.ALLOW_BTN} {name_btn}"

    if cdb['picture'] in [None, "None"]:
        pass
    else:
        picture_btn = f"{texts.ALLOW_BTN} {picture_btn}"

    if cdb['item_firm'] in [None, "None"]:
        item_firm_btn = f"{texts.IMPORTANT_BTN} {item_firm_btn}"
    else:
        item_firm_btn = f"{texts.ALLOW_BTN} {item_firm_btn}"

    if cdb['barcode'] in [None, "None"]:
        pass
    else:
        barcode_btn = f"{texts.ALLOW_BTN} {barcode_btn}"

    if cdb['input_cost'] in [None, "None"]:
        pass
    else:
        input_cost_btn = f"{texts.ALLOW_BTN} {input_cost_btn}"

    if cdb['output_cost'] in [None, "None"]:
        pass
    else:
        output_cost_btn = f"{texts.ALLOW_BTN} {output_cost_btn}"

    if cdb['item_count'] in [None, "None"]:
        pass
    else:
        item_count_btn = f"{texts.ALLOW_BTN} {item_count_btn}"


    name = btn(name_btn, callback_data=f"admin_set_new_item_name||{str(cat_id)}||{str(item_id)}")
    picture = btn(picture_btn, callback_data=f"admin_set_new_item_picture||{str(cat_id)}||{str(item_id)}")
    item_firm = btn(item_firm_btn, callback_data=f"admin_set_new_item_firm||{str(cat_id)}||{str(item_id)}")
    barcode = btn(barcode_btn, callback_data=f"admin_set_new_item_barcode||{str(cat_id)}||{str(item_id)}")
    input_cost = btn(input_cost_btn, callback_data=f"admin_set_new_item_input_cost||{str(cat_id)}||{str(item_id)}")
    output_cost = btn(output_cost_btn, callback_data=f"admin_set_new_item_output_cost||{str(cat_id)}||{str(item_id)}")
    item_count = btn(item_count_btn, callback_data=f"admin_set_new_item_count||{str(cat_id)}||{str(item_id)}")
    done_btn = btn(texts.get_text(chat_id, "done_btn"), callback_data=f"admin_set_new_item_done||{str(cat_id)}||{str(item_id)}")
    for button in [
                   name,
                   picture,
                   item_firm,
                   barcode,
                   input_cost,
                   output_cost,
                   item_count,
                   done_btn]:
        k.row(button)

    msg = texts.get_text(chat_id, "admin_add_item_panel").format(**{
        "lcat": configurer.Categories(cat_id=cat_id).show_content(user_id=chat_id)
    })
    k.row(back(chat_id, "admin_items_add"))
    send(chat_id, msg, reply_markup=k)


def admin_set_new_item_name(call, cat_id, item_id):
    chat_id = call

    k = kmarkup()

    msg = texts.get_text(chat_id, "admin_set_new_item_name_msg")

    k.row(back(chat_id, f"admin_add_item_panel||{cat_id}"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_set_new_item_name||{str(cat_id)}||{str(item_id)}")


def admin_set_new_item_picture(call, cat_id, item_id):
    chat_id = call.message.chat.id

    k = kmarkup()

    msg = texts.get_text(chat_id, "admin_set_new_item_picture_msg")

    k.row(back(chat_id, f"admin_add_item_panel||{cat_id}"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_set_new_item_picture||{str(cat_id)}||{str(item_id)}")


def admin_set_new_item_firm(call, cat_id, item_id):
    chat_id = call.message.chat.id

    k = kmarkup()

    msg = texts.get_text(chat_id, "admin_set_new_item_firm_msg")

    k.row(back(chat_id, f"admin_add_item_panel||{cat_id}"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_set_new_item_firm||{str(cat_id)}||{str(item_id)}")


def admin_set_new_item_barcode(call, cat_id, item_id):
    chat_id = call.message.chat.id

    k = kmarkup()

    msg = texts.get_text(chat_id, "admin_set_new_item_barcode_msg")

    k.row(back(chat_id, f"admin_add_item_panel||{cat_id}"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_set_new_item_barcode||{str(cat_id)}||{str(item_id)}")


def admin_set_new_item_input_cost(call, cat_id, item_id):
    chat_id = call.message.chat.id

    k = kmarkup()

    msg = texts.get_text(chat_id, "admin_set_new_item_input_cost_msg")

    k.row(back(chat_id, f"admin_add_item_panel||{cat_id}"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_set_new_item_input_cost||{str(cat_id)}||{str(item_id)}")


def admin_set_new_item_output_cost(call, cat_id, item_id):
    chat_id = call.message.chat.id

    k = kmarkup()

    msg = texts.get_text(chat_id, "admin_set_new_item_output_cost_msg")

    k.row(back(chat_id, f"admin_add_item_panel||{cat_id}"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_set_new_item_output_cost||{str(cat_id)}||{str(item_id)}")


def admin_set_new_item_count(call, cat_id, item_id):
    chat_id = call.message.chat.id

    k = kmarkup()

    msg = texts.get_text(chat_id, "admin_set_new_item_count_msg")

    k.row(back(chat_id, f"admin_add_item_panel||{cat_id}"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_set_new_item_count||{str(cat_id)}||{str(item_id)}")


def admin_add_category(chat_id):

    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_add_category_msg")
    k.row(back(chat_id, "admin_items_add"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_add_category")


def admin_find_by_category(chat_id, cat_id=None):

    # Categories stage
    if cat_id == None:
        k = kmarkup()
        msg = texts.get_text(chat_id, "admin_find_by_category_msg")
        for cat_id in configurer.Categories().list_categories_id():
            cat = configurer.Categories(cat_id=cat_id).show_content(user_id=chat_id)
            button = btn(cat, callback_data=f"admin_find_by_category||{cat_id}")
            k.row(button)
        k.row(back(chat_id, "admin_item"))
        send(chat_id, msg, reply_markup=k)

    # category selected stage
    elif cat_id != None:
        k = kmarkup()

        for undercat_id in configurer.UnderCats(cat_id=cat_id).list_all_id():
            undercat = configurer.UnderCats(undercat_id=undercat_id).show_content(chat_id)
            button = btn(undercat, callback_data=f"admin_find_by_undercat||{undercat_id}||1")
            k.row(button)
        msg = texts.get_text(chat_id, f"admin_find_by_category_selector_msg")
        k.row(back(chat_id, f"admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)


def admin_find_by_undercat(chat_id, undercat_id, page="1"):
    page = int(page)
    step = 10
    from_item = page * step - step
    to_item = page * step
    items_id = configurer.Catlinks(cat_id=undercat_id).list_undercat_items()

    last_page_btn = btn("< < <", callback_data=f"admin_find_by_undercat||{undercat_id}||{str(page - 1)}")
    next_page_btn = btn("> > >", callback_data=f"admin_find_by_undercat||{undercat_id}||{str(page + 1)}")

    k = kmarkup()
    stock = configurer.Stock()
    item_num = 0

    for item_id in items_id:
        if item_num >= from_item and item_num < to_item:

            k.row(btn(stock.get(value=item_id)['name'], callback_data=f"admin_item_panel||{str(item_id)}"))
        item_num += 1

    if len(items_id) <= 10:
        pass
    elif from_item == 0:
        k.row(next_page_btn)
    elif to_item >= len(items_id):
        k.row(last_page_btn)
    else:
        k.row(last_page_btn, next_page_btn)
    k.row(back(chat_id, f"admin_find_by_category"))
    send(chat_id, texts.get_text(chat_id, "admin_find_by_undercat_list_items_msg").format(**{
        "page_num": str(page),
        "from_item": str((int(page)*10)-9),
        "to_item": str((int(page)*10)+1)

    }), reply_markup=k)

def admin_find_by_id(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_find_by_id_msg")
    k.row(back(chat_id, "admin_item"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set("admin_find_by_id")


def admin_find_by_name(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_find_by_name_msg")
    k.row(back(chat_id, "admin_item"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set("admin_find_by_name")


def admin_item_panel(chat_id, item_id):
    st = configurer.Stock()
    stock_dict = st.get(value=item_id)
    if stock_dict == None:
        k = kmarkup()
        k.row(back(chat_id, f"admin_item"))
        send(chat_id, texts.get_text(chat_id, "item_not_found_msg"), reply_markup=k)
    else:
        k = kmarkup()
        msg = texts.get_text(chat_id, "admin_item_panel_msg").format(**{
            "item_id": str(item_id),
            "name": str(stock_dict['name']),
            "picture": str(stock_dict['picture']),
            "item_firm": str(stock_dict['item_firm']),
            "barcode": str(stock_dict['barcode']),
            "input_cost": str(stock_dict['input_cost']),
            "output_cost": str(stock_dict['output_cost']),
            "item_count": str(stock_dict['item_count']),
            "in_stock": str(stock_dict['in_stock']),
            "special_files": str(stock_dict['files'])
        })
        k.row(btn(texts.get_text(chat_id, "set_item_name_btn"), callback_data=f"admin_item_panel_set_name||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_picture_btn"), callback_data=f"admin_item_panel_set_item_picture||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_item_firm_btn"), callback_data=f"admin_item_panel_set_item_firm||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_barcode_btn"), callback_data=f"admin_item_panel_set_item_barcode||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_input_cost_btn"), callback_data=f"admin_item_panel_set_item_input_cost||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_output_cost_btn"), callback_data=f"admin_item_panel_set_item_output_cost||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_item_count_btn"), callback_data=f"admin_item_panel_set_item_count||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_item_in_stock_btn"), callback_data=f"admin_item_panel_set_item_in_stock||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_special_files_btn"), callback_data=f"admin_item_panel_set_item_special_files||{str(item_id)}"))

        k.row(back(chat_id, "admin_item"))
        send(chat_id, msg, reply_markup=k)
        Stages(chat_id).set("None")


def admin_item_panel_set(chat_id, item_id, set=None):
    k = kmarkup()
    if set == "name":
        msg = texts.get_text(chat_id, "").format(**{
            "item_id": "",
            "ru": texts.get_text("ru", ""),
            "en": texts.get_text("en", ""),
            "he": texts.get_text("he", ""),
            "ar": texts.get_text("ar", "")
        })
    elif set == "picture":
        st = configurer.Stock()
        item_info = st.get("item_id", item_id)
        picture = None
        if item_info['picture'] != "None":
            picture = item_info['picture']
        msg = texts.get_text(chat_id, "admin_item_panel_set_picture_msg")

        k.row(btn(texts.get_text(chat_id, "remove_item_picture_btn"), callback_data=f"admin_remove_item_picture||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "edit_item_picture_btn"), callback_data=f"admin_edit_item_picture||{str(item_id)}"))
        k.row(back(chat_id, f"admin_item"))
        if picture in ["None", "", None]:
            send(chat_id, msg, reply_markup=k)
        else:
            bot.send_photo(chat_id=chat_id, photo=open(item_info['picture'], "rb"), caption=msg, reply_markup=k)
    elif set == "item_firm":
        msg = texts.get_text(chat_id, "admin_item_panel_set_item_firm_msg")
        k.row(back(chat_id, f"admin_item"))
        send(chat_id, msg, reply_markup=k)
        Stages(chat_id).set(f"admin_item_panel_set_item_firm||{str(item_id)}")
    elif set == "barcode":
        msg = texts.get_text(chat_id, "admin_item_panel_set_item_barcode_msg")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
        Stages(chat_id).set(f"admin_item_panel_set_item_barcode||{str(item_id)}")
    elif set == "input_cost":
        msg = texts.get_text(chat_id, "admin_item_panel_set_item_input_cost_msg")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
        Stages(chat_id).set(f"admin_item_panel_set_item_input_cost||{str(item_id)}")
    elif set == "output_cost":
        msg = texts.get_text(chat_id, "admin_item_panel_set_item_output_cost_msg")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
        Stages(chat_id).set(f"admin_item_panel_set_item_output_cost||{str(item_id)}")
    elif set == "item_count":
        msg = texts.get_text(chat_id, "admin_item_panel_set_item_count_msg")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
        Stages(chat_id).set(f"admin_item_panel_set_item_count||{str(item_id)}")


def admin_remove_item_someshit(chat_id, item_id, to_delete):
    st = configurer.Stock()
    st.item_id = item_id
    st.remove(to_delete)
    admin_item_panel(chat_id, item_id)


def admin_edit_item_picture(chat_id, item_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_edit_item_picture_msg")
    k.row(back(chat_id, "admin_item"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_edit_item_picture||{str(item_id)}")


def admin_item_panel_set_item_in_stock(chat_id, item_id):
    st = configurer.Stock()
    in_stock = st.get(value=item_id)['in_stock']
    if in_stock in ["None", "False"]:
        st.set(search_value=item_id, column="in_stock", value="True")
    elif in_stock == "True":
        st.set(search_value=item_id, column="in_stock", value="False")

    admin_item_panel(chat_id, item_id)


def admin_item_panel_set_item_special_files(chat_id, item_id):
    k = kmarkup()
    if item_id not in os.listdir("sources/items_files"):
        os.mkdir("sources/items_files/"+item_id)

    for file in os.listdir("sources/items_files/"+item_id):
        k.row(btn(file, callback_data=f"admin_select_item_file||{str(item_id)}||{file}"))
    msg = texts.get_text(chat_id, "admin_set_item_special_files_msg")
    k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
    send(chat_id, msg, reply_markup=k)


def admin_select_item_file(chat_id, item_id, file_name):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_select_item_file_msg")
    k.row(btn(texts.get_text(chat_id, "download_file"), callback_data=f"admin_set_item_special_files_download||{str(item_id)}||{file_name}"))
    k.row(btn(texts.get_text(chat_id, "update_file"), callback_data=f"admin_set_item_special_files_update||{str(item_id)}||{file_name}"))
    k.row(btn(texts.get_text(chat_id, "remove_file"), callback_data=f"admin_set_item_special_files_remove||{str(item_id)}||{file_name}"))
    k.row(back(chat_id, f"admin_item_panel_set_item_special_files||{str(item_id)}"))
    send(chat_id, msg, reply_markup=k)


def admin_set_item_special_files_download(chat_id, item_id, file_name):
    filepath = f"sources/items_files/{str(item_id)}/{str(file_name)}"
    file = open(filepath, "rb")
    bot.send_document(chat_id=chat_id, document=file)
    admin_select_item_file(chat_id, item_id, file_name)


def admin_set_item_special_files_update(chat_id, item_id, file_name):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_special_files_update")
    k.row(back(chat_id, f"admin_select_item_file||{str(item_id)}||{file_name}"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_set_item_special_files_update||{str(item_id)}||{file_name}")


def admin_set_item_special_files_remove(chat_id, item_id, file_name):
    os.remove(f"sources/items_files/{str(item_id)}/{str(file_name)}")
    admin_item_panel(chat_id, item_id)


def agent_panel(chat_id):
    k = kmarkup()
    #msg = texts.get_text(chat_id, "agent_panel")
    # k.row(btn(texts.get_text(chat_id, ""), callback_data=f""))
    # k.row(btn(texts.get_text(chat_id, ""), callback_data=f""))
    # k.row(btn(texts.get_text(chat_id, ""), callback_data=f""))
    # k.row(btn(texts.get_text(chat_id, ""), callback_data=f""))
    #send(chat_id, msg, reply_markup=k)


def admin_firms(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_firms_msg")
    btn(texts.get_text(chat_id, "add_btn"), callback_data=f"admin_add_firm")
    for firm in configurer.Firm().listall():
        k.row(btn(firm['firm_name'], callback_data=f"admin_firm_panel||{str(firm['ident_id'])}"))
    k.row(back(chat_id, "admin"))
    send(chat_id, msg, reply_markup=k)


def admin_add_firm(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_add_firm_msg")
    k.row(back(chat_id, f"admin_firms"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_add_firm")


def customer_panel(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "customer_panel")
    #k.row(btn(texts.get_text(chat_id, "categories_btn"), callback_data=f"customer_categories"))
    #k.row(btn(texts.get_text(chat_id, "firms_btn"), callback_data=f"customer_firms"))

    send(chat_id, msg, reply_markup=k)


def admin_firm_panel(chat_id, ident_id):
    cf = configurer.Firm()
    cf.ident_id = ident_id
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_firm_panel_msg").format(**{
        "ident_id": ident_id,
        "firm_name": cf.get(value=ident_id)['firm_name'],
        "affiliate_count": str(cf.affiliate_count())
    })

    k.row(btn(texts.get_text(chat_id, "affiliates_btn"), callback_data=f"admin_firm_affiliates||{str(ident_id)}"))
    k.row(btn(texts.get_text(chat_id, "edit_data_btn"), callback_data=f"admin_edit_firm_data||{str(ident_id)}"))



    k.row(back(chat_id, "admin_firms"))
    send(chat_id, msg, reply_markup=k)


def admin_edit_firm_data(chat_id, firm_id):
    k = kmarkup()

    msg = texts.get_text(chat_id, "admin_edit_firm_data_msg")

    name_btn = btn(texts.get_text(chat_id, "firm_name_btn"), callback_data=f"admin_edit_firm_name||{str(firm_id)}")
    picture_btn = btn(texts.get_text(chat_id, "firm_picture_btn"), callback_data=f"admin_edit_firm_picture||{str(firm_id)}")
    contact_id_btn = btn(texts.get_text(chat_id, "firm_contact_id_btn"), callback_data=f"admin_edit_firm_contact_id||{str(firm_id)}")
    phone_btn = btn(texts.get_text(chat_id, "firm_phone_btn"), callback_data=f"admin_edit_firm_phone||{str(firm_id)}")
    site_btn = btn(texts.get_text(chat_id, "firm_site_btn"), callback_data=f"admin_edit_firm_site||{str(firm_id)}")
    email_btn = btn(texts.get_text(chat_id, "firm_email_btn"), callback_data=f"admin_edit_firm_email||{str(firm_id)}")

    files_btn = btn(texts.get_text(chat_id, "firm_files_btn"), callback_data=f"admin_edit_firm_files||{str(firm_id)}")

    for button in [name_btn, picture_btn, contact_id_btn, phone_btn, site_btn, email_btn, files_btn]:
        k.row(button)

    send(chat_id, msg, reply_markup=k)


def admin_edit_firm_name(chat_id, ident_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "")
    k.row(back(chat_id, f""))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_edit_firm_name||{str(ident_id)}")


def admin_edit_firm_picture(chat_id, ident_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "")
    k.row(back(chat_id, f""))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_edit_firm_picture||{str(ident_id)}")

def admin_categories(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_categories_panel_msg")
    k.row(btn(texts.get_text(chat_id, "add_btn"), callback_data=f"admin_add_category"))
    for cat_id in configurer.Categories().list_categories_id():
        k.row(btn(configurer.Categories(cat_id=cat_id).show_content(user_id=chat_id), callback_data=f"admin_category_panel_select||{str(cat_id)}"))
    k.row(back(chat_id, "admin"))
    send(chat_id, msg, reply_markup=k)


def admin_category_panel_select(chat_id, cat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_category_panel_select_msg")
    k.row(btn(texts.get_text(chat_id, "add_btn"), callback_data=f"admin_add_undercat_to_cat||{str(cat_id)}"))
    for undercat_id in configurer.UnderCats(cat_id=cat_id).list_all_id():
        k.row(btn(configurer.UnderCats(undercat_id=undercat_id).show_content(user_id=chat_id), callback_data=f"admin_remove_undercat||{str(cat_id)}||{str(undercat_id)}"))
    k.row(back(chat_id, f"admin_categories"))
    send(chat_id, msg, reply_markup=k)


def admin_add_undercat_to_cat(chat_id, cat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_add_undercat_msg")
    k.row(back(chat_id, f"admin_category_panel_select||{str(cat_id)}"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_add_undercat||{str(cat_id)}")


def admin_admins(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_admins_msg")
    admins = btn(texts.get_text(chat_id, "admins_set_btn"), callback_data=f"admin_admins_adminview")
    developers = btn(texts.get_text(chat_id, "developers_set_btn"), callback_data=f"admin_admins_devview")
    view_all = btn(texts.get_text(chat_id, "viewall_btn"), callback_data=f"admin_admins_viewall")
    for button in [admins, developers, view_all]:
        k.row(button)
    k.row(back(chat_id, f"admin"))
    send(chat_id, msg, reply_markup=k)


def admin_admins_adminview(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_admins_adminview_msg")
    admins_list = configurer.Staff().list_by_status('admin')

    k.row(btn(texts.get_text(chat_id, "add_btn"), callback_data=f"admin_admins_add_admin"))
    for user_id, vip, reg_date, special_files, status in admins_list:
        b_view = bot.get_chat(user_id)
        if b_view != None:
            b_view = b_view.title
            if b_view == None:
                b_view = user_id
        else:
            b_view = user_id
        k.row(btn(b_view, callback_data=f"admin_admins_panel||{str(user_id)}"))
    k.row(back(chat_id, "admin_admins"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set("None")


def admin_admins_add_admin(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_admins_add_admin_msg")
    k.row(back(chat_id, "admin_admins_adminview"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_admins_add_admin||{str(chat_id)}")


def admin_admins_panel(chat_id, admin_id):
    admin_info = configurer.Staff(admin_id).get()

    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_admins_panel_msg").format(**{
        "user_id": str(admin_id),
        "name": bot.get_chat(admin_id).first_name,
        "username": bot.get_chat(admin_id).first_name,
        "reg_date": admin_info['reg_date']
    })
    k.row(btn(texts.get_text(chat_id, "remove_admin_btn"), callback_data=f"admin_remove_admin||{str(admin_id)}"))
    k.row(back(chat_id, "admin_admins_adminview"))
    send(chat_id, msg, reply_markup=k)


def admin_remove_admin(call, admin_id):
    chat_id = call.fom_user.id
    configurer.Staff(admin_id).remove_by_id()
    bot.answer_callback_query(call.id, texts.get_text(chat_id, "admin_remove_admin_removed_msg"), show_alert=True)
    admin_admins(chat_id)
    
    
def admin_admins_devview(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_admins_devview_msg")
    devs_list = configurer.Staff().list_by_status('developer')

    k.row(btn(texts.get_text(chat_id, "add_btn"), callback_data=f"admin_admins_add_developer"))
    for user_id, vip, reg_date, special_files, status in devs_list:
        b_view = bot.get_chat(user_id)
        if b_view != None:
            b_view = b_view.title
            if b_view == None:
                b_view = user_id
        else:
            b_view = user_id
        k.row(btn(b_view, callback_data=f"admin_devs_panel||{str(user_id)}"))
    k.row(back(chat_id, "admin_admins"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set("None")


def admin_admins_add_developer(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_admins_add_developer_msg")
    k.row(back(chat_id, "admin_admins_devview"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set(f"admin_admins_add_developer||{str(chat_id)}")


def admin_devs_panel(chat_id, dev_id):
    dev_info = configurer.Staff(dev_id).get()

    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_devs_panel_msg").format(**{
        "user_id": str(dev_id),
        "name": bot.get_chat(dev_id).first_name,
        "username": bot.get_chat(dev_id).first_name,
        "reg_date": dev_info['reg_date']
    })
    k.row(btn(texts.get_text(chat_id, "remove_dev_btn"), callback_data=f"admin_remove_dev||{str(dev_id)}"))
    k.row(back(chat_id, "admin_admins_adminview"))
    send(chat_id, msg, reply_markup=k)


def admin_remove_dev(call, dev_id):
    chat_id = call.message.chat.id
    configurer.Staff(dev_id).remove_by_id()
    bot.answer_callback_query(call.id, texts.get_text(chat_id, "admin_remove_developer_removed_msg"), show_alert=True)
    admin_admins(chat_id)


def upload_items_from_csv(chat_id):
    k = kmarkup()
    msg = texts.get_text(chat_id, "upload_items_from_csv_msg")
    k.row(back(chat_id, "admin_item"))
    send(chat_id, msg, reply_markup=k)
    Stages(chat_id).set("upload_items_from_csv")