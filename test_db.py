from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configuração direta do banco de dados
DATABASE_URL = "postgresql://patricia:patricia123@localhost/credit_db"

try:
    # Criar engine
    engine = create_engine(DATABASE_URL)
    
    # Testar conexão
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexão com o banco de dados bem sucedida!")
        print("Resultado:", result.fetchone())
        
except Exception as e:
    print("Erro ao conectar com o banco de dados:")
    print(str(e)) 