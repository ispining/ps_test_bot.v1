import datetime
import threading

from config import *
from sources.csv import csvToDB

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
        # ADDRESS 2
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
            special_files TEXT,
            status TEXT)""")
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
            for user_id, vip, reg_date, special_files, status in fAll:
                result.append({"user_id": user_id, "status": status, "vip": vip, "reg_date": reg_date, "special_files": special_files})
            return result
        elif self.user_id != None:
            sql.execute(f"SELECT * FROM mainapp_staff WHERE user_id = '{str(self.user_id)}'")
            fAll = sql.fetchall()
            for user_id, vip, reg_date, special_files, status in fAll:
                return {"user_id": user_id, "status": status, "vip": vip, "reg_date": reg_date, "special_files": special_files}

    def set(self, by="user_id", search_value=None, column=None, value=None, verbose=True):

        sql.execute(f"UPDATE mainapp_staff SET {str(column)} = '{str(value)}' WHERE {by} = '{str(search_value)}'")
        db.commit()


        if verbose:
            print("[+] Value saved")

    def new(self):

        sql.execute(f"INSERT INTO mainapp_staff VALUES('{str(self.user_id)}', '{str(self.vip)}', '{str(self.reg_date)}', '{str(self.special_files)}',  '{self.status}')")
        db.commit()

    def list_by_status(self, status):
        sql.execute(f"SELECT * FROM mainapp_staff WHERE status = '{str(status)}'")
        return sql.fetchall()

    def remove_by_id(self):
        sql.execute(f"DELETE FROM mainapp_staff WHERE user_id = '{str(self.user_id)}'")
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
        # FIRM_AGENT
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
        return len(Affiliate().get(by="firm_id"))



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

            sql.execute(f"INSERT INTO mainapp_categories VALUES ('{str(self.cat_id)}', '{str(self.ru)}', '{str(self.en)}', '{str(self.he)}', '{str(self.ar)}')")
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


# Under-Categories
class UnderCats:
    def __init__(self, ident_id=None, cat_id=None, undercat_id=None,
                 ru=None, en=None, he=None, ar=None):
        def pre_db():
            sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_undercats(
            ident_id TEXT,
            cat_id TEXT,
            undercat_id TEXT,
            ru TEXT,
            en TEXT,
            he TEXT,
            ar TEXT
            )""")
            db.commit()
        self.ident_id = ident_id
        self.cat_id = cat_id
        self.undercat_id = undercat_id
        self.ru = ru
        self.en = en
        self.he = he
        self.ar = ar

        pre_db()

    def exists(self):
        sql.execute(f"SELECT * FROM mainapp_undercats WHERE ident_id = '{self.ident_id}'")
        if sql.fetchall() is None:
            return False
        else:
            return True

    def get(self) -> [list, dict]:
        result = []
        if self.undercat_id == None:
            cmd = f"SELECT * FROM mainapp_undercats WHERE cat_id = '{str(self.cat_id)}'"
        else:
            cmd = f"SELECT * FROM mainapp_undercats WHERE cat_id = '{str(self.cat_id)}' AND undercat_id = '{str(self.undercat_id)}'"

        sql.execute(cmd)
        undercat_lst = sql.fetchall()

        for row in undercat_lst:
            result.append({
                "ident_id": row[0],
                "cat_id": row[1],
                "undercat_id": row[2],
                "ru": row[3],
                "en": row[4],
                "he": row[5],
                "ar": row[6]
            })
        if all((self.cat_id!= None, self.cat_id != None)):
            if len(result) != 0:
                return result[0]
        return result

    def set(self) -> [None, dict]:
        if all((self.cat_id != None, self.undercat_id)):
            res = {"ru": self.ru, "en": self.en, "he": self.he, "ar": self.ar}

            updated = False

            for lng in ['ru', 'en', 'he', 'ar']:
                if res[lng] != None:
                    cmd = f"UPDATE mainapp_undercats SET {lng} = '{str(res[lng])}'"

                    if self.ident_id != None:
                        cmd += f"WHERE ident_id = '{str(self.ident_id)}'"
                        sql.execute(cmd)
                        db.commit()
                    elif all((self.cat_id != None, self.undercat_id != None)):
                        cmd += f"WHERE cat_id = '{str(self.cat_id)}' AND undercat_id = '{str(self.undercat_id)}'"
                        sql.execute(cmd)
                        db.commit()


                    if not updated:
                        updated = True

            if not updated:
                return self.add()
        else:
            print("""[-] Can't  add UnderCats.cat_id and UnderCats.undercat_id """, end="\n\n")

    def add(self):
        self.ident_id = Randomizer().lower_with_int()
        self.undercat_id = self.ident_id
        sql.execute(f"""INSERT INTO mainapp_undercats VALUES('{str(self.ident_id)}', '{str(self.cat_id)}', '{str(self.undercat_id)}', 
        '{str(self.ru)}', '{str(self.en)}', '{str(self.he)}', '{str(self.ar)}')""")
        db.commit()


        return self.ident_id

    def list_all_id(self):
        result = []
        sql.execute(f"SELECT * FROM mainapp_undercats WHERE cat_id = '{self.cat_id}'")
        for i in sql.fetchall():
            result.append(i[2])
        return result

    def show_content(self, user_id=None, lang=None):
        result = None
        if user_id != None:
            lang = Lang(user_id).get()
        if lang != None:
            sql.execute(f"SELECT * FROM mainapp_undercats WHERE undercat_id = '{str(self.undercat_id)}'")
            for _, __, ___,  ru, en, he, ar in sql.fetchall():
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

        sql.execute(f"SELECT * FROM mainapp_catlink WHERE item_id = '{self.item_id}' AND cat_id = '{self.cat_ids}'")
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

    def list_undercat_items(self):
        if not self.exists():
            result = []

            sql.execute(f"SELECT * FROM mainapp_catlink WHERE cat_id = '{self.cat_ids}'")
            for cat_link in sql.fetchall():
                result.append(cat_link[1])

            return result


class Names:

    class Item:
        def __init__(self, ident_id=None):
            def preDB():
                sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_item_names(
                ident_id TEXT PRIMARY KEY,
                ru TEXT,
                en TEXT,
                he TEXT,
                ar TEXT)""")
                db.commit()

            preDB()
            self.ident_id = ident_id

        def exists(self):
            sql.execute(f"SELECT * FROM mainapp_item_names WHERE ident_id = '{str(self.ident_id)}'")
            if sql.fetchone() is None:
                return False
            else:
                return True

        def set(self, ru=None, en=None, he=None, ar=None):
            if self.exists():
                if ru != None:
                    sql.execute(f"UPDATE mainapp_item_names SET ru = '{str(ru)}' WHERE ident_id = '{str(self.ident_id)}'")
                    db.commit()
                if en != None:
                    sql.execute(f"UPDATE mainapp_item_names SET ru = '{str(en)}' WHERE ident_id = '{str(self.ident_id)}'")
                    db.commit()
                if he != None:
                    sql.execute(f"UPDATE mainapp_item_names SET ru = '{str(he)}' WHERE ident_id = '{str(self.ident_id)}'")
                    db.commit()
                if ar != None:
                    sql.execute(f"UPDATE mainapp_item_names SET ru = '{str(ar)}' WHERE ident_id = '{str(self.ident_id)}'")
                    db.commit()

            else:
                sql.execute(f"INSERT INTO mainapp_item_names VALUES('{str(self.ident_id)}', '{str(ru)}', '{str(en)}', '{str(he)}', '{str(ar)}')")
                db.commit()

        def get(self):
            """
            :return: {"ident_id", "ru", "en","he", "ar"}
            """
            sql.execute(f"SELECT * FROM mainapp_item_names WHERE ident_id = '{str(self.ident_id)}'")
            for row in sql.fetchall():
                return {
                    "ident_id": row[0],
                    "ru": row[1],
                    "en": row[2],
                    "he": row[3],
                    "ar": row[4],
                }


class ItemConfig:
    def __init__(self, ident_id=None, buy_without_stock=False, can_review=True, one_by_one=False, recomended=False):
        def preDB():
            sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_item_configs(
            ident_id TEXT PRIMARY KEY,
            buy_without_stock TEXT, 
            can_review TEXT, 
            one_by_one TEXT, 
            recomended TEXT
            )""")
            db.commit()
        preDB()
        self.ident_id = ident_id
        self.buy_without_stock = buy_without_stock
        self.can_review = can_review
        self.one_by_one = one_by_one
        self.recomended = recomended

        if not self.exists():
            sql.execute(f"""INSERT INTO mainapp_item_configs VALUES (
            '{str(self.ident_id)}', 
            '{str(buy_without_stock)}', 
            '{str(can_review)}', 
            '{str(one_by_one)}', 
            '{str(recomended)}'
            )""")
            db.commit()

    def exists(self):
        sql.execute(f"SELECT * FROM mainapp_item_configs WHERE ident_id = '{str(self.ident_id)}'")
        if sql.fetchone() is None:
            return False
        else:
            return True

    def get(self):
        sql.execute(f"SELECT * FROM mainapp_item_configs WHERE ident_id = '{str(self.ident_id)}'")
        for row in sql.fetchall():
            ident_id = self.ident_id
            buy_without_stock = row[1]
            can_review = row[2]
            one_by_one = row[3]
            recomended = row[4]
            return {
                "ident_id": ident_id,
                "buy_without_stock": buy_without_stock,
                "can_review": can_review,
                "one_by_one": one_by_one,
                "recomended": recomended
            }

    def set(self):
        if self.buy_without_stock in [True, "True", False, "False", 0, "0", 1, "1"]:
            if self.buy_without_stock in [True, "True", 1, "1"]:
                self.buy_without_stock = "True"
            else:
                self.buy_without_stock = "False"

            sql.execute(f"UPDATE mainapp_item_configs SET buy_without_stock = '{str(self.buy_without_stock)}' WHERE ident_id = '{str(self.ident_id)}'")
            db.commit()

        if self.can_review in [True, "True", False, "False", 0, "0", 1, "1"]:
            if self.can_review in [True, "True", 1, "1"]:
                self.can_review = "True"
            else:
                self.can_review = "False"
            sql.execute(f"UPDATE mainapp_item_configs SET can_review = '{str(self.can_review)}' WHERE ident_id = '{str(self.ident_id)}'")
            db.commit()
        if self.one_by_one in [True, "True", False, "False", 0, "0", 1, "1"]:
            if self.one_by_one in [True, "True", 1, "1"]:
                self.one_by_one = "True"
            else:
                self.one_by_one = "False"
            sql.execute(f"UPDATE mainapp_item_configs SET one_by_one = '{str(self.one_by_one)}' WHERE ident_id = '{str(self.ident_id)}'")
            db.commit()
        if self.recomended in [True, "True", False, "False", 0, "0", 1, "1"]:
            if self.recomended in [True, "True", 1, "1"]:
                self.recomended = "True"
            else:
                self.recomended = "False"
            sql.execute(f"UPDATE mainapp_item_configs SET recomended = '{str(self.recomended)}' WHERE ident_id = '{str(self.ident_id)}'")
            db.commit()


# CSV convert tools
class Csv:
    CSV_PATH = "/sources/csv/"

    def __init__(self, filename):
        self.filename = filename
        self.content = ''

    def generate_csv(self):
        f = open(os.getcwd() + self.CSV_PATH + self.filename, "w")
        f.write(self.content)
        f.close()

    def upload_items(self, verbose=GLOBAL_VERBOSE) -> None:
        list_items = csvToDB.ImportFromCsv(self.filename).list_items()
        items_num = len(list_items)
        num = 1
        for item in list_items:

            num += 1

    def categories(self, filter: str=None) -> str:

        self.content = "Category id,Russian,English,Hebrew,Arabic\n"
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
        for item in sql.fetchall():
            self.content += f"{item[0]};{item[2]};{item[4]};{item[5]};{item[6]};{item[7]};{item[9]}\n"
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

    def lower_with_int(self, char_size: int = 9):
        r = ""
        for i in range(char_size):
            r += random.choice(self.ineg+self.low_str)

        return r

    def only_low_str(self, char_size: int = 9):
        r = ""
        for i in range(char_size):
            r += random.choice(self.low_str)

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


class Content:
    class Item:
        def __init__(self, ident_id=None):
            def preDB():
                sql.execute(f"""CREATE TABLE IF NOT EXISTS mainapp_item_content (
                ident_id TEXT PRIMARY KEY,
                btn_text TEXT,
                description TEXT,
                about TEXT,
                posted_by TEXT
                )""")
            preDB()
            self.ident_id = ident_id

        def exists(self):
            sql.execute(f"SELECT * FROM mainapp_item_content WHERE ident_id = '{str(self.ident_id)}'")
            if sql.fetchone() is None:
                return False
            else:
                return True

        def set(self, btn_text=None, description=None, about=None, posted_by=None):
            """
            format {'btn_text', 'description', 'about', 'posted_by'}

            :param btn_text: ident id for Names class
            :param description: ident id for Names class
            :param about: ident id for Names class
            :param posted_by: ident id for Names class
            :return:  None
            """
            if self.exists():
                if btn_text != None:
                    txt_id = self.get()['btn_text']
                    Names().Item(txt_id).set(he=btn_text)
                if description != None:
                    txt_id = self.get()['description']
                    Names().Item(txt_id).set(he=btn_text)
                if about != None:
                    txt_id = self.get()['about']
                    Names().Item(txt_id).set(he=btn_text)
                if posted_by != None:
                    txt_id = self.get()['posted_by']
                    Names().Item(txt_id).set(he=btn_text)

            else:
                names = Names()
                btn_id = "None"
                description_id = "None"
                about_id = "None"
                posted_by_id = "None"
                if btn_text != None:
                    try:
                        new_btn_id = Randomizer().only_low_str()
                        it = names.Item(ident_id=new_btn_id)
                        it.set(he=btn_text)
                        btn_id = new_btn_id
                    except:
                        pass
                if description != None:
                    try:
                        new_description_id = Randomizer().only_low_str()
                        it = names.Item(ident_id=new_description_id)
                        it.set(he=description)
                        description_id = new_description_id
                    except:
                        pass
                if about != None:
                    try:
                        new_about_id = Randomizer().only_low_str()
                        it = names.Item(ident_id=new_about_id)
                        it.set(he=about)
                        about_id = new_about_id
                    except:
                        pass
                if posted_by != None:
                    try:
                        new_posted_by_id = Randomizer().only_low_str()
                        it = names.Item(ident_id=new_posted_by_id)
                        it.set(he=about)
                        posted_by_id = new_posted_by_id
                    except:
                        pass

                sql.execute(f"INSERT INTO mainapp_item_content VALUES('{str(self.ident_id)}, {str(btn_id)}', '{str(description_id)}', '{str(about_id)}', '{str(posted_by_id)}')")
                db.commit()

        def get(self, lang=None):
            """

            :param lang: ru, en, he, ar
            :return: {"ident_id", "ident_id", "description", "about", "posted_by"}
            """
            sql.execute(f"SELECT * FROM mainapp_item_content WHERE ident_id = '{str(self.ident_id)}'")
            for row in sql.fetchall():
                if lang == None:
                    r = {
                        "ident_id": row[0],
                        "btn_text": Names().Item(row[1]).get(),
                        "description": Names().Item(row[2]).get(),
                        "about": Names().Item(row[3]).get(),
                        "posted_by": Names().Item(row[4]).get()
                    }
                else:
                    r = {
                        "ident_id": row[0],
                        "btn_text": Names().Item(row[1]).get()[lang],
                        "description": Names().Item(row[2]).get()[lang],
                        "about": Names().Item(row[3]).get()[lang],
                        "posted_by": Names().Item(row[4]).get()[lang]
                    }
                return r


def new_category_text(source):
    result = {}
    result['cat_id'] = Randomizer().lower_with_int()
    for row in source.split("\n"):
        lng = row.split("::")[0]

        if row.replace(" ", "") != "":
            if lng in ["he", "en", "ru", "ar"]:
                    result[lng] = row.split("::")[1]

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


