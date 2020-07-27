db = {
    'user' : 'myuser',
    'password' : '1q2w3e4r5t',
    'host' : 'mysql',
    'port' : 3306,
    'database' : 'gpp_db'
}

# flask-sqlalchemy db_url
DB_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"