from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
mysql_host = os.getenv('MYSQL_HOST_STOCKVIP')
mysql_user = os.getenv('MYSQL_USER_STOCKVIP')
mysql_pass = os.getenv('MYSQL_PASS_STOCKVIP')
# engine_user= create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_pass}@{mysql_host}:3306/user?auth_plugin=mysql_native_password',pool_pre_ping=True)
engine_stockDB= create_engine(f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/stockdb",
    pool_size=10,             # Số kết nối giữ sẵn trong pool
    max_overflow=2,          # Số kết nối vượt quá pool_size khi cần
    pool_timeout=30,          # Thời gian chờ lấy kết nối trước khi raise TimeoutError
    pool_recycle=120,        # Tái tạo kết nối sau 30 phút (tránh idle disconnect)
    pool_pre_ping=True, )      # Kiểm tra kết nối trước khi dùng)
engine_user= create_engine(f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/userdb",
    pool_size=3,             # Số kết nối giữ sẵn trong pool
    max_overflow=2,          # Số kết nối vượt quá pool_size khi cần
    pool_timeout=30,          # Thời gian chờ lấy kết nối trước khi raise TimeoutError
    pool_recycle=120,        # Tái tạo kết nối sau 30 phút (tránh idle disconnect)
    pool_pre_ping=True,)
DATABASE_URL_EOD=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/stockdb" # Kết nối lắng nghe postgres không thêm psycopg2
engine_stock=''