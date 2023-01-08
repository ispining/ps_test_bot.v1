import psycopg2
import csv
from pprint import pprint


class ImportFromCsv:
    def __init__(self, filename):
        self.filename = filename
        self.vars = ['ident_id', # str
                'item_type',
                'barcode', # str
                "name", # str
                "posted_by", # bool
                'catalog_view', # bool (visible, hidden)
                'description', # str
                'about', #  long str
                'mas_status', # taxable?
                'mas_type', # parent
                "in_stock", # num
                "minimal_stock", # num
                "buy_without_stock", # bool
                'one_by_one', # bool
                'kilograms', # float
                'x', # int
                'y', # int
                'z', # int
                'can_review', # bool
                'category_cost',
                'tags',
                'delivery_type', # str
                'download limit',
                'days_left_to_download', # str
                'parent', #str (category)
                'mekuvazim', # str
                'upgraded',# empty
                'mashlimim',# empty
                'source', # str (url)
                'btn_text', # empty
                'location' # str (str/list)
                ]






# item_type = simple/variable/variation
# barcode = 999999999 # str
# name = Names class ident_id # str
# posted_by, # bool
# recomended, # bool
# catalog_view, # bool (visible, hidden)
# description, # str
# about, #  long str
# mas_status, # taxable?
# mas_type, # parent
# in_stock, # bool
# stock, # empty
# minimal_stock, # empty
# buy_without_stock, # bool
# one_by_one, # bool
# kilograms, # float
# x, # int
# y, # int
# z, # int
# can_review, # bool
# category_cost,
# tags,
# delivery_type, # str
# download limit,
# days_left_to_download, # str
# parent, #str (category)
# mekuvazim, # str
# upgraded,# empty
# mashlimim,# empty
# source, # str (url)
# btn_text, # empty
# location, # str (str/list)