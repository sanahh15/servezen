class Config:
    SECRET_KEY = "servezen_secret"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:3306/servezen"
    SQLALCHEMY_TRACK_MODIFICATIONS = False