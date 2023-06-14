import uuid
#extrakce id ze stringu
def extract_after_third_space(string):
    words = string.split()
    
    if len(words) > 3:
        result = ' '.join(words[3:])
        return result
    else:
        return None
#generovani UUID
def generate_uuid():
    return str(uuid.uuid4())

#SCRAPE JEDNE PUBLIKACE
def scrape_publication(publication_page):
    #ID
    id_locator = publication_page.get_by_text("Detail výsledku")
    id=extract_after_third_space(id_locator.inner_text())
    #UUID
    uuid_publication=generate_uuid()
    #name
    name_locator = publication_page.locator('tr:has-text("Název v původním jazyce") td:nth-child(2)')
    name=name_locator.inner_text()
    #place
    place_locator = publication_page.locator('tr:has-text("Místo vydání") td:nth-child(2)')
    place=place_locator.inner_text()
    #published date
    published_date_locator = publication_page.locator('tr:has-text("Rok uplatnění") td:nth-child(2)')
    published_date=published_date_locator.inner_text()
    #publication type
    publication_type_locator = publication_page.locator('tr:has-text("Druh výsledku") td:nth-child(2)')
    publication_type=publication_type_locator.inner_text()
    #link
    second_table = publication_page.locator('table').nth(1)
    eleventh_tr_second_col = second_table.locator('tr:nth-child(11) td:nth-child(2)')
    reference= eleventh_tr_second_col.inner_text()
    #backup link
    third_table = publication_page.locator('table').nth(2)
    seven_tr_sec_col = third_table.locator('tr:nth-child(7) td:nth-child(2)')
    backup_link = seven_tr_sec_col.inner_text()
    #isbn
    third_table = publication_page.locator('table').nth(2)
    second_tr_sec_col = third_table.locator('tr:nth-child(2) td:nth-child(2)')
    isbn=second_tr_sec_col.inner_text()
    #amount of authors
    author_table = publication_page.locator('tbody').nth(0)
    tr_count = author_table.locator('tr').count()
    #table of authors
    list_of_authors=[]
    for i in range(1,tr_count+1):
        author_locator_string='tr:nth-child('+str(i)+') td:nth-child(2)'
        author = author_table.locator(author_locator_string).inner_text()
        list_of_authors.append(author)
    #publication_list=[id, uuid_publication, name, place, published_date, publication_type, reference, isbn, list_of_authors]
    publication_dict={"id":id, "uuid_publication":uuid_publication, "name":name, "place":place, "published_date":published_date, "publication_type":publication_type, "reference":reference, "backup_link":backup_link, "isbn":isbn, "list_of_authors":list_of_authors}
    return publication_dict

#LISTOVÁNÍ PUBLIKACEMI 
def individual_publication_view(page, browser, max_publication): 
    all_publication_table = page.locator('tbody').nth(0)
    publication_context = browser.new_context()
    publication_dict = {}
    for x in range(1, max_publication+1): #ZDE 1
        locator='tr:nth-child('+str(x)+') td:nth-child(3) li:nth-child(1)'
        single_publication_link_locator = all_publication_table.locator(locator)  
        publication_url= single_publication_link_locator.inner_html().split('"')
        complete_url="https://apl.unob.cz"+publication_url[1]
        #print(complete_url)
        #OTEVŘENÍ PUBLIKACE 
        publication_page = publication_context.new_page()
        publication_page.goto(complete_url)
        #SCRAPE PUBLIKACE
        publication_list=scrape_publication(publication_page)
        key = f"publication{x}"
        publication_dict[key]=publication_list
        #publication_page.wait_for_timeout(500)
        publication_page.close()
    publication_context.close()
    #print(publication_dict)
    return publication_dict

##NAČTENÍ KOMPLETNÍHO LISTU PUBLIKACÍ KE SCRAPU
def load_all_publications(page):
    load_more_button = page.get_by_role("link", name="Načíst další záznamy")
    while load_more_button.is_visible():
        last_row = page.locator('tbody tr:nth-last-child(1) td:nth-child(1)')
        if(last_row.inner_text()=="Seznam je prázdný."):
            print("KONEC SEZNAMU")
            break        
        else:
            load_more_button.click()

##POCET ZAZNAMU
def publication_count(page):
    publication_count_locator = page.locator('div:has-text("Počet záznamů: ") strong')
    return publication_count_locator.inner_text()