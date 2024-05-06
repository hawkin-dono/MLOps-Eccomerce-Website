from typing import Any
import pandas as pd
from django.core.management.base import BaseCommand
from store.models import Product
from sqlalchemy import create_engine    

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        csv_file = 'data_products/crawled_data_the_thao_da_ngoai.csv'
        
        # lam_dep_suc_khoe 8
        # bach_hoa_online 9
        # the_thao_da_ngoai 10
        df = pd.read_csv(csv_file)

        #xóa đi data không có description
        length = df['short_description'].apply(len)
        df = df.drop(df[length < 10].index)
        
        #sửa lại price và sale_price về float
        df['price'] = df['price'].astype(float).round(2)
        

        df = df.drop(columns=['sku'])
        df = df.drop(columns=['product_link'])
        df = df.drop(columns=['list_price'])
        df = df.drop(columns=['price_usd'])
        df = df.drop(columns=['discount'])
        df = df.drop(columns=['discount_rate'])
        df = df.drop(columns=['review_count'])
        df = df.drop(columns=['order_count'])
        df = df.drop(columns=['inventory_status'])
        df = df.drop(columns=['is_visible'])
        df = df.drop(columns=['stock_item_qty'])
        df = df.drop(columns=['stock_item_max_sale_qty'])
        df = df.drop(columns=['product_name'])
        

        df['category_id'] = 10

        #Đổi tên 
        df.rename(columns={'id': 'tiki_product_id'}, inplace=True)
        df.rename(columns={'short_description':'description'}, inplace=True)
        
        df.reset_index(drop=True, inplace=True)
        
        df = df.drop_duplicates()
        df.reset_index(drop=True, inplace=True)
        print(df)

        engine = create_engine('sqlite:///db.sqlite3')
        df.to_sql(Product._meta.db_table, if_exists='append', con=engine, index=False)
        