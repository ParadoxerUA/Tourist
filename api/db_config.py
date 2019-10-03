class Config:
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
