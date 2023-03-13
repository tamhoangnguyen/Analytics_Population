import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome('chromedriver.exe')

# Tạo ra url
url = 'https://danso.org/'
url_region = "https://danso.org/the-gioi/" # Danh sách các nước theo từng khu vực
url_table = '/html/body/div[2]/main/section/article/div[2]/div[4]/div/table/tbody'
url_country = '/html/body/div[2]/main/section/article/div[1]/div[2]/ul/li[1]/strong[1]'# Danh sách tất cả các nước
url_header = '/html/body/div[2]/main/section/article/div[2]/div[4]/div/table/thead/tr'

#Truy cập vào url
driver.get(url)

    #1 Lấy tên quốc gia từng quốc gia
elems_country = driver.find_elements(By.CSS_SELECTOR,".country-list")
countrys = [country.text.split('\n') for country in elems_country]

    #2 Lấy link từng quốc gia
elems_link = driver.find_elements(By.CSS_SELECTOR,".country-list [href]")
links = [link.get_attribute('href') for link in elems_link]
   
    #3 Tạo dataframe chưa #1 và #2 kết hợp tạo index
sumarize_table_1 = pd.DataFrame(countrys[0], columns=["Country"])
sumarize_table_1['STT'] = np.arange(1,len(countrys[0])+1)
sumarize_table_1['link'] = links
        # Tạo những mãng chứa data
    #1.Data của bảng tóm tắt 

populations,time_update,percents,ranks,densitys,areas,urban_population_density,average_ages = [],[],[],[],[],[],[],[] 
    #2.Data của mãng dữ liệu từ 1955-2020
countrys,year, population, percent_Change, change, Migrate,percent_city,population_city,percent_world,population_world,rank = [],[],[],[],[],[],[],[],[],[],[] 

def crawl_data_summarize_table(element):
    if len(element) != 13:
        year.append(element[0])
        population.append(element[1])
        percent_Change.append(element[2])
        change.append(element[3])
        Migrate.append(element[4])
        percent_city.append(element[5])
        population_city.append(element[6])
        percent_world.append(element[7])
        population_world.append(element[8])
        rank.append(element[9])
    else:
        year.append(element[0])
        population.append(element[1])
        percent_Change.append(element[2])
        change.append(element[3])
        Migrate.append(element[4])
        percent_city.append(element[8])
        population_city.append(element[9])
        percent_world.append(element[10])
        population_world.append(element[11])
        rank.append(element[12])

lost_data = [] # Tạo ra 1 danh sách các link ở ngoại lệ NoSuchElementException

def crawl_data_table(links):
    try:
        driver.get(links)
        country = driver.find_element('xpath',url_country)
        all_list = []
        element = driver.find_element('xpath',url_table)
        all_list.append(element.text.split('\n'))
        new_range = len(all_list[0]) 
        for n in range(new_range):
            new_list = all_list[0]
            new_list = str(new_list[n]).split()
            countrys.append(country.text)
            crawl_data_summarize_table(new_list)
        print('Crawl data full is success !')
    except NoSuchElementException:
        print('Crawl data full is fail !')
        lost_data.append(links)

def crawl_lost_data(links):
    for i in range(len(links)):
        try:
            driver.get(links[i])
            country = driver.find_element('xpath',url_country)
            all_list = []
            element = driver.find_element('xpath',url_table)
            all_list.append(element.text.split('\n'))
            new_range = len(all_list[0]) 
            for n in range(new_range):
                new_list = all_list[0]
                new_list = str(new_list[n]).split()
                countrys.append(country.text)
                crawl_data_summarize_table(new_list)
        except NoSuchElementException:
            lost_data.append(links[i])
            print('Crawl data lost full {} is fail !'.format(i+1))

for n in range(len(links)):
    driver.get(links[n])
    print("Crawl Data {} !".format(n))
    # Lấy dữ liệu của bảng tóm tắt 
    elems_population = driver.find_element('xpath','/html/body/div[2]/main/section/article/div[1]/div[2]/ul/li[1]/strong[2]')
    populations.append(elems_population.text)

    elems_percent = driver.find_element('xpath','/html/body/div[2]/main/section/article/div[1]/div[2]/ul/li[2]/strong')
    percents.append(elems_percent.text)

    elems_time = driver.find_element('xpath','/html/body/div[2]/main/section/article/div[1]/div[2]/div[1]/p[2]')
    time_update.append(elems_time.text)

    elems_rank = driver.find_element('xpath','/html/body/div[2]/main/section/article/div[1]/div[2]/ul/li[3]/strong')
    ranks.append(elems_rank.text)

    elems_densitys = driver.find_element('xpath','/html/body/div[2]/main/section/article/div[1]/div[2]/ul/li[4]/strong')
    densitys.append(elems_densitys.text)

    elems_area = driver.find_element('xpath','/html/body/div[2]/main/section/article/div[1]/div[2]/ul/li[5]/strong[2]')
    areas.append(elems_area.text)

    elems_urban_population_density = driver.find_element('xpath','/html/body/div[2]/main/section/article/div[1]/div[2]/ul/li[6]/strong')
    urban_population_density.append(elems_urban_population_density.text)

    elems_average_ages = driver.find_element('xpath','/html/body/div[2]/main/section/article/div[1]/div[2]/ul/li[7]/strong[2]')
    average_ages.append(elems_average_ages.text)
    
    # Lấy dữ liệu từ 1955-2020
    crawl_data_table(links[n])
    print("Crawl Data Country {} is success !".format(n))
    sleep(3)

#Lấy dữ liệu bị ngoại lệ
stt = 0
new_links = lost_data
lost_data = []
while len(new_links) > 0 :  
    crawl_lost_data(new_links) 
    new_links = lost_data
    lost_data = []
    stt +=1
    if stt == 10:
        break

#Lấy dữ liệu các nước theo khu vực
driver.get(url_region)
region = []
country = []
url_re_gion = '.cat-container .sub-cat .sub-cat-title [href]'
elements_region = driver.find_elements(By.CSS_SELECTOR,url_re_gion)
regions = [region.get_attribute('title') for region in elements_region]
for i in range(1,len(regions)+1):
    url_tiles = '/html/body/div[2]/main/section/div[2]/div[{}]/ul'.format(i)
    re_gion = regions[i-1]
    elements_tiles = driver.find_element('xpath',url_tiles)
    elements_country = elements_tiles.find_elements(By.CSS_SELECTOR,'.entry-title')
    coun_trys = [new_country.text for new_country in elements_country]
    for i in range(len(coun_trys)):
        country.append(coun_trys[i])
        region.append(re_gion)


#Lưu dữ liệu của bảng tóm tắt
sumarize_table_2 = pd.DataFrame(list(zip(populations,time_update,percents,ranks,densitys,areas,urban_population_density,average_ages)),
                   columns=['Population','Time_Update','Percent','Rank','Density','Area','Urban_population_density','Average_age'])
sumarize_table_2['index'] = np.arange(1,len(links) + 1)

sumarize_table = sumarize_table_1.merge(sumarize_table_2,left_on="STT",right_on="index")

sumarize_table.to_csv("Data_DanSo.csv")


#Lưu dữ liệu của bảng dữ liệu từ 1955-2020
Full_Table = pd.DataFrame(list(zip(countrys,year, population, percent_Change, change, Migrate,percent_city,population_city,percent_world,population_world,rank)),
                  columns=['Country','Year','Population','Population_change_rate','Population_change','Migrate','percent_city','population_city','percent_world','population_world','rank'])

Full_Table.to_csv('Data_table.csv')

#Lưu dữ liệu các nước theo khu vực
region_table = pd.DataFrame(list(zip(region,country)),columns=['Region','Country'])
region_table.to_csv('Data_Region.csv')



