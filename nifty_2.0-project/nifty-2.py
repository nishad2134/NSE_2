from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import pandas as pd
from IPython.display import display
import ipywidgets as widgets

def get_stock_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_selector('table')  
        page.wait_for_load_state('networkidle') 

        html_body = page.inner_html('body')
        browser.close()

        return HTMLParser(html_body)

def parse_and_save_to_csv(html, filename):
    tbody = html.css('tbody')
    all_data = []

    for tbody_element in tbody:
        for row in tbody_element.css('tr'):
            nse_dic = {}
            columns = row.css('td')
            if len(columns) >= 6:  
                nse_dic['Parameter'] = columns[0].text()
                nse_dic['Value'] = columns[1].text()
                all_data.append(nse_dic)

    data = pd.DataFrame(all_data)
    data.to_csv(filename, index=False)
    
    display(data)


url = 'https://www.nseindia.com/get-quotes/equity?symbol=KOTAKBANK'
html = get_stock_data(url)
parse_and_save_to_csv(html, 'KOTAKBANK_data.csv')
