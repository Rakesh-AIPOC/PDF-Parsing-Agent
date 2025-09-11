import mysql.connector
from langchain_core.tools import tool

def get_connection():
    """Connect to the MySQL DB using Spring Boot credentials."""
    return mysql.connector.connect(
        host="localhost",
        user="rakesh",
        password="Rakeshk@326",
        database="report_system"
    )

def run_query(query: str, params: tuple = None):
    """Execute a SQL query and return results."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    conn.close()
    return rows


def query_for_part_requirement(user_id: int):
    # """
    # Fetch reports for a given user_id.
    # Returns both user_id and report_id along with description.
    # """
    # sql = "SELECT barcode, user_id FROM pdf_inout_data WHERE task_id = %s"
    # rows = run_query(sql, (user_id,))
    # sql_data = {"barcode": str(rows[0][0]), "user": rows[0][1]}
    sql_data = {"barcode": '12345', "user": 'user01'}
    print("Part Requirement SQL Data fetched" + str(sql_data))
    return sql_data

def query_for_measurements(user_id: int):
    # """
    # Fetch reports for a given user_id.
    # Returns both user_id and report_id along with description.
    # """
    # sql = "SELECT barcode, user_id FROM pdf_inout_data WHERE task_id = %s"
    # rows = run_query(sql, (user_id,))
    # sql_data = {"barcode": str(rows[0][0]), "user": rows[0][1]}
    sql_data = {"barcode": '12345', "user": 'user01'}
    print("Measurements SQL Data fetched" + str(sql_data))
    return sql_data


if __name__ == "__main__":
    print(query_for_part_requirement(101))
    print(query_for_measurements(101))