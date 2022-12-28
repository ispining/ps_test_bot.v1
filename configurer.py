import datetime
import os
import random
import threading

from config import *


GLOBAL_VERBOSE = False
ADMIN_PANEL_ALLOWED_STATUSES = ['admin']
AGENT_PANEL_ALLOWED_STATUSES = ['admin']
# Lang model
class Lang:
    def __init__(self, user_id=None):
        self.user_id = user_id

        db.rollback()
        sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_lang(
user_id TEXT PRIMARY KEY,
lang TEXT
        )""")
        db.commit()

    def get(self):
        if self.user_id != None:
            cmd = f"SELECT * FROM mainapp_lang WHERE user_id = '{str(self.user_id)}'"
            sql.execute(cmd)
            if sql.fetchone() is None:
                sql.execute(f"INSERT INTO mainapp_lang VALUES('{str(self.user_id)}', 'he')")
                return "None"
            else:
                sql.execute(cmd)
                for user_id, lang in sql.fetchall():
                    return lang

        else:
            result = []
            cmd = "SELECT * FROM mainapp_lang"
            sql.execute(cmd)
            for user_id, lang in sql.fetchall():
                result.append({"user_id": str(user_id), "lang": str(lang)})
            return result

    def set(self, new):

        sql.execute(f"UPDATE mainapp_lang SET lang = '{str(new)}' WHERE user_id = '{str(self.user_id)}'")
        db.commit()


# Lead model
class Lead:
    def __init__(self):
        self.user_id = None
        self.first_name = None
        self.last_name = None
        self.teudat_zeut = None
        self.picture = None
        self.status = None
        self.country = None
        self.city = None
        self.address = None
        self.phone1 = None
        self.phone2 = None
        self.email = None
        self.reg_date = None
        self.birth_date = None
        self.agent_id = None
        self.special_files = None

        def preDB():

            db, sql = sysDB()

            sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_lead(
            user_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            teudat_zeut TEXT,
            picture TEXT,
            family_ids TEXT,
            status TEXT,
            country TEXT,
            city TEXT,
            address TEXT,
            phone1 TEXT,
            phone2 TEXT,
            email TEXT,
            reg_date TEXT,
            birth_date TEXT,
            agent_id TEXT,
            special_files TEXT
            )""")
            db.commit()

            close_db(db)

        preDB()

    def get(self, by='user_id', value=None):
        result = []
        cmd = f"SELECT * FROM mainapp_lead WHERE {by} = '{str(value)}'"

        sql.execute(cmd)
        fetchall = sql.fetchall()
        for user_id, first_name, last_name, teudat_zeut, picture, family_ids, status, country, city, address, phone1, phone2, email, reg_date, birth_date, agent_id in fetchall:
            r = {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "teudat_zeut": teudat_zeut,
                "picture": picture,
                "family_ids": family_ids,
                "status": status,
                "country": country,
                "city": city,
                "address": address,
                "phone1": phone1,
                "phone2": phone2,
                "email": email,
                "reg_date": reg_date,
                "birth_date": birth_date,
                "agent_id": agent_id
            }
            if by in ['user_id', 'teudat_zeut', 'email', 'phone1, phone2']:
                return r
            else:
                result.append(r)

        return result

    def set(self, by="user_id", search_value=None, column=None, value=None, verbose=True):

        sql.execute(f"SELECT * FROM mainapp_lead WHERE {str(by)} = '{str(search_value)}'")

        len_fetch = len(sql.fetchall())

        if len_fetch == 1:
            sql.execute(f"UPDATE mainapp_lead SET {str(column)} = '{str(value)}' WHERE {str(by)} = '{str(search_value)}'")
            db.commit()
            if verbose:
                print("[+] Value edited")

        elif len_fetch < 1:
            if verbose:
                print("[-] Can`t set values.\nNo matches")
        elif len_fetch > 1:
            if verbose:
                print("[-] Can`t set values.\nA lot of matches")

    def new(self):

        sql.execute(f"""INSERT INTO mainapp_lead VALUES(
        '{str(self.user_id)}', 
        '{str(self.first_name)}', 
        '{str(self.last_name)}', 
        '{str(self.teudat_zeut)}', 
        '{str(self.picture)}', 
        '{str(self.status)}', 
        '{str(self.country)}', 
        '{str(self.city)}', 
        '{str(self.address)}', 
        '{str(self.phone1)}', 
        '{str(self.phone2)}', 
        '{str(self.email)}', 
        '{str(self.reg_date)}', 
        '{str(self.birth_date)}', 
        '{str(self.agent_id)}',
        '{str(self.special_files)}')""")
        db.commit()


# Worker model
class Worker:
    def __init__(self, user_id=None):
        def preDB():

            sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_worker(
            user_id TEXT PRIMARY KEY,
            vip TEXT,
            reg_date TEXT,
            special_files TEXT)""")
            db.commit()

        preDB()

        self.user_id = user_id
        self.vip = None
        self.reg_date = None
        self.special_files = None

    def get(self):

        if self.user_id == None:
            sql.execute(f"SELECT * FROM mainapp_worker")
            fAll = sql.fetchall()
            for user_id, vip, reg_date, special_files in fAll:
                return {"user_id": user_id, "vip": vip, "reg_date": reg_date, "special_files": special_files}

    def set(self, by="user_id", search_value=None, column=None, value=None, verbose=True):

        sql.execute(f"UPDATE mainapp_worker SET {str(column)} = '{str(value)}' WHERE {by} = '{str(search_value)}'")
        db.commit()


        if verbose:
            print("[+] Value saved")

    def new(self):

        sql.execute(f"INSERT INTO mainapp_worker VALUES('{str(self.user_id)}', '{str(self.vip)}', '{str(self.reg_date)}', '{str(self.special_files)}')")
        db.commit()


# Staff model
class Staff:
    def __init__(self, user_id=None):
        def preDB():

            sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_staff(
            user_id TEXT PRIMARY KEY,
            vip TEXT,
            reg_date TEXT,
            special_files TEXT)""")
            db.commit()

        preDB()

        self.user_id = user_id
        self.status = None
        self.vip = None
        self.reg_date = None
        self.special_files = None

    def get(self):

        if self.user_id == None:
            result = []
            sql.execute(f"SELECT * FROM mainapp_staff")
            fAll = sql.fetchall()
            for user_id, status, vip, reg_date, special_files in fAll:
                result.append({"user_id": user_id, "status": status, "vip": vip, "reg_date": reg_date, "special_files": special_files})
            return result
        elif self.user_id != None:
            sql.execute(f"SELECT * FROM mainapp_staff WHERE user_id = '{str(self.user_id)}'")
            fAll = sql.fetchall()
            for user_id, status, vip, reg_date, special_files in fAll:
                return {"user_id": user_id, "status": status, "vip": vip, "reg_date": reg_date, "special_files": special_files}

    def set(self, by="user_id", search_value=None, column=None, value=None, verbose=True):

        sql.execute(f"UPDATE mainapp_staff SET {str(column)} = '{str(value)}' WHERE {by} = '{str(search_value)}'")
        db.commit()


        if verbose:
            print("[+] Value saved")

    def new(self):

        sql.execute(f"INSERT INTO mainapp_staff VALUES('{str(self.user_id)}', '{self.status}', '{str(self.vip)}', '{str(self.reg_date)}', '{str(self.special_files)}')")
        db.commit()


# firm model
class Firm:
    def __init__(self):
        def preDB():

            sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_firm(
            ident_id TEXT PRIMARY KEY,
            firm_name TEXT,
            picture TEXT,
            contact_id TEXT,
            phone TEXT,
            site TEXT,
            email TEXT,
            reg_date TEXT,
            special_files TEXT
            )""")
            db.commit()

        preDB()
        self.ident_id = None
        self.firm_name = None
        self.picture = None
        self.contact_id = None
        self.phone = None
        self.site = None
        self.email = None
        self.reg_date = None
        self.special_files = None

    def get(self, by='ident_id', value=None):
        cmd = f"SELECT * FROM mainapp_firm WHERE {by} = '{str(value)}'"

        sql.execute(cmd)
        for ident_id, firm_name, picture, contact_id, phone, site, email, reg_date, special_files in sql.fetchall():
            return {
                "ident_id": ident_id,
                "firm_name": firm_name,
                "picture": picture,
                "contact_id": contact_id,
                "phone": phone,
                "site": site,
                "email": email,
                "reg_date": reg_date,
                "special_files": special_files
            }

    def set(self, by="ident_id", search_value=None, column=None, value=None, verbose=True):

        sql.execute(f"UPDATE mainapp_worker SET {str(column)} = '{str(value)}' WHERE {by} = '{str(search_value)}'")
        db.commit()


        if verbose:
            print("[+] Value saved")

    def new(self):

        sql.execute(f"INSERT INTO mainapp_worker VALUES('{str(self.ident_id)}', '{str(self.firm_name)}', '{str(self.picture)}', '{str(self.contact_id)}', '{str(self.phone)}', '{str(self.site)}', '{str(self.email)}', '{str(self.reg_date)}', '{str(self.special_files)}')")
        db.commit()

    def listall(self):
        result = []
        sql.execute(f"SELECT * FROM mainapp_worker")
        for ident_id, firm_name, picture, contact_id, phone, site, email, reg_date, special_files in sql.fetchall():
            result.append({
                "ident_id": ident_id,
                "firm_name": firm_name,
                "picture": picture,
                "contact_id": contact_id,
                "phone": phone,
                "site": site,
                "email": email,
                "reg_date": reg_date,
                "special_files": special_files
            })
        return result

    def affiliate_count(self):
        afs = Affiliate().get(by="firm_id")


# Affiliate model
class Affiliate:
    def __init__(self):
        def preDB():

            sql.executef(f"""CREATE TABLE IF NOT EXISTS mainapp_affiliate(
            affiliate_id TEXT PRIMARY KEY,
            affiliate_name TEXT,
            firm_id TEXT,
            country TEXT,
            city TEXT,
            location TEXT,
            affiliate_percent TEXT,
            phone1 TEXT,
            phone2 TEXT,
            email TEXT,
            profile_picture TEXT,
            status TEXT,
            contact_id TEXT,
            reg_date TEXT,
            special_files TEXT
            )""")
            db.commit()

        preDB()
        self.affiliate_id = None
        self.affiliate_name = None
        self.firm_id = None
        self.country = None
        self.city = None
        self.location = None
        self.affiliate_percent = None
        self.phone1 = None
        self.phone2 = None
        self.email = None
        self.picture = None
        self.status = None
        self.contact_id = None
        self.reg_date = None
        self.files = None

    def get(self, by='affiliate_id', value=None):
        result = []
        sql.execute(f"SELECT * FROM mainapp_affiliate WHERE {str(by)} = '{str(value)}'")

        for a_id, a_name, firm_id, country, city, location, a_percent, phone1, phone2, email, picture, status, contact_id, reg_date, special_files in sql.fetchall():
            result.append({
                "id": a_id,
                "name": a_name,
                "firm_id": firm_id,
                "country": country,
                "city": city,
                "location": location,
                "affiliate_percent": a_percent,
                "phone1": phone1,
                "phone2": phone2,
                "email": email,
                "picture": picture,
                "status": status,
                "contact_id": contact_id,
                "reg_date": reg_date,
                "files": special_files
            })
        return result

    def set(self, by="affiliate_id", search_value=None, column=None, value=None, verbose=True):

        sql.execute(f"UPDATE mainapp_affiliate SET {str(column)} = '{str(value)}' WHERE {by} = '{str(search_value)}'")
        db.commit()


        if verbose:
            print("[+] Value saved")

    def new(self):
        sql.execute(f"""INSERT INTO mainapp_worker VALUES(
        '{str(self.affiliate_id)}', 
        '{str(self.affiliate_name)}', 
        '{str(self.firm_id)}', 
        '{str(self.country)}', 
        '{str(self.city)}', 
        '{str(self.location)}', 
        '{str(self.email)}', 
        '{str(self.affiliate_percent)}', 
        '{str(self.phone1)}', 
        '{str(self.phone2)}', 
        '{str(self.email)}', 
        '{str(self.picture)}', 
        '{str(self.status)}', 
        '{str(self.contact_id)}', 
        '{str(self.reg_date)}', 
        '{str(self.files)}'
        )""")
        db.commit()


# Stock model
class Stock:
    def __init__(self):
        def preDB():

            sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_stock(
            ident_id TEXT PRIMARY KEY,
            item_id TEXT,
            name TEXT,
            picture TEXT,
            item_firm TEXT,
            barcode TEXT,
            input_cost TEXT,
            output_cost TEXT,
            creation_date TEXT,
            exp_date TEXT,
            package_num TEXT,
            item_count TEXT,
            in_stock TEXT,
            special_files TEXT
            )""")
            db.commit()

        preDB()

        self.ident_id = None
        self.item_id = None
        self.name = None
        self.picture = None
        self.item_firm = None
        self.barcode = None
        self.input_cost = None
        self.output_cost = None
        self.creation_date = None
        self.exp_date = None
        self.package_num = None
        self.item_count = None
        self.in_stock = None
        self.special_files = None

    def get(self, by='ident_id', value=None):

        sql.execute(f"SELECT * FROM mainapp_stock WHERE {by} = '{value}'")
        for ident_id, item_id, name, picture, item_firm, barcode, input_cost, output_cost, creation_date, exp_date, package_num, item_count, in_stock, files in sql.fetchall():
            return {
                "ident_id": ident_id,
                "item_id": item_id,
                "name": name,
                "picture": picture,
                "item_firm": item_firm,
                "barcode": barcode,
                "input_cost": input_cost,
                "output_cost": output_cost,
                "creation_date": creation_date,
                "exp_date": exp_date,
                "package_num": package_num,
                "item_count": item_count,
                "in_stock": in_stock,
                "files": files
            }

    def set(self, by="ident_id", search_value=None, column=None, value=None, verbose=GLOBAL_VERBOSE):

        sql.execute(f"UPDATE mainapp_stock SET {str(column)} = '{str(value)}' WHERE {by} = '{str(search_value)}'")
        db.commit()


        if verbose:
            print("[+] Value saved")

    def new(self):
        sql.execute(f"""INSERT INTO mainapp_stock VALUES(
        '{str(self.ident_id)}', 
        '{str(self.item_id)}', 
        '{str(self.name)}', 
        '{str(self.picture)}', 
        '{str(self.item_firm)}', 
        '{str(self.barcode)}', 
        '{str(self.input_cost)}', 
        '{str(self.output_cost)}', 
        '{str(self.creation_date)}', 
        '{str(self.exp_date)}', 
        '{str(self.package_num)}', 
        '{str(self.item_count)}', 
        '{str(self.in_stock)}', 
        '{str(self.special_files)}'
        )""")
        db.commit()

    def remove(self, column: str):
        sql.execute(f"UPDATE mainapp_stock SET {column} = 'None' WHERE item_id = '{self.item_id}' OR ident_id  = '{self.item_id}'")
        db.commit()


# Text model
class Text:
    def __init__(self, user_id=None, lang=None):

        def preDB():

            sql.execute(f"""CREATE TABLE IF NOT EXISTS bot_text(
            text_id TEXT PRIMARY KEY,
            ru TEXT,
            en TEXT,
            he TEXT,
            ar TEXT
            )""")
            db.commit()

        preDB()

        self.user_id = user_id
        self.lang = lang

    def get(self, text_id):

        sql.execute(f"SELECT * FROM bot_text WHERE text_id = '{str(text_id)}'")
        result = sql.fetchall()

        lng = "he"
        if self.user_id != None:
            lng = Lang(self.user_id).get().lower()
        elif self.lang != None:
            lng = self.lang.lower()

        for _, ru, en, he, ar in result:
            if lng == "ru":
                return ru
            elif lng == "en":
                return en
            elif lng == "he":
                return he
            elif lng == "ar":
                return ar

    def set(self, text_id, new):
        if self.lang != None:

            sql.execute(f"UPDATE bot_text SET {str(self.lang)} = '{str(new)}' WHERE text_id = '{str(text_id)}'")
            db.commit()

        else:
            print("[-] Cannot set new text without selected language")


# Categories model
class Categories:
    def __init__(self, cat_id=None, ru="ru", en="en", he="he", ar="ar"):

        sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_categories(
        cat_id TEXT PRIMARY KEY,
        ru TEXT,
        en TEXT,
        he TEXT,
        ar TEXT
        )""")
        db.commit()

        self.cat_id = cat_id
        self.ru = ru
        self.en = en
        self.he = he
        self.ar = ar

    def exists(self):

        sql.execute(f"SELECT * FROM mainapp_categories WHERE cat_id = '{str(self.cat_id)}'")
        if sql.fetchone() is None:
            r = False
        else:
            r = True
        return r

    # First set all vars
    def add(self):

        if not self.exists():

            """
Example:

c = Categories()
c.cat_id = ""
c.ru = ""
c.he = ""
c.en = ""
c.ar = ""
c.add_category()
            
            """

            sql.execute(f"INSERT INTO mainapp_categories VALUES ('{str(self.cat_id)}', '{str(self.ru)}', '{str(self.he)}', '{str(self.en)}', '{str(self.ar)}'")
            db.commit()
        else:
            if self.ru != "ru":
                sql.execute(f"UPDATE mainapp_categories SET ru = '{self.ru}' WHERE cat_id = '{str(self.cat_id)}'")
                db.commit()
            elif self.he != "he":
                sql.execute(f"UPDATE mainapp_categories SET he = '{self.he}' WHERE cat_id = '{str(self.cat_id)}'")
                db.commit()
            elif self.en != "en":
                sql.execute(f"UPDATE mainapp_categories SET en = '{self.en}' WHERE cat_id = '{str(self.cat_id)}'")
                db.commit()
            elif self.ar != "ar":
                sql.execute(f"UPDATE mainapp_categories SET ar = '{self.ar}' WHERE cat_id = '{str(self.cat_id)}'")
                db.commit()

    def remove(self):

        sql.execute(f"DELETE FROM mainapp_categories WHERE item_id = '{str(self.cat_id)}'")
        db.commit()

    def list_categories_id(self):
        result = []

        sql.execute(f"SELECT * FROM mainapp_categories")
        for i in sql.fetchall():
            result.append(i[0])

        return result

    def show_content(self, user_id=None, lang=None):
        result = None
        if user_id != None:
            lang = Lang(user_id).get()
        if any((lang != None, user_id != None)):

            sql.execute(f"SELECT * FROM mainapp_categories WHERE cat_id = '{str(self.cat_id)}'")
            for _, ru, en, he, ar in sql.fetchall():
                result = {"ru": ru, "en": en, "he": he, "ar": ar}[lang]

        return result


# Catlinks model
class Catlinks:
    def __init__(self, ident_id=None, item_id=None, cat_id=None):

        sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_catlinks(
        ident_id TEXT PRIMARY KEY,
        item_id TEXT,
        cat_id TEXT
        )""")
        db.commit()
        self.ident_id = ident_id
        self.item_id = item_id
        self.cat_ids = cat_id

    def exists(self):

        sql.execute(f"SELECT * FROM mainapp_catlink WHERE item_id = '{self.item_id} AND cat_id = '{self.cat_ids}'")
        if sql.fetchone() is None:
            r = False
        else:
            r = True

        return r

    def add(self):
        if not self.exists():

            sql.execute(f"INSERT INTO mainapp_catlink VALUES ('{str(self.ident_id)}', '{str(self.item_id)}', '{self.cat_ids}')")
            db.commit()

        else:
            print("[-] Error! Catlink already exists")

    def remove(self):

        if self.cat_ids != None:
            sql.execute(f"DELETE FROM mainapp_catlink WHERE item_id = '{self.item_id} AND cat_ids = '{self.cat_ids}'")
            db.commit()
        else:
            sql.execute(f"DELETE FROM mainapp_catlink WHERE item_id = '{self.item_id}")
            db.commit()

    def list_item_categories(self):
        if not self.exists():
            result = []

            sql.execute(f"SELECT * FROM mainapp_catlink WHERE item_id = '{self.item_id}'")
            for cat_link in sql.fetchall():
                result.append(cat_link[2])


            return result


# CSV convert tools
class Csv:
    CSV_PATH = "/sources/csv/"

    def __init__(self, filename, ):
        self.filename = filename
        self.content = ''

    def generate_csv(self):
        with open(os.getcwd() + self.CSV_PATH + self.filename, "w") as file:
            file.write(self.content)


    def categories(self, filter: str=None) -> str:

        self.content = "Category id;Russian;English;Hebrew;Arabic\n"
        sql.execute(f"SELECT * FROM mainapp_categories")
        for row in sql.fetchall():
           for item in row:
               self.content += f"{item};"
           self.content += "\n"
        self.generate_csv()

        return os.getcwd() + self.CSV_PATH + self.filename


    def items(self):
        self.content = "ident_id;name;item_firm;barcode;input_cost;output_cost;item_count\n"
        sql.execute(f"SELECT * FROM mainapp_stock")
        for _, item_ident, name, _____, item_firm, barcode, input_cost, output_cost, __, ___, item_count, ____ in sql.fetchall():
            self.content += f"{item_ident};{name};{item_firm};{barcode};{input_cost};{output_cost};{item_count}\n"
        self.generate_csv()

        return os.getcwd() + self.CSV_PATH + self.filename


    def leads(self):
        self.content = "User id;First Name;Last Name;Teudat Zeut;Country;City;Address;Phone1;Phone2;email;Reg Date;Birth Date;Agent id\n"

        sql.execute(f"SELECT * FROM mainapp_lead")
        for user_id, fn, ln, tz, _, status, country, city, address, p1, p2, email, reg_date, b_d, agent_id, __ in sql.fetchall():
            self.content += f"{user_id};{fn};{ln};{tz};{country};{city};{address};{p1};{p2};{email};{reg_date};{b_d};{agent_id}\n"
        self.generate_csv()


        return os.getcwd() + self.CSV_PATH + self.filename


# Random tools
class Randomizer:
    def __init__(self):
        self.ineg = "0123456789"
        self.low_str = "abcdefghijklmnopqrstuvwxyz"
        self.high_str = self.low_str.upper()

    def lower_with_int(self, char_size=9):
        r = ""
        for i in range(char_size):
            r += random.choice(self.ineg+self.low_str)

        return r


# Pre adding to item DB
class TG_item_pre_add:
    def __init__(self, item_id=None, item_name=None, picture=None,item_firm=None,
                 barcode=None, input_cost=None, output_cost=None, item_count=None):
        def preDB():

            sql.execute(f"""CREATE TABLE IF NOT EXISTS bot_pre_item(
            item_id TEXT PRIMARY KEY,
            name TEXT,
            picture TEXT,
            firm_id TEXT,
            barcode TEXT,
            input_cost TEXT,
            output_cost TEXT,
            item_count TEXT
            )""")
            db.commit()

        preDB()

        self.item_id = item_id
        self.item_name = item_name
        self.picture = picture
        self.item_firm = item_firm
        self.barcode = barcode
        self.input_cost = input_cost
        self.output_cost = output_cost
        self.item_count = item_count

    def exists(self):

        sql.execute(f"SELECT * FROM bot_pre_item WHERE item_id = '{str(self.item_id)}'")
        if sql.fetchone() is None:
            r = False
        else:

            r = True

        return r

    def add(self):

        if self.exists():
            if self.item_name != None:
                sql.execute(f"UPDATE bot_pre_item SET name = '{str(self.item_name)}' WHERE item_id = '{str(self.item_id)}'")
                db.commit()
            if self.picture != None:
                sql.execute(f"UPDATE bot_pre_item SET picture = '{str(self.picture)}' WHERE item_id = '{str(self.item_id)}'")
                db.commit()
            if self.item_firm != None:
                sql.execute(f"UPDATE bot_pre_item SET firm_id = '{str(self.item_firm)}' WHERE item_id = '{str(self.item_id)}'")
                db.commit()
            if self.barcode != None:
                sql.execute(f"UPDATE bot_pre_item SET barcode = '{str(self.barcode)}' WHERE item_id = '{str(self.item_id)}'")
                db.commit()
            if self.input_cost != None:
                sql.execute(f"UPDATE bot_pre_item SET input_cost = '{str(self.input_cost)}' WHERE item_id = '{str(self.item_id)}'")
                db.commit()
            if self.output_cost != None:
                sql.execute(f"UPDATE bot_pre_item SET output_cost = '{str(self.output_cost)}' WHERE item_id = '{str(self.item_id)}'")
                db.commit()
            if self.item_count != None:
                sql.execute(f"UPDATE bot_pre_item SET item_count = '{str(self.item_count)}' WHERE item_id = '{str(self.item_id)}'")
                db.commit()

        elif not self.exists():
            sql.execute(f"INSERT INTO bot_pre_item VALUES ('{str(self.item_id)}', '{str(self.item_name)}', '{str(self.picture)}', '{str(self.item_firm)}', '{str(self.barcode)}', '{str(self.input_cost)}', '{str(self.output_cost)}', '{str(self.item_count)}')")
            db.commit()

    def show(self):
        sql.execute(f"SELECT * FROM bot_pre_item WHERE item_id = '{str(self.item_id)}'")
        for item_id, item_name, picture, item_firm, barcode, input_cost, output_cost, item_count in sql.fetchall():
            return {
                "item_id": item_id,
                "item_name": item_name,
                "picture": picture,
                "item_firm": item_firm,
                "barcode": barcode,
                "input_cost": input_cost,
                "output_cost": output_cost,
                "item_count": item_count
            }

    def send_to_main_db(self):

        st = Stock()
        sql.execute(f"SELECT * FROM bot_pre_item WHERE item_id = '{str(self.item_id)}'")
        for item_id, item_name, picture, item_firm, barcode, input_cost, output_cost, item_count in sql.fetchall():
            st.ident_id = item_id
            st.item_id = item_id
            st.name = item_name
            st.picture = picture
            st.item_firm = item_firm
            st.barcode = barcode
            st.input_cost = input_cost
            st.output_cost = output_cost
            st.item_count = item_count

            st.new()
            break

        self.remove_not_used()

    def remove_not_used(self):
        sql.execute(f"DELETE FROM bot_pre_item")
        db.commit()


def new_category_text(source):
    result = {}
    result['cat_id'] = Randomizer().lower_with_int()
    for row in source.split("\n"):
        if row.replace(" ", "") != "":
            if row.split("::")[0] in ["he", "en", "ru", "ar"]:
                result[row.split("::")[0]] = row.split("::")[1]

    return result


def timer(verbose=GLOBAL_VERBOSE):
    def decorator(func):
        t1 = datetime.datetime.now()
        r = func()
        t2 = datetime.datetime.now()
        if verbose:
            print("[+] Func_time: "+str(t2-t1).split(":")[-1])
        return r
    return decorator


def thread(with_timer=False):
    if with_timer:
        @timer
        def decorator(func):
            th = threading.Thread(target=func)
            th.daemon = True
            th.start()
            threading.main_thread()
        return decorator

    def decorator(func):
        th = threading.Thread(target=func)
        th.daemon = True
        th.start()
        threading.main_thread()
    return decorator


def id_admin(user_id):
    return Staff(user_id).get() in ADMIN_PANEL_ALLOWED_STATUSES


def is_agent(user_id):
    return Firm().get(by="contact_id", value=user_id) != None