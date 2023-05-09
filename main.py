
from ast import For
from optparse import Values
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

    
    
    # seznam_empty = page.locator('tr:has-text("Seznam je prázdný")')
    # print(seznam_empty.inner_text())
    load_more_button = page.get_by_role("link", name="Načíst další záznamy")
    #print(load_more_button)

    last_row = page.locator('tbody tr:nth-last-child(1) td:nth-child(1)') #obsah prvniho sloupce posledni bunky
    print(last_row.text_content())
    
    while load_more_button.is_visible():
        last_row = page.locator('tbody tr:nth-last-child(1) td:nth-child(1)')
        print(last_row.inner_text())
        if(last_row.inner_text()=="Seznam je prázdný."):
            print("Seznam je prazdny")
            break        
        else:
            load_more_button.click()
        # try:
        #     seznam_empty = page.locator('tr:has-text("Seznam je prázdný")')
        #     print(seznam_empty.inner_text())
        #     print("end")
        # except:
        #     print("nejsem na konci")


        #page.wait_for_timeout(10)
    #page.get_by_role("link", name="Načíst další záznamy").click()

    # page.get_by_role("link", name="Rádiotechnický prieskum").click()
    # #name
    # name_locator = page.locator('tr:has-text("Název v původním jazyce") td:nth-child(2)')
    # name=name_locator.inner_text()
    # print(name)
    # #place
    # place_locator = page.locator('tr:has-text("Místo vydání") td:nth-child(2)')
    # place=place_locator.inner_text()
    # print(place)
    # #published date
    # published_date_locator = page.locator('tr:has-text("Rok uplatnění") td:nth-child(2)')
    # published_date=published_date_locator.inner_text()
    # print(published_date)
    # #publication type
    # publication_type_locator = page.locator('tr:has-text("Druh výsledku") td:nth-child(2)')
    # publication_type=publication_type_locator.inner_text()
    # print(publication_type)
    # #hyperodkaz
    # second_table = page.locator('table').nth(1)
    # eleventh_tr_second_col = second_table.locator('tr:nth-child(11) td:nth-child(2)')
    # reference= eleventh_tr_second_col.inner_text()
    # print(reference)
    # #isbn
    # third_table = page.locator('table').nth(2)
    # second_tr_sec_col = third_table.locator('tr:nth-child(2) td:nth-child(2)')
    # isbn=second_tr_sec_col.inner_text()
    # print(isbn)
    # #amount of authors check
    # author_table = page.locator('tbody').nth(0)
    # tr_count = author_table.locator('tr').count()
    # #table of authors
    # list_of_authors=[]
    # for i in range(1,tr_count):
    #     string='tr:nth-child('+str(i)+') td:nth-child(2)'
    #     author = author_table.locator(string).inner_text()
    #     list_of_authors.append(author)
    # print(list_of_authors)


    # ---------------------
    page.wait_for_timeout(1000)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
