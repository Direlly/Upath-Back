from core.config import settings
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    try:
        print("🔍 Testando conexão com banco...")
        print(f"URL: {settings.DATABASE_URL}")
        
        # Criar engine de teste
        engine = create_engine(
            settings.DATABASE_URL, 
            echo=True,
            pool_pre_ping=True
        )
        
        # Testar conexão
        with engine.begin() as conn:
            # Teste 1: Conexão básica
            print("\n1. 🧪 Testando conexão básica...")
            result = conn.execute(text("SELECT 1"))
            print("   ✅ SELECT 1: OK")
            
            # Teste 2: Informações do banco
            print("\n2. 📊 Obtendo informações do banco...")
            result = conn.execute(text("SELECT DATABASE(), USER(), VERSION()"))
            db_info = result.fetchone()
            if db_info:
                print(f"   ✅ Banco: {db_info[0]}")
                print(f"   ✅ Usuário: {db_info[1]}")
                print(f"   ✅ Versão: {db_info[2]}")
            else:
                print("   ⚠️ Não foi possível obter informações do banco")
            
            # Teste 3: Listar tabelas
            print("\n3. 📋 Listando tabelas...")
            try:
                result = conn.execute(text("SHOW TABLES"))
                tables = result.fetchall()
                if tables:
                    table_list = [row[0] for row in tables]
                    print(f"   ✅ Tabelas encontradas: {len(tables)}")
                    for table in table_list:
                        print(f"      - {table}")
                else:
                    print("   ℹ️ Nenhuma tabela encontrada no banco")
            except Exception as e:
                print(f"   ⚠️ Erro ao listar tabelas: {e}")
            
            # Teste 4: Verificar caracteres e collation
            print("\n4. ⚙️ Verificando configurações...")
            try:
                result = conn.execute(text("SHOW VARIABLES LIKE 'character_set_database'"))
                charset = result.fetchone()
                if charset:
                    print(f"   ✅ Charset: {charset[1]}")
                
                result = conn.execute(text("SHOW VARIABLES LIKE 'collation_database'"))
                collation = result.fetchone()
                if collation:
                    print(f"   ✅ Collation: {collation[1]}")
            except Exception as e:
                print(f"   ⚠️ Erro ao verificar configurações: {e}")
        
        print("\n🎉 Todos os testes passaram! Conexão está funcionando perfeitamente.")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO na conexão: {e}")
        print("\n💡 Possíveis soluções:")
        print("   1. Verifique se o MySQL está rodando")
        print("   2. Verifique se a senha está correta")
        print("   3. Verifique se o banco 'upath_db' existe")
        print("   4. Verifique se o usuário tem privilégios")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    exit(0 if success else 1)