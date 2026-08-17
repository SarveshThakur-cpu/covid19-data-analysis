import pyodbc


def get_connection():

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DARSHAN\\SQLEXPRESS;"
        "DATABASE=COVID19_DB;"
        "Trusted_Connection=yes;"
    )

    return conn


# Test connection
if __name__ == "__main__":

    try:
        conn = get_connection()

        print("Connection successful!")

        conn.close()

    except pyodbc.Error as e:

        print("Connection failed!")
        print(e)