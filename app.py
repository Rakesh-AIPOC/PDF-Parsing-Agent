from playwright.sync_api import sync_playwright
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

@tool
def query_reports(user_id: int):
    """
    Fetch reports for a given user_id.
    Returns both user_id and report_id along with description.
    """
    sql = "SELECT user_id, report_id, description FROM reports WHERE user_id = %s"
    rows = run_query(sql, (user_id,))
    if not rows:
        return f"No reports found for user_id {user_id}"
    result = "\n".join([f"user_id: {r[0]}, report_id: {r[1]}, description: {r[2]}" for r in rows])
    return result


def playwright():
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://rakeshk326.netlify.app/")
        page.wait_for_selector("a[href='#education']")
        page.click("a[href='#education']")
        input("Press Enter to close the browser...")
        browser.close()

if __name__ == "__main__":
    print(query_reports({"user_id": 101}))