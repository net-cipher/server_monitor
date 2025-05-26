import mysql.connector
def log_stats(data):

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='monitoring_db'
        )
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO system_stats (cpu, ram, network, disk)
            VALUES (%s, %s, %s, %s)
        """, (data['cpu'], data['ram'], data['network'], data['disk']))

        conn.commit() 
        conn.close()

    except Exception as e:
        print("DB Error:", e) 
    
