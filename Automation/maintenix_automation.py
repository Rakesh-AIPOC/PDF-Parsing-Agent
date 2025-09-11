from playwright.sync_api import sync_playwright
import re

def run_mx():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("file:///D:/Rakesh/Study materials/PDF Parsing Agent/UI/maintenix_portal.html")
        headers = page.locator("table thead th").all_inner_texts()
        name_col_index = headers.index("Name")
        row = page.locator("table tbody tr").first
        link = row.locator("td").nth(name_col_index).locator("a")
        page.wait_for_timeout(2000)
        link.click()
        page.wait_for_load_state("load")

        headers1 = page.locator("table thead th").all_inner_texts()
        name_col_index1 = headers1.index("Id")
        row1 = page.locator("table tbody tr").first
        link1 = row1.locator("td").nth(name_col_index1).locator("a")
        page.wait_for_timeout(2000)
        link1.click()
        page.wait_for_load_state("load")
        page.wait_for_timeout(2000)

        page.locator("div.info-header2", has_text="Measurement").click()
        measurement_table = page.locator("div.info-header2", has_text="Measurement").locator("xpath=following-sibling::div[1]//table")
        measurement_table.wait_for(state="visible", timeout=5000)
        rows = measurement_table.locator("tbody tr")

        if rows.count() > 0 :
            page.wait_for_timeout(2000)
            details_header = page.locator("div.info-header", has_text="Details")
            details_content = details_header.locator("xpath=following-sibling::div[1]")
            text = details_content.inner_text()
            match = re.search(r'Barcode:\s*(\S+)', text)
            if match :
                barcode = match.group(1)
                print(barcode)
                browser.close()
                return barcode
        else :
            browser.close()
            print("False")
            return "False"


if __name__ == "__main__":
    run_mx()