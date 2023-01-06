import psycopg2
import csv
from pprint import pprint



class Import:
    def __init__(self, filename):
        self.filename = filename
        self.vars =  ['ident id',
                'item_type',
                'barcode',
                "name",
                "posted",
                'recomended',
                'catalog_view',
                'description',
                'about',
                'start_sales',
                'end_sales',
                'mas_status',
                'mas_type',
                "in_stock",
                "stock",
                "minimal_stock",
                "buy_without_stock",
                'one_by_one',
                'kilograms',
                'x',
                'y',
                'z',
                'can_review',
                'category_cost',
                'tags',
                'deluvery_type',
                'downliad limit',
                'days_left_to_download',
                'parent',
                'mekuvazim',
                'upgraded',
                'mashlimim',
                'source',
                'btn_text',
                'location',
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


items_list = Import("items.csv").test_useble()
pprint(items_list)

