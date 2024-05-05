from typing import Any
import pandas as pd
from django.core.management.base import BaseCommand
from store.models import Product
from sqlalchemy import create_engine    

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        csv_file = 'crawled_data_nha_cua_doi_song.csv'
        df = pd.read_csv(csv_file)

        #xóa đi data không có description
        length = df['short_description'].apply(len)
        df = df.drop(df[length < 10].index)
        
        #sửa lại price và sale_price về float
        df['price'] = df['price'].astype(float).round(2)
        df['sale_price'] = df['sale_price'].astype(float).round(2)

        #Đổi tên 
        df.rename(columns={'id': 'tiki_product_id'}, inplace=True)
        df.rename(columns={'short_description':'description'}, inplace=True)
        df.rename(columns={'category-id': 'category_id'}, inplace=True)
        df.reset_index(drop=True, inplace=True)
        

        engine = create_engine('sqlite:///db.sqlite3')
        df.to_sql(Product._meta.db_table, if_exists='append', con=engine, index=False)
        