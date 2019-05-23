from bs4 import BeautifulSoup
import os
import csv

os.chdir('C:/Users/s0046794/Documents/pycharm/brickset-scraper')

#Get list of all valid ICD Codes
import xml.etree.ElementTree as ET

#File source: https://www.cdc.gov/nchs/icd/icd10cm.htm#FY%202019%20release%20of%20ICD-10-CM
root = ET.parse('icd10cm_index_2019.xml').getroot()
code_list = []
for code in root.iter('code'):
    code_list.append(code.text.replace('-', ''))

num_code = len(code_list)

def get_syn_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    syn_list = []

    # Determine whether the code is still valid
    if soup.find('span', {'class': 'text-danger'}) is not None:
        syn_list = 'Invalid ICD Code'
    elif soup.find('span', {'class': 'text-info gi-1-25x'}, text='Synonyms') is None:
        syn_list = 'No Synonyms'
    else:
        #Find syn list
        span_class = soup.find('span', {'class': 'text-info gi-1-25x'}, text='Synonyms')
        for li in span_class.find_next('ul').find_all('li'):
            syn_list.append(li.text)

    return syn_list

#Determine whether the code is still valid
#if soup.find('span', {'class': 'text-success'}) is not None:
    #val.append('Valid ICD Code')

with open('mapping.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['ICD Code', 'Description', 'Synonyms'])

mapping_dict = {}
for i in range(num_code):
    url = 'https://icdlist.com/icd-10/' + code_list[i]
    syn_list = get_syn_list(url)
    desc = soup.find_all('strong')[1].text
    mapping_dict[str(code_list[i])] = [desc, syn_list]

    with open('mapping.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([code_list[i], desc, syn_list])
