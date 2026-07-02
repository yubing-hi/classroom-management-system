import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv
from pymysql import Error

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / '.env')

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'classroom_management'),
    'charset': 'utf8mb4',
    'autocommit': True,
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)


if __name__ == '__main__':
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
            print('数据库连接成功:', cursor.fetchone())
        conn.close()
    except Error as e:
        print('数据库连接失败:', e)
