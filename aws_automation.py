from playwright.sync_api import sync_playwright

def run_aws():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("file:///D:/Rakesh/Study materials/PDF Parsing Agent/UI/aws_access_portal.html")
        page.type('#account-search', 'Finance Team', delay=150)
        account = page.locator(".account-item", has_text="Finance Team")
        account.locator(".dropdown-btn").click()
        page.wait_for_timeout(2000)

        with page.expect_navigation():
            account.locator(".dropdown-list li a").first.click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        page.locator('#recently-visited-ec2').click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        page.locator('#EC2-instance').click()
        page.wait_for_load_state("domcontentloaded")

        page.type('#instance-search', 'Server', delay=150)
        all_checkboxes = page.locator(".instance-checkbox").all()

        visible_checkboxes = [cb for cb in all_checkboxes if cb.is_visible()]

        for i, cb in enumerate(visible_checkboxes):
            cb.click() 
            page.wait_for_timeout(300) 
            instance_id = page.locator("#details-id").inner_text()
            public_ip = page.locator("#details-public").inner_text()
            private_ip = page.locator("#details-private").inner_text()

            print(f"--- Instance {i+1} ---")
            print(f"Instance ID: {instance_id}")
            print(f"Public IP: {public_ip}")
            print(f"Private IP: {private_ip}")

            cb.click()
            page.wait_for_timeout(200)

        page.wait_for_timeout(3000)
        browser.close()

if __name__ == "__main__":
    run_aws()