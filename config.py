#class Config:
 #    SECRET_KEY = "servezen_secret"
  #   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:3306/servezen"
#SQLALCHEMY_TRACK_MODIFICATIONS = False

#import os

#db_url = os.getenv("DATABASE_URL")

#if db_url and db_url.startswith("postgres://"):
 #   db_url = db_url.replace("postgres://", "postgresql://", 1)

#SQLALCHEMY_DATABASE_URI = db_url
#SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    db_url = os.getenv("DATABASE_URL")

    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     
