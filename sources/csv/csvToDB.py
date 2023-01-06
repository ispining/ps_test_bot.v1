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
                'recomended', # bool
                'catalog_view', # bool (visible, hidden)
                'description', # str
                'about', #  long str
                'start_sales',
                'end_sales',
                'mas_status', # taxable?
                'mas_type', # parent
                "in_stock", # bool
                "stock", # empty
                "minimal_stock", # empty
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
                'location', # str (str/list)
                's1_shemot',
                's1_arahim',
                's1_showed',
                's1_global',
                's1_default',
                's2_shemot',
                's2_arahim',
                's2_showed',
                's2_global',
                's2_default',
                's3_shemot',
                's3_arahim',
                's3_showed',
                's3_global',
                's3_default'
                ]
    
    def list_items(self):
        with open(self.filename) as csv_file:
            result = []
            csv_reader = []
            row_numval = 0
            for i in csv.reader(csv_file, delimiter=','):

                r = {}
                column_numval = 0
                for varname in self.vars:
                    try:
                        r[varname] = i[column_numval]
                    except:
                        break
                    column_numval += 1
                    
                if row_numval != 0:
                    result.append(r)
                
                row_numval += 1
            return result

    def test_useble(self):
        result = {}
        for varname in self.vars:
            result[varname] = 0
        for item in self.list_items():
            for varname in self.vars:
                try:
                    if item[varname] != '':
                        result[varname] += 1
                except:
                    break
        return result


class Test:
    class Item:
        def __str__(self):
            return "Items csv read test"

        def show_items_value(self, value):
            items_list = ImportFromCsv("../../items.csv").list_items()
            for item in items_list:
                print(item[value])
                print()


