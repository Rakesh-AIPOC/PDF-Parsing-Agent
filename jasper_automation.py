from playwright.sync_api import sync_playwright
import requests
import time

def run_jaspersoft():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("file:///D:/Rakesh/Study materials/PDF Parsing Agent/UI/jaspersoft_login.html")
        page.type('#username', 'admin', delay=150)
        page.type('#password', 'admin123', delay=150)
        page.locator('.login-btn').click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        page.hover('.nav-item:nth-child(2)')
        page.wait_for_timeout(2000)
        page.click('#respository-link')
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        page.click('#root-folder > span')
        page.wait_for_timeout(1000)
        page.click('#organisations-folder > span')
        page.wait_for_timeout(1000)
        page.click('#mx-folder > span')
        page.wait_for_timeout(1000)
        page.click('#reports-folder > span')
        page.wait_for_timeout(1000)
        page.click('#custom-folder > span')
        page.wait_for_timeout(1000)

        page.locator("table tbody tr td a").filter(has_text="Item1").click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        page.type('#barcode', '12345', delay=150)
        page.type('#userid', 'user01', delay=150)
        page.click('#apply-btn')
        page.click('#download-btn')
        browser.close()

if __name__ == "__main__":
    run_jaspersoft()