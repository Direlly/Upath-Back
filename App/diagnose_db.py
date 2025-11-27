from core.config import settings
import pymysql
import subprocess
import platform

def diagnose_database():
    print("🔍 DIAGNÓSTICO COMPLETO DO BANCO DE DADOS")
    print("=" * 50)
    
    # 1. Verificar se MySQL está rodando
    print("\n1. 🐬 Verificando se MySQL está rodando...")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['sc', 'query', 'mysql'], capture_output=True, text=True)
            if result.stdout and "RUNNING" in result.stdout:
                print("   ✅ MySQL está rodando no Windows")
            else:
                print("   ❌ MySQL NÃO está rodando no Windows")
        else:
            result = subprocess.run(['systemctl', 'is-active', 'mysql'], capture_output=True, text=True)
            if result.stdout and result.stdout.strip() == "active":
                print("   ✅ MySQL está rodando no Linux/Mac")
            else:
                print("   ❌ MySQL NÃO está rodando no Linux/Mac")
    except Exception as e:
        print(f"   ⚠️ Não foi possível verificar status do MySQL: {e}")
    
    # 2. Testar conexão direta com pymysql
    print("\n2. 🔌 Testando conexão direta com PyMySQL...")
    try:
        # Extrair dados da URL de forma segura
        url_parts = settings.DATABASE_URL.replace("mysql+pymysql://", "").split("@")
        if len(url_parts) < 2:
            print("   ❌ Formato inválido da DATABASE_URL")
            return
            
        user_pass = url_parts[0].split(":")
        host_port_db = url_parts[1].split("/")
        if len(user_pass) < 2 or len(host_port_db) < 2:
            print("   ❌ Formato inválido da DATABASE_URL")
            return
            
        host_port = host_port_db[0].split(":")
        
        username = user_pass[0] if user_pass else "root"
        password = user_pass[1] if len(user_pass) > 1 else ""
        host = host_port[0] if host_port else "localhost"
        port = int(host_port[1]) if len(host_port) > 1 else 3306
        database = host_port_db[1] if len(host_port_db) > 1 else "upath_db"
        
        print(f"   Conectando em: {host}:{port}, banco: {database}, usuário: {username}")
        
        connection = pymysql.connect(
            host=host,
            user=username,
            password=password,
            database=database,
            port=port,
            connect_timeout=5
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE(), USER()")
            result = cursor.fetchone()
            if result:
                print(f"   ✅ Conexão direta OK! Banco: {result[0]}, Usuário: {result[1]}")
            else:
                print("   ⚠️ Conexão OK mas não retornou dados")
        
        connection.close()
        
    except Exception as e:
        print(f"   ❌ Falha na conexão direta: {e}")
    
    # 3. Testar sem o banco (apenas conexão)
    print("\n3. 🧪 Testando conexão sem banco específico...")
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Abi369nt45',
            port=3306,
            connect_timeout=5
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            result = cursor.fetchall()
            databases = [row[0] for row in result] if result else []
            print(f"   ✅ Conectado ao MySQL! Bancos disponíveis: {databases}")
            
            if 'upath_db' in databases:
                print("   ✅ Banco 'upath_db' existe!")
            else:
                print("   ❌ Banco 'upath_db' NÃO existe!")
        
        connection.close()
        
    except Exception as e:
        print(f"   ❌ Falha na conexão básica: {e}")

if __name__ == "__main__":
    diagnose_database()