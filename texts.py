import datetime
import os
import threading

from config import db, sql
import configurer



contents = [
    # admin_msg
    ['admin_msg',
     """<b>Админ панель</b>
Выберите действие""",
     'en',
     'he',
     'ar'
     ],

    #admin_items_msg
    ["admin_items_msg",
    """<b>Товары</b>
Выберите данная платформа расчитана на не ограниченное колличество товаров, изза чего показ всех товаров не предусмотрен.
Вы можете сгенирировать список всех товаров в файл, и найти товар по идентификатору, названию, или производителю.""",
    'en',
    'he',
    'ar'

    ],

    # admin_select_category_for_add_item
    ['admin_select_category_for_add_item',
    """<b>Добавление товара</b>
Выберите категорию товара, или добавьте новую категорию""",
    'en',
    'he',
    'ar'
    ],

    # admin_add_item_panel
    ['admin_add_item_panel',
    """<b>Добавление товара</b>
Категория товара: {lcat}

Заполните следующие пункты.

❗ - Обязательные

""",
    'en',
    'he',
    'ar'
    ],

    # admin_set_new_item_name_msg
    ['admin_set_new_item_name_msg',
    """<b>Добавление товара</b>
Категория товара: {lcat}

Введите название нового товара.
""",
    'en',
    'he',
    'ar'
    ],

    # admin_set_new_item_picture_msg
    ['admin_set_new_item_picture_msg',
    """<b>Добавление товара</b>
Категория товара: {lcat}

Добавьте фото товара.

(Этот пункт не является обязательным!)
""",
    'en',
    'he',
    'ar'
    ],

    # admin_set_new_item_firm_msg
    ['admin_set_new_item_firm_msg',
    """<b>Добавление товара</b>

Введите фирму производителя товара

(Этот пункт не является обязательным!)
""",
    'en',
    'he',
    'ar'
    ],

    # admin_set_new_item_barcode_msg
    ['admin_set_new_item_barcode_msg',
    """<b>Добавление товара</b>

Введите штрихкод товара

(Этот пункт не является обязательным!)
""",
    'en',
    'he',
    'ar'
    ],

    # admin_set_new_item_input_cost_msg
    ['admin_set_new_item_input_cost_msg',
    """<b>Добавление товара</b>

Введите цену закупки товара.

(Этот пункт не является обязательным!)
""",
    'en',
    'he',
    'ar'
    ],

    # admin_set_new_item_output_cost_msg
    ['admin_set_new_item_output_cost_msg',
    """<b>Добавление товара</b>

Введите цену продажи товара.

(Этот пункт не является обязательным!)
""",
    'en',
    'he',
    'ar'
    ],

    # admin_set_new_item_count_msg
    ['admin_set_new_item_count_msg',
    """<b>Добавление товара</b>

Введите цену продажи товара.

(Этот пункт не является обязательным!)
""",
    'en',
    'he',
    'ar'
    ],

    # admin_add_category_msg
    ['admin_add_category_msg',
    """<b>Добавление категории</b>

Отправьте название категории с помощью следующего шаблона:

he::{content}
ru::{content}
en::{content}
ar::{content}

Можно отправить несколько языков в одном сообщении.
Хотите добавить только один язык? Так тоже можно
""",
    'en',
    'he',
    'ar'
    ],

    # admin_set_new_item_done_call
    ['admin_set_new_item_done_call',
    """Товар успешно добавлен.
""",
    'en',
    'he',
    'ar'
    ],

    # admin_set_new_item_no_important_call
    ['admin_set_new_item_no_important_call',
    """ОШИБКА!
Вы не заполнили обязательные поля для заполнения""",
    'en',
    'he',
    'ar'
    ],

    # admin_find_by_category_msg
    ['admin_find_by_category_msg',
    """<b>Товар по категории</b>
    
Выберите категорию товара""",
    'en',
    'he',
    'ar'
    ],

    # admin_find_by_category_selector_msg
    ['admin_find_by_category_selector_msg',
    """<b>Товар по категории</b>
    
Выберите товар""",
    'en',
    'he',
    'ar'
    ],

    # admin_item_panel_msg
    ['admin_item_panel_msg',
    """<b>{name}</b>
    
<b>ID товара:</b> {item_id}
<b>Название товара:</b> {name} 
<b>Фото товара:</b> {picture}
<b>Производитель:</b> {item_firm}
<b>Штрих-код:</b> {barcode}
<b>Цена закупки:</b> {input_cost}шек.
<b>Цена продажи:</b> {output_cost}шек.
<b>В наличии:</b> {item_count}шт.
<b>На складе:</b> {in_stock}
<b>Доп. файлы:</b> {special_files}
""",
    'en',
    'he',
    'ar'
    ],

    # in_Dev
    ['in_Dev',
    """<b>В разработке</b>
    
Данная функция находится на стадии разработки / обновлений.
""",
    'This feature is under development / updates.',
    'תכונה זו נמצאת בפיתוח/עדכונים.',
    'هذه الميزة قيد التطوير / التحديثات.'
    ],

    # admin_item_panel_set_picture_msg
    ['admin_item_panel_set_picture_msg',
    """<b>Изображение / Фото товара</b>
    
Выберите действие.
""",
    'en',
    'he',
    'ar'
    ],

    # admin_item_panel_set_item_firm_msg
    ['admin_item_panel_set_item_firm_msg',
    """<b>Изображение / Фото товара</b>
    
Выберите действие.
""",
    'en',
    'he',
    'ar'
    ],





############# BUTTONS #############
    # items_btn
    ['items_btn',
    "Товары",
    'en',
    'he',
    'ar'
    ],

    # firms_btn
    ['firms_btn',
    "Фирмы",
    'en',
    'he',
    'ar'
    ],

    # add_btn
    ['add_btn',
    "Добавить",
    'en',
    'he',
    'ar'
    ],

    # find_by_id_btn
    ['find_by_id_btn',
    "Искать по Идентификатору",
    'en',
    'he',
    'ar'
    ],

    # find_by_name_btn
    ['find_by_name_btn',
    "Искать по названию",
    'en',
    'he',
    'ar'
    ],

    # find_by_firm_btn
    ["find_by_firm_btn",
    "Искать по Производителю",
    'en',
    'he',
    'ar'
    ],

    # find_by_category_btn
    ["find_by_category_btn",
    "Искать по Категории",
    'en',
    'he',
    'ar'
    ],

    # generete_csv_btn
    ["generete_csv_btn",
    "Сгенирировать CSV файл",
    'en',
    'he',
    'ar'
    ],

    # find_by_category_btn
    ["find_by_category_btn",
    "Найти по категории",
    'en',
    'he',
    'ar'
    ],

    # set_item_id_btn
    ["set_item_id_btn",
    "Ай-ди товара",
    'en',
    'he',
    'ar'
    ],

    # set_item_name_btn
    ["set_item_name_btn",
    "Название товара",
    'en',
    'he',
    'ar'
    ],

    # set_item_picture_btn
    ["set_item_picture_btn",
    "Фото товара",
    'en',
    'he',
    'ar'
    ],

    # set_item_firm_btn
    ["set_item_item_firm_btn",
    "Изготовитель",
    'en',
    'he',
    'ar'
    ],

    # set_item_item_in_stock_btn
    ["set_item_item_in_stock_btn",
    "Есть на складе",
    'en',
    'he',
    'ar'
    ],

    # set_item_barcode_btn
    ["set_item_barcode_btn",
    "Штрихкод",
    'en',
    'he',
    'ar'
    ],

    # set_item_input_cost_btn
    ["set_item_input_cost_btn",
    "Цена закупки",
    'en',
    'he',
    'ar'
    ],

    # set_item_output_cost_btn
    ["set_item_output_cost_btn",
    "Цена продажи",
    'en',
    'he',
    'ar'
    ],

    # set_item_creation_date_btn
    ["set_item_creation_date_btn",
    "Дата создания",
    'en',
    'he',
    'ar'
    ],

    # set_item_exp_date_btn
    ["set_item_exp_date_btn",
    "Срок годности",
    'en',
    'he',
    'ar'
    ],

    # set_item_package_num_btn
    ["set_item_package_num_btn",
    "Номер упаковки",
    'en',
    'he',
    'ar'
    ],

    # set_item_item_count_btn
    ["set_item_item_count_btn",
    "Колличестов товар",
    'en',
    'he',
    'ar'
    ],

    # back_btn
    ["back_btn",
    "Назад",
    'Back',
    'חזרה',
    'ar'
    ],

    # done_btn
    ["done_btn",
    "Сохранить",
    'Save',
    'שמירה',
    'ar'
    ],

    # done_btn
    ["done_btn",
    "Сохранить",
    'Save',
    'שמירה',
    'ar'
    ]


]

IMPORTANT_BTN = "❗"
ALLOW_BTN = "✅"
DENI_BTN = "❌"


# Check if text_id registred in db
def id_in_db(content_id):

    sql.execute(f"SELECT * FROM bot_text WHERE text_id = '{content_id}'")
    if sql.fetchone() is None:
        result = False
    else:
        result = True


    return result


# add text content to texts db
def add_if_not_in_db(content_id, ru, en, he, ar):
    sql.execute(f"INSERT INTO bot_text VALUES('{str(content_id)}', '{str(ru)}', '{str(en)}', '{str(he)}', '{str(ar)}')")
    db.commit()


# return coontent by land ang id
def content_by_lang(content_id, lang):
    result = None
    sql.execute(f"SELECT * FROM bot_text WHERE text_id = '{content_id}'")
    for content_id, ru, en, he, ar in sql.fetchall():
        content = {"ru": ru,
                   "en": en,
                   "he": he,
                   "ar": ar}
        result = content[lang]



    return result


# update text content in texts db
def update_content(content_id, lang, new_content):
    db, sql = configurer.sysDB()

    sql.execute(f"UPDATE bot_text SET {str(lang)} = '{str(new_content)}' WHERE text_id = '{str(content_id)}'")
    db.commit()

    configurer.close_db(db)


def db_text_updater():
    print(f"[+] DB text updater started")
    t1 = datetime.datetime.now()

    for content_id, ru, en, he, ar in contents:
        if not id_in_db(content_id):
            add_if_not_in_db(content_id, ru, en, he, ar)
        for i in [['ru', ru], ['en', en], ['he', he], ['ar', ar]]:
            if content_by_lang(content_id, i[0]) != i[1]:
                update_content(content_id, i[0], i[1])
    t2 = datetime.datetime.now()
    result = str(t2-t1).split(":")[-1]

    print(f"[+] DB text updater done!")
    print(f"[+] Timer: {result}s")


th = threading.Thread(target=db_text_updater)
th.daemon = True
th.start()
threading.main_thread()


# get texts for regular use
def get_text(user_id, text_id):
    if user_id in ["ru", "en", "he", "ar"]:
        lng = user_id
    else:
        lng = configurer.Lang(user_id).get()
    if lng != None:
        return content_by_lang(text_id, lng)





