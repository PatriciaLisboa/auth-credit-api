from app.database import engine, Base
from app.models import User, Debt

def create_tables():
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    create_tables() 