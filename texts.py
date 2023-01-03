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
     '''<b>פאנל ניהול</b>
בחר פעולה''',
     'ar'
     ],

    #admin_items_msg
    ["admin_items_msg",
    """<b>Товары</b>
Данная платформа расчитана на не ограниченное колличество товаров, изза чего показ всех товаров не предусмотрен.
Вы можете сгенирировать список всех товаров в файл, и найти товар по идентификатору, названию, или производителю.""",

    '''<b>Products</b>
This platform is designed for an unlimited number of products, which is why the display of all products is not provided.
You can generate a list of all products in a file, and search for a product by id, name, or manufacturer.''',

    '''<b>מוצרים</b>
פלטפורמה זו מיועדת למספר בלתי מוגבל של מוצרים, וזו הסיבה שהתצוגה של כל המוצרים אינה מסופקת.
אתה יכול ליצור רשימה של כל המוצרים בקובץ, ולחפש מוצר לפי מזהה, שם או יצרן.''',

    '''<b> المنتجات </ b>
تم تصميم هذه المنصة لعدد غير محدود من المنتجات ، وهذا هو سبب عدم عرض جميع المنتجات.
يمكنك إنشاء قائمة بجميع المنتجات في ملف ، والبحث عن منتج حسب المعرف أو الاسم أو الشركة المصنعة.'''

    ],

    # admin_select_category_for_add_item
    ['admin_select_category_for_add_item',
    """<b>Добавление товара</b>
Выберите категорию товара, или добавьте новую категорию""",

    '''<b>Adding a product</b>
Select a product category, or add a new category''',

    '''<b>הוספת מוצר</b>
בחר קטגוריית מוצר, או הוסף קטגוריה חדשה''',

    '''<b> إضافة منتج </ b>
حدد فئة منتج ، أو أضف فئة جديدة'''
    ],

    # admin_add_item_panel
    ['admin_add_item_panel',
    """<b>Добавление товара</b>
Категория товара: {lcat}

Заполните следующие пункты.

❗ - Обязательные

""",

    '''<b>Adding a product</b>
Product category: {lcat}

Complete the following items.

❗ - Mandatory''',

    '''<b>הוספת מוצר</b>
קטגוריית מוצרים: {lcat}

השלם את הפריטים הבאים.

❗ - חובה''',

    '''<b> إضافة منتج </ b>
فئة المنتج: {lcat}

أكمل العناصر التالية.

❗ - إلزامي'''
    ],

    # admin_set_new_item_name_msg
    ['admin_set_new_item_name_msg',
    """<b>Добавление товара</b>
Категория товара: {lcat}

Введите название нового товара.
""",
    '''<b>Adding a product</b>
Product category: {lcat}

Enter the name of the new product''',
    '''<b>הוספת מוצר</b>
קטגוריית מוצרים: {lcat}

הזן את שם המוצר החדש''',
    '''<b> إضافة منتج </ b>
فئة المنتج: {lcat}

أدخل اسم المنتج الجديد'''
    ],

    # admin_set_new_item_picture_msg
    ['admin_set_new_item_picture_msg',
    """<b>Добавление товара</b>
Категория товара: {lcat}

Добавьте фото товара.

(Этот пункт не является обязательным!)
""",
    '''<b>Adding a product</b>
Product category: {lcat}

Add a product photo.

(This item is optional!)''',
    '''<b>הוספת מוצר</b>
קטגוריית מוצרים: {lcat}

הוסף תמונת מוצר.

(פריט זה הוא אופציונלי!)''',
    '''<b> إضافة منتج </ b>
فئة المنتج: {lcat}

أضف صورة المنتج.

(هذا العنصر اختياري!)'''
    ],

    # admin_set_new_item_firm_msg
    ['admin_set_new_item_firm_msg',
    """<b>Добавление товара</b>

Введите фирму производителя товара

(Этот пункт не является обязательным!)
""",
    '''<b>Adding a product</b>

Enter the manufacturer company

(This item is optional!)''',
    '''<b>הוספת מוצר</b>

הזן את חברת היצרן

(פריט זה הוא אופציונלי!)''',
    '''<b> إضافة منتج </ b>

أدخل الشركة المصنعة

(هذا العنصر اختياري!)'''
    ],

    # admin_set_new_item_barcode_msg
    ['admin_set_new_item_barcode_msg',
    """<b>Добавление товара</b>

Введите штрихкод товара

(Этот пункт не является обязательным!)
""",
    '''<b>Adding a product</b>

Enter the product barcode

(This item is optional!)''',
    '''<b>הוספת מוצר</b>

הזן את ברקוד המוצר

(פריט זה הוא אופציונלי!)''',
    '''<b> إضافة منتج </ b>

أدخل الرمز الشريطي للمنتج

(هذا العنصر اختياري!)'''
    ],

    # admin_set_new_item_input_cost_msg
    ['admin_set_new_item_input_cost_msg',
    """<b>Добавление товара</b>

Введите цену закупки товара.

(Этот пункт не является обязательным!)
""",
    '''<b>Adding a product</b>

Enter the purchase price of the item.

(This item is optional!)''',
    '''<b>הוספת מוצר</b>

הזן את מחיר הרכישה של הפריט.

(פריט זה הוא אופציונלי!)''',
    '''<b> إضافة منتج </ b>

أدخل سعر شراء العنصر.

(هذا العنصر اختياري!)'''
    ],

    # admin_set_new_item_output_cost_msg
    ['admin_set_new_item_output_cost_msg',
    """<b>Добавление товара</b>

Введите цену продажи товара.

(Этот пункт не является обязательным!)
""",
    '''<b>Adding a product</b>

Enter the selling price of the item.

(This item is optional!)''',
    '''<b>הוספת מוצר</b>

הזן את מחיר המכירה של הפריט.

(פריט זה הוא אופציונלי!)''',
    '''<b> إضافة منتج </ b>

أدخل سعر بيع العنصر.

(هذا العنصر اختياري!)'''
    ],

    # admin_set_new_item_count_msg
    ['admin_set_new_item_count_msg',
    """<b>Добавление товара</b>

Введите цену продажи товара.

(Этот пункт не является обязательным!)
""",
    '''<b>Adding a product</b>

Enter the selling price of the item.

(This item is optional!)''',
    '''<b>הוספת מוצר</b>

הזן את מחיר המכירה של הפריט.

(פריט זה הוא אופציונלי!)''',
    '''<b> إضافة منتج </ b>

أدخل سعر بيع العنصر.

(هذا العنصر اختياري!)'''
    ],

    # admin_add_cat_msg
    ['admin_add_cat_msg',
    """<b>Добавление категории</b>

Виберите категорию, в которой хотите добавить подкатегорию. 
Если вы хотите добавить и подкатегорию - нажмите на кнопку добавления
""",
    '''en''',
    '''he''',
    '''ar'''
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
    '''<b>Adding a category</b>

Submit the category name using the following template:

he::{content}
ru::{content}
en::{content}
ar::{content}

You can send multiple languages in one message.
Want to add just one language? So it is also possible''',
    '''<b>הוספת קטגוריה</b>

שלח את שם הקטגוריה באמצעות התבנית הבאה:

he::{תוכן}
ru::{תוכן}
en::{תוכן}
ar::{תוכן}

ניתן לשלוח מספר שפות בהודעה אחת.
רוצה להוסיף רק שפה אחת? אז זה גם אפשרי''',
    '''<b> إضافة فئة </ b>

أرسل اسم الفئة باستخدام النموذج التالي:

he :: {content}
ru :: {content}
en :: {content}
ar :: {content}

يمكنك إرسال لغات متعددة في رسالة واحدة.
هل تريد إضافة لغة واحدة فقط؟ لذلك من الممكن أيضا'''
    ],

    # admin_set_new_item_done_call
    ['admin_set_new_item_done_call',
    """Товар успешно добавлен.
""",
    'Product added successfully.',
    'המוצר נוסף בהצלחה.',
    'تمت إضافة المنتج بنجاح.'
    ],


    # admin_set_new_item_no_important_call
    ['admin_set_new_item_no_important_call',
    """ОШИБКА!
Вы не заполнили обязательные поля для заполнения""",
    '''ERROR!
You have not filled in the required fields''',
    '''טעות!
לא מילאת את השדות הנדרשים''',
    '''خطأ!
لم تقم بملء الحقول المطلوبة'''
    ],

    # admin_find_by_category_msg
    ['admin_find_by_category_msg',
    """<b>Товар по категории</b>
    
Выберите категорию товара""",
    '''<b>Product by category</b>
    
Select product category''',
    '''<b>מוצר לפי קטגוריה</b>
    
בחר קטגוריית מוצרים''',
    '''<b> المنتج حسب الفئة </ b>
    
حدد فئة المنتج'''
    ],

    # admin_find_by_id_msg
    ['admin_find_by_id_msg',
    """<b>Товар по категории</b>
    
Введите Ай ди товара""",
    '''<b>Product by category</b>
    
Enter product ID''',
    '''<b>מוצר לפי קטגוריה</b>
    
הזן מזהה מוצר''',
    '''<b> المنتج حسب الفئة </ b>
    
أدخل معرف المنتج'''
    ],

    # admin_find_by_name_msg
    ['admin_find_by_name_msg',
    """<b>Товар по категории</b>
    
Введите название товара""",
    '''<b>Product by category</b>
    
Enter product name''',
    '''<b>מוצר לפי קטגוריה</b>
    
הזן את שם המוצר''',
    '''<b> المنتج حسب الفئة </ b>
    
أدخل اسم المنتج'''
    ],

    # admin_find_by_category_selector_msg
    ['admin_find_by_category_selector_msg',
    """<b>Товар по категории</b>
    
Выберите товар""",
    '''<b>Product by category</b>
    
Choose a product''',
    '''<b>מוצר לפי קטגוריה</b>
    
בחר מוצר''',
    '''<b> المنتج حسب الفئة </ b>
    
اختر منتجًا'''
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
    '''<b>{name}</b>
    
<b>Item ID:</b> {item_id}
<b>Product name:</b> {name}
<b>Product photo:</b> {picture}
<b>Manufacturer:</b> {item_firm}
<b>Barcode:</b> {barcode}
<b>Purchase price:</b> {input_cost}NIS
<b>Sale price:</b> {output_cost}iss.
<b>In stock:</b> {item_count}pcs.
<b>Stock:</b> {in_stock}
<b>Files:</b> {special_files}''',
    '''<b>{name}</b>
    
<b>מזהה פריט:</b> {item_id}
<b>שם המוצר:</b> {name}
<b>תמונת מוצר:</b> {picture}
<b>יצרן:</b> {item_firm}
<b>ברקוד:</b> {barcode}
<b>מחיר רכישה:</b> {input_cost}₪
<b>מחיר מבצע:</b> {output_cost}₪.
<b>במלאי:</b> {item_count} יחידות.
<b>מלאי:</b> {in_stock}
<b>קבצים:</b> {special_files}''',
    '''<b> {name} </b>
    
<b> معرف العنصر: </ b> {item_id}
<b> اسم المنتج: </ b> {name}
<b> صورة المنتج: </ b> {picture}
<b> الشركة المصنعة: </ b> {item_firm}
<b> الرمز الشريطي: </ b> {barcode}
<b> سعر الشراء: </ b> {input_cost} شيكل
<b> سعر البيع: </ b> {output_cost} شيكل.
<b> في المخزن: </ b> {item_count} قطعة.
<b> المخزون: </ b> {in_stock}
<b> الملفات: </ b> {special_files}'''
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
    '''<b>Image / Product photo</b>
    
Select an action.''',
    '''<b>תמונה / תמונת מוצר</b>
    
בחר פעולה.''',
    '''<b> صورة / صورة منتج </ b>
    
حدد إجراء.'''
    ],

    # admin_item_panel_set_item_firm_msg
    ['admin_item_panel_set_item_firm_msg',
    """<b>Производитель товара</b>
    
Введите название конторы производителя
""",
    '''<b>Product manufacturer</b>
    
Enter the name of the manufacturer office''',
    '''<b>יצרן מוצר</b>
    
הזן את שם משרד היצרן''',
    '''<b> الشركة المصنعة للمنتج </ b>
    
أدخل اسم مكتب الشركة المصنعة'''
    ],

    # admin_item_panel_set_item_barcode_msg
    ['admin_item_panel_set_item_barcode_msg',
    """<b>Штрих-код товара</b>
    
Введите значения нового Штрих-кода
""",
    '''<b>Product barcode</b>
    
Enter new Barcode values''',
    '''<b>ברקוד מוצר</b>
    
הזן ערכי ברקוד חדשים''',
    '''<b> الرمز الشريطي للمنتج </ b>
    
أدخل قيم الباركود الجديدة'''
    ],

    # admin_item_panel_set_item_input_cost_msg
    ['admin_item_panel_set_item_input_cost_msg',
    """<b>Цена закупки товара</b>
    
Введите новую цену закупки для данного товара (только в цифрах)
""",
    '''<b>Product purchase price</b>
    
Enter a new purchase price for this item (only in numbers)''',
    '''<b>מחיר רכישת מוצר</b>
    
הזן מחיר רכישה חדש עבור פריט זה (במספרים בלבד)''',
    '''<b> سعر شراء المنتج </ b>
    
أدخل سعر شراء جديدًا لهذا العنصر (بالأرقام فقط)'''
    ],

    # admin_item_panel_set_item_output_cost_msg
    ['admin_item_panel_set_item_output_cost_msg',
    """<b>Цена продажи товара</b>
    
Введите новую цену продажи для данного товара (только в цифрах)
""",
    '''<b>Product selling price</b>
    
Enter a new selling price for this item (in numbers only)''',
    '''<b>מחיר מכירת מוצר</b>
    
הזן מחיר מכירה חדש עבור פריט זה (במספרים בלבד)''',
    '''<b> سعر بيع المنتج </ b>
    
أدخل سعر بيع جديدًا لهذه السلعة (بالأرقام فقط)'''
    ],

    # admin_set_item_special_files_msg
    ['admin_set_item_special_files_msg',
    """<b>Доп. файлы товара</b>
    
Перед вами список файлов, привязанных к товару.
Выберите нужный файл
""",
    '''<b>Product files</b>
    
Here is a list of files associated with the product.
Select the desired file''',
    '''<b>קבצי מוצר</b>
    
להלן רשימה של קבצים המשויכים למוצר.
בחר את הקובץ הרצוי''',
    '''<b> ملفات المنتج </ b>
    
فيما يلي قائمة بالملفات المرتبطة بالمنتج.
حدد الملف المطلوب'''
    ],

    # admin_item_panel_set_item_count_msg
    ['admin_item_panel_set_item_count_msg',
    """<b>Количество товара</b>
    
Введите новое количество для данного товара (только в цифрах)
""",
    '''<b>Product Quantity</b>

Enter a new quantity for this product (only in numbers)''',
    '''<b>כמות מוצר</b>

הזן כמות חדשה עבור מוצר זה (במספרים בלבד)''',
    '''<b> كمية المنتج </ b>

أدخل كمية جديدة لهذا المنتج (بالأرقام فقط)'''
    ],

    # item_not_found_msg
    ['item_not_found_msg',
    """<b>ОШИБКА</b>
    
Товар не был найден по указанным данным
""",
    '''<b>ERROR</b>
    
The product was not found according to the specified data''',
    '''<b>שגיאה</b>
    
המוצר לא נמצא על פי הנתונים שצוינו''',
    '''<b> خطأ </ b>
    
لم يتم العثور على المنتج وفقًا للبيانات المحددة'''
    ],

    # admin_edit_item_picture_msg
    ['admin_edit_item_picture_msg',
    """<b>Ред. фото товара</b>
    
Пришлите новое фото товара
""",
    '''<b>Product photo</b>
    
Submit a new product photo''',
    '''<b>תמונת מוצר</b>
    
שלח תמונת מוצר חדשה''',
    '''<b> صورة المنتج </ b>
    
إرسال صورة منتج جديد'''
    ],

    # new_value_setted_msg
    ['new_value_setted_msg',
    """<b>Сохранено</b>
    
Изменения были сохранены успешно
""",
    '''<b>Saved</b>
    
Changes were saved successfully''',
    '''<b>נשמר</b>
    
השינויים נשמרו בהצלחה''',
    '''<b> المحفوظة </ b>
    
تم حفظ التغييرات بنجاح'''
    ],

    # admin_special_files_update
    ['admin_special_files_update',
    """<b>Обновление доп. файлов</b>
    
Отправь новый файл, который заменит текущий
""",
    '''<b>Updating files</b>
    
Submit a new file to replace the current one''',
    '''<b>עדכון קבצים</b>
    
שלח קובץ חדש כדי להחליף את הקובץ הנוכחי''',
    '''<b> تحديث الملفات </ b>
    
قم بإرسال ملف جديد ليحل محل الملف الحالي'''
    ],

    # admin_firms_msg
    ['admin_firms_msg',
    """<b>Фирмы и филиалы</b>
    
Выберите фирму из списка
""",
    '''<b>Firms and branches</b>
    
Select a company from the list''',
    '''<b>חברות וסניפים</b>
    
בחר חברה מהרשימה''',
    '''<b> الشركات والفروع </ b>
    
حدد شركة من القائمة'''
    ],

    # admin_firm_panel_msg #
    ['admin_firm_panel_msg',
    """<b>Панель управления Фирмы</b>

<b>Идентификатор фирмы:</b> {firm_name}
<b>Название фирмы:</b> {firm_name}
<b>Филиалов:</b> {affiliate_count}

""",
    '''en''',
    '''he''',
    '''ar'''
    ],


    # admin_add_undercat_msg #
    ['admin_add_undercat_msg',
    """<b>Добавление подкатегории</b>

Отправьте название подкатегории с помощью следующего шаблона:

he::{content}
ru::{content}
en::{content}
ar::{content}

Можно отправить несколько языков в одном сообщении.
Хотите добавить только один язык? Так тоже можно
""",
    '''<b>Adding an under-category</b>

Submit the under-category name using the following template:

he::{content}
ru::{content}
en::{content}
ar::{content}

You can send multiple languages in one message.
Want to add just one language? So it is also possible''',
    '''<b>הוספת תת-קטגוריה</b>

שלח את שם התת-קטגוריה באמצעות התבנית הבאה:

he::{תוכן}
ru::{תוכן}
en::{תוכן}
ar::{תוכן}

ניתן לשלוח מספר שפות בהודעה אחת.
רוצה להוסיף רק שפה אחת? אז זה גם אפשרי''',
    '''ar'''
    ],



    # admin_categories_panel_msg #
    ['admin_categories_panel_msg',
    """<b>Категории</b>

Выберите категорию для добавления и просмотра подкатегорий.
Для добавления категории, нажмите кнопку добавить
""",
    '''en''',
    '''he''',
    '''ar'''
    ],



    # admin_category_panel_select_msg #
    ['admin_category_panel_select_msg',
    """<b>Подкатегории</b>

Выберите подкатегорию для ее удаления.
Для добавления подкатегории, нажмите кнопку добавить
""",
    '''en''',
    '''he''',
    '''ar'''
    ],


    # no_permissions_msg #
    ['no_permissions_msg',
    """<b>Не достаточно прав</b>

У вас не достаточно прав, для выполнения данного действия
""",
    '''en''',
    '''<b>שגיעה</b>

אין לך מספיק הרשאות לביצוע פעולה זו''',
    '''ar'''
    ],


    # admin_admins_msg #
    ['admin_admins_msg',
    """<b>Члены администрации</b>

Тут вы можете просматривать информацию о пользователях, которые имеют административный доступ.

Выберите нужный раздел
""",
    '''en''',
    '''he''',
    '''ar'''
    ],


    # admin_admins_adminview_msg #
    ['admin_admins_adminview_msg',
    """<b>Члены администрации</b>

Выберите Администратора из добавленых, либо добавьте нового
""",
    '''en''',
    '''he''',
    '''ar'''
    ],


    # admin_admins_add_admin_msg #
    ['admin_admins_add_admin_msg',
    """<b>Добавление администратора</b>

Введите ID пользователя, которого хотите назначить дминистратором.

""",
    '''en''',
    '''he''',
    '''ar'''
    ],


    # admin_already_exists_msg #
    ['admin_already_exists_msg',
    """<b>ОШИБКА</b>

Данный пользователь уже записан в базе данных как Админ.
Вы не можете добавить его повторно

""",
    '''en''',
    '''he''',
    '''ar'''
    ],


    # admin_admins_panel_msg #
    ['admin_admins_panel_msg',
    """<b>Просмотр Админа</b>

<b>Ай-ди пользователя: </b> {user_id}
<b>Имя пользователя: </b> {name}
<b>Юзернейм пользователя: </b> {username}
<b>Дата регистрации пользователя: </b> {reg_date}
""",
    '''en''',
    '''he''',
    '''ar'''
    ],


    # admin_remove_admin_removed_msg #
    ['admin_remove_admin_removed_msg',
    """Администратор удален успешно!""",
    '''en''',
    '''he''',
    '''ar'''
    ],







############# BUTTONS #############
    # items_btn
    ['items_btn',
    "Товары",
    'Items',
    'פריטים',
    'العناصر'
    ],

    # firms_btn
    ['firms_btn',
    "Фирмы",
    'Firms',
    'חברות',
    'الشركات'
    ],

    # add_btn
    ['add_btn',
    "Добавить",
    'Add',
    'לְהוֹסִיף',
    'يضيف'
    ],

    # find_by_id_btn
    ['find_by_id_btn',
    "Искать по Идентификатору",
    'Search by id',
    'חפש לפי מזהה',
    'البحث عن طريق معرف'
    ],

    # find_by_name_btn
    ['find_by_name_btn',
    "Искать по названию",
    'Search by name',
    'חפש לפי שם',
    'البحث عن طريق الإسم'
    ],

    # find_by_firm_btn
    ["find_by_firm_btn",
    "Искать по Производителю",
    'חפש לפי יצרן',
    'חפש לפי יצרן',
    'البحث عن طريق الشركة المصنعة'
    ],

    # find_by_category_btn
    ["find_by_category_btn",
    "Искать по Категории",
    'Search by Category',
    'חפש לפי קטגוריה',
    'البحث حسب الفئة'
    ],

    # generete_csv_btn
    ["generete_csv_btn",
    "Сгенирировать CSV файл",
    'Generate CSV file',
    'צור קובץ CSV',
    'إنشاء ملف CSV'
    ],

    # set_item_id_btn
    ["set_item_id_btn",
    "Ай-ди товара",
    'Item id',
    'מזהה פריט',
    'تعريف العنصر'
    ],

    # set_item_name_btn
    ["set_item_name_btn",
    "Название товара",
    'Item name',
    'שם הפריט',
    'اسم العنصر'
    ],

    # set_item_picture_btn
    ["set_item_picture_btn",
    "Фото товара",
    'Item photo',
    'תמונת פריט',
    'صورة العنصر'
    ],

    # set_item_firm_btn
    ["set_item_item_firm_btn",
    "Изготовитель",
    'Manufacturer',
    'יצרן',
    'الشركه المصنعه'
    ],

    # set_item_item_in_stock_btn
    ["set_item_item_in_stock_btn",
    "Есть на складе",
    'Available in stock',
    'זמין במלאי',
    'متوفر في المخزون'
    ],

    # set_item_barcode_btn
    ["set_item_barcode_btn",
    "Штрихкод",
    'Barcode',
    'ברקוד',
    'الباركود'
    ],

    # set_item_input_cost_btn
    ["set_item_input_cost_btn",
    "Цена закупки",
    'Purchase price',
    'מחיר רכישה',
    'سعر الشراء'
    ],

    # set_item_output_cost_btn
    ["set_item_output_cost_btn",
    "Цена продажи",
    'Sale price',
    'מחיר מבצע',
    'سعر البيع'
    ],

    # set_item_creation_date_btn
    ["set_item_creation_date_btn",
    "Дата создания",
    'Creation date',
    'תאריך יצירה',
    'تاريخ الإنشاء'
    ],

    # set_item_exp_date_btn
    ["set_item_exp_date_btn",
    "Срок годности",
    'Exp date',
    'תאריך תפוגה',
    'تاريخ انتهاء الصلاحية'
    ],

    # set_item_package_num_btn
    ["set_item_package_num_btn",
    "Номер упаковки",
    'Package Number',
    'מספר חבילה',
    'رقم الباقة'
    ],

    # set_item_item_count_btn
    ["set_item_item_count_btn",
    "Количество товара",
    'Quantity of Items',
    'כמות פריטים',
    'كمية العناصر'
    ],

    # back_btn
    ["back_btn",
    "Назад",
    'Back',
    'חזרה',
    'ظهر'
    ],

    # done_btn
    ["done_btn",
    "Сохранить",
    'Save',
    'שמירה',
    'أنقذ'
    ],

    # set_item_special_files_btn
    ["set_item_special_files_btn",
    "Доп. файлы",
    'Files',
    'קבצים',
    'الملفات'
    ],

    # remove_item_picture_btn
    ["remove_item_picture_btn",
    "Удалить фото товара",
    'Delete product photo',
    'מחיקת תמונת מוצר',
    'حذف صورة المنتج'
    ],

    # edit_item_picture_btn
    ["edit_item_picture_btn",
    "Ред. фото товара",
    'Edit item picture',
    'עריכת תמונת פריט',
    'تحرير صورة العنصر'
    ],

    # download_file
    ["download_file_btn",
    "Скачать файл",
    'Download file',
    'הורדת קובץ',
    'تحميل الملف'
    ],

    # update_file
    ["update_file",
    "Обновить файл",
    'Update File',
    'עדכון קובץ',
    'تحديث الملف'
    ],

    # remove_file
    ["remove_file",
    "Удалить файл",
    'Delete file',
    'מחיקת קובץ',
    'حذف الملف'
    ],

    # categories_btn
    ["categories_btn",
    "Категории",
    'Categories',
    'קטגוריות',
    'ar'
    ],

    # admins_btn
    ["admins_btn",
    "Администрация",
    'Administration',
    'הגדרת מנהלים',
    'ar'
    ],

    # admins_btn
    ["admins_set_btn",
    "Администраторы",
    'Administrators',
    'מנהלים',
    'ar'
    ],

    # developers_set_btn
    ["developers_set_btn",
    "Разработчики",
    'Developers',
    'מפתחים',
    'ar'
    ],

    # viewall_btn
    ["viewall_btn",
    "Просмотреть все",
    'View all',
    'לראות הכל',
    'ar'
    ],

    # remove_admin_btn
    ["remove_admin_btn",
    "Удалить Админа",
    'Remove admin',
    'מחיקת מנהל',
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





