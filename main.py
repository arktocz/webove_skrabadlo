
from ast import For
from optparse import Values
from playwright.sync_api import Playwright, sync_playwright, expect
import json
from my_functions import publication_count, load_all_publications, individual_publication_view

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.set_default_timeout(2**31-1)
    page = context.new_page()
    page.goto("https://apl.unob.cz/vvi/registr?NazevVysledku=")
    page.get_by_role("button", name="-Druh výsledku-").click()
    page.get_by_role("button", name="Odborná kniha (B)").click()
    page.get_by_role("button", name="Odborná kniha (B)", exact=True).click()
    page.get_by_role("button", name="").click()
    ##TEST PRO 9 ZAPISU
    # page.get_by_role("button", name="-Rok uplatnění-").click()
    # page.get_by_role("button", name="2020").click()
    # page.get_by_role("button", name="2020", exact=True).click()
    # page.get_by_role("button", name="-Druh výsledku-").click()
    # page.get_by_role("button", name="Odborná kniha (B)").click()
    # page.get_by_role("button", name="Odborná kniha (B)", exact=True).click()
    # page.get_by_role("button", name="").click()

    ##POCET ZAZNAMU
    publication_amount=int(publication_count(page))
    print(publication_amount)
    #NACTENI VSECH PUBLIKACI
    load_all_publications(page)
    #listovani publikacemi+scrape
    publication_dict=individual_publication_view(page, browser, publication_amount)
    #uloženi do jsonu
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(publication_dict, f, ensure_ascii=False)
    print("Neplecha ukončena")
    
    # ---------------------
    page.wait_for_timeout(1000)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
