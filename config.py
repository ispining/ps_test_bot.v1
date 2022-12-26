import os
import random

from bot_connect import *

pickle = ilm.tools.pickle


kmarkup = tg.kmarkup
send = tg.send

import psycopg2


def sysDB() -> psycopg2:
    db = psycopg2.connect(host='illyashost.ddns.net', database="powersport", user="postgres", password="armageddon")
    return db, db.cursor()


def close_db(db) -> None:
    try:
        db.close()
    except:
        pass
db, sql = sysDB()

class Stages:
    def __init__(self, user_id):

        if "stages" not in os.listdir("sources"):
            pickle("sources/stages").pick([])
        self.user_id = user_id
        self.lst = pickle("sources/stages").unpick()

    def get(self):
        for user in self.lst:
            if user['user_id'] == self.user_id:
                return user['stage']
        return "None"

    def set(self, new):
        for user in self.lst:
            if user['user_id'] == self.user_id:
                self.lst.remove(user)
                user['stage'] = new
                self.lst.append(user)
                pickle("sources/stages").pick(self.lst)

                return user['stage']

        self.lst.append({"user_id": self.user_id, "stage": new})
        pickle("sources/stages").pick(self.lst)
        return new


def str_is_only_integers(str_to_check):
    try:
        int(str_to_check)
        return True
    except:
        return False