import os
import pymysql
import ssl

# TiDB Cloud Serverless Connection Details
host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
port = 4000
user = "vheZ87CwGZ77QoT.root"
password = "Jg7Ec8kbI7mVGADI"
database = "test"

print(f"--- Attempting Connection to TiDB Cloud ({host}:{port}) ---")

try:
    # Attempting connection using pymysql with basic SSL requirements
    # TiDB Serverless requires SSL by default
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        ssl_verify_identity=True, # Equivalent to ssl_mode=VERIFY_IDENTITY
        # If you don't have the CA file, we can try to use system certs or no verify for test
        # ssl={"ca": "<CA_PATH>"} 
    )
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION(), DATABASE();")
        version, db_name = cursor.fetchone()
        print(f"SUCCESS! Connected to {db_name} (Version: {version})")
        
    connection.close()

except Exception as e:
    print(f"CONNECTION FAILED: {e}")
    print("\nAttempting Fallback (No identity verification)...")
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            ssl_verify_cert=False # Only for internal testing to verify credentials
        )
        print("SUCCESS! Connected (Unverified SSL)")
        connection.close()
    except Exception as e2:
        print(f"FALLBACK FAILED TOO: {e2}")
