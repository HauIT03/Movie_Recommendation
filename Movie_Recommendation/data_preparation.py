import pandas as pd
from sqlalchemy import create_engine

# Thông tin kết nối
server = 'ADMIN'  # Tên server của bạn
database = 'MovieRecommendation'  # Tên cơ sở dữ liệu của bạn

# Chuỗi kết nối SQLAlchemy với Windows Authentication
connection_string = f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'

engine = create_engine(connection_string)

ratings_df = pd.read_sql('SELECT * FROM Ratings', engine)
movies_df = pd.read_sql('SELECT * FROM Movies', engine)
tags_df = pd.read_sql('SELECT * FROM Tags', engine)
users_df = pd.read_sql('SELECT * FROM Users', engine)

print(movies_df.head())
print(ratings_df.head())
print(users_df.head())
print(tags_df.head())
