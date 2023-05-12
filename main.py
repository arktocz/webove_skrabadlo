
from ast import For
from optparse import Values
from playwright.sync_api import Playwright, sync_playwright, expect
import re
import json


#SCRAPE JEDNE PUBLIKACE
def scrape_publication(publication_page):
    #name
    name_locator = publication_page.locator('tr:has-text("Název v původním jazyce") td:nth-child(2)')
    name=name_locator.inner_text()
    #print(name)
    #place
    place_locator = publication_page.locator('tr:has-text("Místo vydání") td:nth-child(2)')
    place=place_locator.inner_text()
    #print(place)
    #published date
    published_date_locator = publication_page.locator('tr:has-text("Rok uplatnění") td:nth-child(2)')
    published_date=published_date_locator.inner_text()
    #print(published_date)
    #publication type
    publication_type_locator = publication_page.locator('tr:has-text("Druh výsledku") td:nth-child(2)')
    publication_type=publication_type_locator.inner_text()
    #print(publication_type)
    #hyperodkaz
    second_table = publication_page.locator('table').nth(1)
    eleventh_tr_second_col = second_table.locator('tr:nth-child(11) td:nth-child(2)')
    reference= eleventh_tr_second_col.inner_text()
    #print(reference)
    #isbn
    third_table = publication_page.locator('table').nth(2)
    second_tr_sec_col = third_table.locator('tr:nth-child(2) td:nth-child(2)')
    isbn=second_tr_sec_col.inner_text()
    #print(isbn)
    #amount of authors check
    author_table = publication_page.locator('tbody').nth(0)
    tr_count = author_table.locator('tr').count()
    #table of authors
    list_of_authors=[]
    for i in range(1,tr_count+1):
        string='tr:nth-child('+str(i)+') td:nth-child(2)'
        author = author_table.locator(string).inner_text()
        list_of_authors.append(author)
    publication_list=[name, place, published_date, publication_type, reference, isbn, list_of_authors]
    #print(publication_list)
    return publication_list

#LISTOVÁNÍ PUBLIKACEMI 
def individual_publication_view(page, browser, max_publication): 
    all_publication_table = page.locator('tbody').nth(0)
    publication_context = browser.new_context()
    publication_dict = {}
    for x in range(1, max_publication):
        locator='tr:nth-child('+str(x)+') td:nth-child(3) li:nth-child(1)'
        #print(locator)
        single_publication_link_locator = all_publication_table.locator(locator)  
        publication_url= single_publication_link_locator.inner_html().split('"')
        complete_url="https://apl.unob.cz"+publication_url[1]
        print(complete_url)
        #OTEVŘENÍ PUBLIKACE 
        #context2 = browser.new_context()
        publication_page = publication_context.new_page()
        publication_page.goto(complete_url)
        #scrape publikace
        publication_list=scrape_publication(publication_page)
        key = f"publication{x}"
        publication_dict[key]=publication_list
        #print(publication_list)
        publication_page.wait_for_timeout(500)
        publication_page.close()
    publication_context.close
    #print(publication_dict)
    return publication_dict

##NAČTENÍ KOMPLETNÍHO LISTU PUBLIKACÍ KE SCRAPU-done
def load_all_publications(page):
    load_more_button = page.get_by_role("link", name="Načíst další záznamy")
    while load_more_button.is_visible():
        last_row = page.locator('tbody tr:nth-last-child(1) td:nth-child(1)')
        if(last_row.inner_text()=="Seznam je prázdný."):
            print("Seznam je prazdnEJ")
            #page.wait_for_timeout(100000)
            break        
        else:
            load_more_button.click()

##POCET ZAZNAMU
def publication_count(page):
    publication_count_locator = page.locator('div:has-text("Počet záznamů: ") strong')
    return publication_count_locator.inner_text()








def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://apl.unob.cz/vvi/registr?NazevVysledku=")
    page.get_by_role("button", name="-Druh výsledku-").click()
    page.get_by_role("button", name="Odborná kniha (B)").click()
    page.get_by_role("button", name="Odborná kniha (B)", exact=True).click()
    page.get_by_role("button", name="").click()


    ##POCET ZAZNAMU
    x=publication_count(page)
    print(x)

    #NACTENI VSECH PUBLIKACI
    load_all_publications(page)

    #listovani publikacemi+scrape
    publication_dict=individual_publication_view(page, browser, 10)
    print(publication_dict)

    #uloženi do jsonu
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(publication_dict, f, ensure_ascii=False)
    



    # ---------------------
    page.wait_for_timeout(1000)
    #page2.close()
    #page.wait_for_timeout(10000)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
