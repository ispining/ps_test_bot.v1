import sqlite3
from pprint import pprint

import configurer
import texts
from config import *


def back(user_id, callback_data):
    bt = texts.get_text(user_id, "back_btn")
    return btn(bt, callback_data=callback_data)


def admin_panel(chat_id):
    k = kmarkup()
    items = btn(texts.get_text(chat_id, "items_btn"), callback_data=f"admin_item")
    sellers = btn(texts.get_text(chat_id, "firms_btn"), callback_data=f"admin_firms")

    k.row(items, sellers)
    send(chat_id, texts.get_text(chat_id, "admin_msg"), reply_markup=k)


def set_lang(chat_id):
    k = kmarkup()

    ru_btn = btn("Русский", callback_data=f"set_lang||ru")
    en_btn = btn("English", callback_data=f"set_lang||en")
    he_btn = btn("עברית", callback_data=f"set_lang||he")
    ar_btn = btn("Arabic", callback_data=f"set_lang||ar")

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
    find_by_firm = btn(texts.get_text(chat_id, "find_by_firm_btn"), callback_data=f"admin_find_by_firm")
    generete_items_csv = btn(texts.get_text(chat_id, "generete_csv_btn"), callback_data=f"generete_csv")

    for button in [items_add, find_by_category, find_by_id, find_by_name, find_by_firm, generete_items_csv]:
        k.row(button)

    k.row(back(chat_id, "admin"))
    send(chat_id, msg, reply_markup=k)


def admin_items_add(chat_id):
    configurer.TG_item_pre_add().remove_not_used()
    k = kmarkup()
    msg = texts.get_text(chat_id, "admin_select_category_for_add_item")
    k.row(btn("add_btn", callback_data=f"admin_add_category"))
    for cat_id in configurer.Categories().list_categories_id():
        cat = configurer.Categories(cat_id=cat_id).show_content(user_id=chat_id)
        button = btn(cat, callback_data=f"admin_add_item_panel||{cat_id}")
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
        sql.execute(f"SELECT * FROM mainapp_catlink WHERE cat_id = '{str(cat_id)}'")
        for ident_id, item_id, cat in sql.fetchall():
            if cat == cat_id:
                cat = configurer.Categories(cat_id=cat_id).show_content(user_id=chat_id)
                button = btn(cat, callback_data=f"admin_item_panel||{item_id}||admin_find_by_category")
                k.row(button)
        msg = texts.get_text(chat_id, f"admin_find_by_category_selector_msg||{cat_id}")
        k.row(back(chat_id, "admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)


def admin_item_panel(chat_id, item_id, back_callback):
    st = configurer.Stock()
    stock_dict = st.get(value=item_id)
    if stock_dict == None:
        # if no items found
        pass
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
            "creation_date": str(stock_dict['creation_date']),
            "exp_date": str(stock_dict['exp_date']),
            "package_num": str(stock_dict['package_num']),
            "item_count": str(stock_dict['item_count']),
            "in_stock": str(stock_dict['in_stock']),
            "special_files": str(stock_dict['special_files'])
        })
        k.row(btn(texts.get_text(chat_id, "set_item_name_btn"), callback_data=f"admin_item_panel_set_name||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_picture_btn"), callback_data=f"admin_item_panel_set_item_picture||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_item_firm_btn"), callback_data=f"admin_item_panel_set_item_firm||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_barcode_btn"), callback_data=f"admin_item_panel_set_item_barcode||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_input_cost_btn"), callback_data=f"admin_item_panel_set_item_input_cost||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_output_cost_btn"), callback_data=f"admin_item_panel_set_item_output_cost||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_creation_date_btn"), callback_data=f"admin_item_panel_set_item_creation_date||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_exp_date_btn"), callback_data=f"admin_item_panel_set_item_exp_date||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_package_num_btn"), callback_data=f"admin_item_panel_set_item_package_num||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_count_btn"), callback_data=f"admin_item_panel_set_item_count||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_item_in_stock_btn"), callback_data=f"admin_item_panel_set_item_in_stock||{str(item_id)}"))
        k.row(btn(texts.get_text(chat_id, "set_item_special_files_btn"), callback_data=f"admin_item_panel_set_item_special_files||{str(item_id)}"))

        k.row(back(chat_id, back_callback))
        send(chat_id, msg, reply_markup=k)


def admin_item_panel_set(chat_id, item_id, set=None):
    k = kmarkup()
    msg = None
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
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        if picture == "None":
            send(chat_id, msg, reply_markup=k)
        else:
            bot.send_photo(chat_id=chat_id, photo=open(item_info['picture'], "rb"), caption=msg, reply_markup=k)
    elif set == "item_firm":
        msg = texts.get_text(chat_id, "")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
    elif set == "barcode":
        msg = texts.get_text(chat_id, "")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
    elif set == "input_cost":
        msg = texts.get_text(chat_id, "")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
    elif set == "output_cost":
        msg = texts.get_text(chat_id, "")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
    elif set == "creation_date":
        msg = texts.get_text(chat_id, "")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
    elif set == "exp_date":
        msg = texts.get_text(chat_id, "")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
    elif set == "package_num":
        msg = texts.get_text(chat_id, "")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
    elif set == "item_count":
        msg = texts.get_text(chat_id, "")
        k.row(back(chat_id, f"admin_item_panel||{item_id}||admin_find_by_category"))
        send(chat_id, msg, reply_markup=k)
    elif set == "files":
        msg = texts.get_text(chat_id, "")


def admin_item_panel_set_item_picture(chat_id, item_id):
    pass


