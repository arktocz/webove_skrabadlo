
from playwright.sync_api import Playwright, sync_playwright, expect



def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://apl.unob.cz/vvi/registr?NazevVysledku=")
    page.get_by_role("button", name="-Druh výsledku-").click()
    page.get_by_role("button", name="Odborná kniha (B)").click()
    page.get_by_role("button", name="Odborná kniha (B)", exact=True).click()
    page.get_by_role("button", name="").click()
    page.get_by_role("link", name="Leadership a stress").click()
    #page.get_by_role("heading", name="Taktika 2018").click()

   
    row = page.locator('tr:has-text("Název v původním jazyce")')
    print(row.inner_text())
    row = page.locator('tr:has-text("Místo vydání")')
    print(row.inner_text())
    row = page.locator('tr:has-text("Rok uplatnění")')
    print(row.inner_text())
    row = page.locator('tr:has-text("Druh výsledku")')
    print(row.inner_text())
    #autor
    first_table = page.locator('tbody').nth(0)
    third_tr = first_table.locator('tr:nth-child(1)')
    print(third_tr.inner_text())
    #hyperodkaz
    first_table = page.locator('table').nth(1)
    third_tr = first_table.locator('tr:nth-child(11)')
    print(third_tr.inner_text())
    #isbn
    first_table = page.locator('table').nth(2)
    third_tr = first_table.locator('tr:nth-child(2)')
    print(third_tr.inner_text())

    # ---------------------
    page.wait_for_timeout(1000)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
