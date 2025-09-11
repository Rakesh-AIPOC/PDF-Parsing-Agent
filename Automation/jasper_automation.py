from playwright.sync_api import sync_playwright

def run_jaspersoft(input_params_casa_faa: dict,
                   input_params_part_requirement: dict,
                   input_params_measurements: dict):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # --- Login ---
        page.goto("file:///D:/Rakesh/Study materials/PDF Parsing Agent/UI/jaspersoft_login.html")
        page.type('#username', 'admin', delay=150)
        page.type('#password', 'admin123', delay=150)
        page.locator('.login-btn').click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        # --- Navigate to Custom folder ---
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

        # --- Process reports in Custom ---
        reports = ["Item1", "Item2"]
        for report in reports:
            with page.context.expect_page() as new_page_info:
                page.locator("table tbody tr td a").filter(has_text=report).click(button="middle")  # open in new tab
            new_page = new_page_info.value

            new_page.bring_to_front()
            new_page.wait_for_load_state("domcontentloaded")
            new_page.wait_for_timeout(2000)

            new_page.type('#barcode', input_params_part_requirement.get("barcode"), delay=150)
            new_page.type('#userid', input_params_part_requirement.get("user"), delay=150)
            new_page.click('#apply-btn')
            new_page.click('#download-btn')
            new_page.wait_for_timeout(5000)

            new_page.close()
            page.wait_for_timeout(2000)

        # --- Process Temp folder ---
        page.click('#temp-folder > span')
        page.wait_for_timeout(1000)

        with page.context.expect_page() as new_page_info:
            page.locator("table tbody tr td a").filter(has_text="Temp1").click(button="middle")
        temp_page = new_page_info.value

        temp_page.bring_to_front()
        temp_page.wait_for_load_state("domcontentloaded")
        temp_page.wait_for_timeout(2000)

        temp_page.type('#barcode', input_params_part_requirement.get("barcode"), delay=150)
        temp_page.type('#userid', input_params_part_requirement.get("user"), delay=150)
        temp_page.click('#apply-btn')
        temp_page.click('#download-btn')
        temp_page.wait_for_timeout(5000)

        temp_page.close()
        browser.close()


if __name__ == "__main__":
    run_jaspersoft(
        {"barcode": "12345", "user": "user01"},
        {"barcode": "12345", "user": "user01"},
        {"barcode": "12345", "user": "user01"}
    )