from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import undetected_chromedriver as uc
import datetime
import time
import os
from db_funcs import *
from config import *
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Scrapes the brand "DS" and inserts data to db
# [Raporlar].[dbo].[DS_cars_data]
def DS_scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[DS_cars_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'DS'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)
    time.sleep(5)
    i = 0
    amount_of_cars_inserted = 0
    while True:
        i += 1
        try:
            driver.get("https://talep.dsautomobiles.com.tr/fiyat-listesi")
            select_element = driver.find_element("xpath", '//*[@id="bilgitalebi"]/div[2]/div[1]/div/div[2]/div/select')
            select = Select(select_element)
            select.select_by_index(i)
            time.sleep(2)

            list_elements = driver.find_elements("tag name", 'li')
            for list_element in list_elements:
                values = list_element.find_elements("tag name", 'em')
                car_dict = {}
                for value in values:
                    if value.text != "":
                        if value.get_attribute('title') == "TAVSİYE EDİLEN ANAHTAR TESLİM FİYATI {} İMAL YILI".format(sene):
                            car_dict['BuSene_Uretim_Fiyat'] = value.text
                        elif value.get_attribute('title') == "TAVSİYE EDİLEN ANAHTAR TESLİM FİYATI {} İMAL YILI".format(sene-1):
                            car_dict['GecenSene_Uretim_Fiyat'] = value.text
                        elif value.get_attribute('title') == "TAVSİYE EDİLEN ANAHTAR TESLİM FİYATI":
                            car_dict['TavsiyeEdilen_AnahtarTeslim_Fiyat'] = value.text
                        else:
                            car_dict['AracModel'] = value.text

                if len(car_dict) != 0:
                    if 'GecenSene_Uretim_Fiyat' in car_dict:
                        if car_dict['GecenSene_Uretim_Fiyat'] != "-":
                            gecensene_uretim_fiyat = car_dict['GecenSene_Uretim_Fiyat'].replace(".","").replace("₺","")
                        else:
                            gecensene_uretim_fiyat = "NULL"
                    else:
                        gecensene_uretim_fiyat = "NULL"
                    if 'BuSene_Uretim_Fiyat' in car_dict:
                        if car_dict['BuSene_Uretim_Fiyat'] != "-":
                            busene_uretim_fiyat = car_dict['BuSene_Uretim_Fiyat'].replace(".","").replace("₺","")
                        else:
                            busene_uretim_fiyat = "NULL"
                    else:
                        busene_uretim_fiyat = "NULL"
                    if 'TavsiyeEdilen_AnahtarTeslim_Fiyat' in car_dict:
                        if car_dict['TavsiyeEdilen_AnahtarTeslim_Fiyat'] != "-":
                            Tavsiye_edilen_anahtarteslim_fiyat = car_dict['TavsiyeEdilen_AnahtarTeslim_Fiyat'].replace(".","").replace("₺","")
                        else:
                            Tavsiye_edilen_anahtarteslim_fiyat = "NULL"
                    else:
                        Tavsiye_edilen_anahtarteslim_fiyat = "NULL"
                    if 'AracModel' in car_dict:
                        Arac_model = car_dict['AracModel']
                    else:
                        Arac_model = "NULL"
                    car_detail = Arac_model
                    query = "Insert INTO [Raporlar].[dbo].[DS_cars_data] (marka, model, thisyear_prod_price, lastyear_prod_price, recommended_sale_price, tarih, car_detail) VALUES ('{}', '{}', {}, {}, {}, '{}', '{}')".format("DS", Arac_model, busene_uretim_fiyat, gecensene_uretim_fiyat, Tavsiye_edilen_anahtarteslim_fiyat, today, car_detail)
                    QueryToDB(YuceDB, query)
                    if busene_uretim_fiyat == 'NULL':
                        fiyat = Tavsiye_edilen_anahtarteslim_fiyat
                    elif Tavsiye_edilen_anahtarteslim_fiyat == 'NULL':
                        fiyat = busene_uretim_fiyat
                    fiyat = fiyat.replace(".","").replace("TL","").replace(" ","").replace(",","")
                    kampanyali_fiyat = "-"
                    query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                        "DS", fiyat, kampanyali_fiyat, car_detail, today)
                    QueryToDB(YuceDB, query_dashboard)
                    amount_of_cars_inserted += 1

            driver.get("https://talep.dsautomobiles.com.tr/fiyat-listesi")
        except:
            break
    driver.quit()
    print("DS_scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))
    return amount_of_cars_inserted

# Scrapes the brand "Peugeot" and inserts data to db
# [Raporlar].[dbo].[Peugeot_auto_data]
def Peugeot_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Peugeot_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Peugeot'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    amount_of_cars_inserted = 0

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)
    driver.get("https://kampanya.peugeot.com.tr/fiyat-listesi/")
    time.sleep(1)
    try:
        # Clicks to "Accept all" for cookies
        driver.find_element("xpath", '//*[@id="ihm-accept-all-btn"]').click()
        time.sleep(0.2)

        car_models = driver.find_elements("class name", 'carModel')
        for car_model in car_models:
            car_model.click()
            time.sleep(0.3)
            #print(car_model.find_element("tag name", 'h3').text)

            fiyat_tablo = driver.find_element("class name", 'dataTableNew')
            tr_tags = fiyat_tablo.find_elements("tag name", 'tr')
            Yakit_Tipi = "Unknown"
            for tr_tag in tr_tags:
                if tr_tag.text != "":
                    td_tags = tr_tag.find_elements("tag name", 'td')
                    i = 0
                    for td_tag in td_tags:
                        i += 1
                        if "Benzin" in td_tag.text:
                            Yakit_Tipi = "Benzin"
                        if "Dizel" in td_tag.text:
                            Yakit_Tipi = "Dizel"
                        if "Elektrikli" in td_tag.text:
                            Yakit_Tipi = "Elektrikli"
                        else:
                            if i == 1:
                                model = td_tag.text
                            elif i == 2:
                                fiyat = td_tag.text
                    try:
                        if "TL" in fiyat:
                            fiyat_int = int(fiyat.replace(".", "").replace("TL", "").replace(" ", ""))
                            if Yakit_Tipi != 'Unknown':
                                car_detail = model + ' ' + Yakit_Tipi
                                car_detail = car_detail.replace("Yeni ", "")

                                query = "Insert INTO [Raporlar].[dbo].[Peugeot_auto_data] (Marka, model, Fiyat, Kampanyali_Fiyat, Yakit_Tipi, tarih, car_detail) VALUES ('{}', '{}', {}, {}, '{}', '{}', '{}')".format("Peugeot", model, fiyat_int, 0, Yakit_Tipi, today, car_detail)
                                QueryToDB(YuceDB, query)

                                query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format("Peugeot", str(fiyat_int), '-', car_detail, today)
                                QueryToDB(YuceDB, query_dashboard)

                                amount_of_cars_inserted += 1
                    except:pass

            time.sleep(0.5)
    except:
        pass
    driver.quit()
    print("Peugeot_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))
    return amount_of_cars_inserted

# Scrapes the brand "Opel" and inserts data to db
# [Raporlar].[dbo].[Opel_auto_data]
def Opel_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Opel_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Opel'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://fiyatlisteleri.opel.com.tr/binek-araclar?gclid=EAIaIQobChMIxpm598vf_AIVCgeLCh0jgQ4pEAAYASABEgIGOvD_BwE&gclsrc=aw.ds")
    Fiyati_incele_btns = driver.find_elements("class name", 'pl-box')
    models_list = []
    amount_of_cars_inserted = 0
    for btn in Fiyati_incele_btns:
        a_tag = btn.find_element("tag name", 'a')
        models_list.append(a_tag.get_attribute('href'))
    for model_link in models_list:
        klist = []
        driver.get(model_link)
        versions_table = driver.find_element("class name", 'versions')
        tr_tags = versions_table.find_elements('tag name', 'tr')
        model = driver.find_element("xpath", '//*[@id="main"]/div[3]/header/div[1]/h1').text
        for tr_tag in tr_tags:
            if tr_tag.text != "Motor / Şanzıman Donanım Tavsiye Edilen Anahtar Teslim Fiyatı":
                td_tags = tr_tag.find_elements("tag name", 'td')
                i = 0
                for td_tag in td_tags:
                    if i == 0:
                        ozellik = td_tag.text.replace("\n"," ")
                    elif i == 1:
                        if td_tag.text.replace("\n", " ") != "Elegance XL":
                            paketler = td_tag.text.replace("\n", " ").split(" ")
                        else:
                            paketler = []
                            paketler.append(td_tag.text.replace("\n", " "))
                    elif i == 2:
                        fiyatlar = td_tag.text.replace("\n", " ").replace(" TL", 'TL').split(" ")
                    i += 1
                for j in range(len(paketler)):
                    car_detail = model + ' ' + ozellik + ' ' + paketler[j]
                    car_detail = car_detail.replace("Yeni ", "")
                    query = "Insert INTO [Raporlar].[dbo].[Opel_auto_data] (Marka, Model, Specs, Paket, Fiyat, Kampanyali_Fiyat, tarih, car_detail) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        "Opel", model, ozellik, paketler[j], fiyatlar[j].replace("TL", " TL"), '-', today, car_detail)
                    QueryToDB(YuceDB, query)

                    fiyat_int = fiyatlar[j].replace(".","").replace(" ","").replace("TL","").replace("tl","").replace(",","")
                    query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format("Opel", fiyat_int, "-", car_detail, today)
                    QueryToDB(YuceDB, query_dashboard)

                    amount_of_cars_inserted += 1

    driver.quit()
    print("Opel_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))
    return amount_of_cars_inserted

# Scrapes the brand "Cupra" and inserts data to db
# [Raporlar].[dbo].[Cupra_auto_data]
def Cupra_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Cupra_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Cupra'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://www.cupraofficial.com.tr/cupra-sahipleri/fiyat-listesi?utm_source=search&utm_medium=cpc&utm_campaign=cupra-search-08.21&gclid=Cj0KCQiApKagBhC1ARIsAFc7Mc5KRVD_UlcBN6nDwft_P7KTd7g7Rt3kJYL_0VKiUl4a3csA_tchb58aAh-sEALw_wcB")
    amount_of_cars_inserted = 0
    for i in range(20):
        if i != 0:
            try:
                xpath = '/html/body/div[3]/div/div/div/div[2]/div/div/div[{}]'.format(str(i))
                the_text = driver.find_element("xpath", xpath).text
                car_infoes = the_text.split("\n")
                model = car_infoes[0]
                specs = car_infoes[1]
                fiyat = car_infoes[2].replace("Tavsiye Edilen Anahtar Teslim Fiyatı: ", "").replace("₺", 'TL').replace("TL ", "TL")
                car_detail = model + ' ' + specs

                query = "Insert INTO [Raporlar].[dbo].[Cupra_auto_data] (Marka, Model, Specs, Fiyat, Kampanyali_Fiyat, tarih, car_detail) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        "Cupra", model, specs, fiyat, "-", today, car_detail)
                QueryToDB(YuceDB, query)

                fiyat_int = fiyat.replace(".","").replace(" ","").replace("TL","").replace("tl","").replace(",","")
                query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                    "Cupra", str(fiyat_int), '-', car_detail, today)
                QueryToDB(YuceDB, query_dashboard)

                amount_of_cars_inserted += 1
            except:
                break
    driver.quit()
    print("Cupra_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Kia" and inserts data to db
# [Raporlar].[dbo].[Kia_auto_data]
def Kia_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Kia_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Kia'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://www.kia.com/tr/satis-merkezi/fiyat-listesi.html")
    tables = driver.find_elements("tag name", 'table')
    amount_of_cars_inserted = 0
    for table in tables:
        # Data in tbody is in this part
        tbody = table.find_element("tag name", 'tbody')
        tr_tags1 = tbody.find_elements("tag name", 'tr')
        for tr_tag1 in tr_tags1:
            x = 0
            model = tr_tag1.find_element("tag name", 'th').text
            td_elements = tr_tag1.find_elements("tag name", 'td')
            for td_element in td_elements:
                if x == 0:
                    Yakit_Tipi = td_element.text.replace("\n"," ")
                elif x == 1:
                    Donanim = td_element.text.replace("\n"," ")
                elif x == 2:
                    Satis_Fiyati = td_element.text.replace("\n"," ")
                elif x == 3:
                    Kampanya_Destegi = td_element.text.replace("\n"," ")
                elif x == 4:
                    Kampanyali_Satis_Fiyati = td_element.text.replace("\n"," ")
                elif x == 5:
                    car_detail = model + ' ' + Yakit_Tipi + ' ' + Donanim
                    car_detail = car_detail.replace("Yeni ", "")

                    query = "Insert INTO [Raporlar].[dbo].[Kia_auto_data] (Marka, Model, YakitTipi, Donanim, Satis_Fiyati, Kampanya_Destegi, Kampanyali_Satis_Fiyati, tarih, car_detail) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        "Kia", model, Yakit_Tipi, Donanim, Satis_Fiyati, Kampanya_Destegi, Kampanyali_Satis_Fiyati, today, car_detail)
                    QueryToDB(YuceDB, query)

                    fiyat_int = Satis_Fiyati.replace(".","").replace(" ","").replace("TL","").replace("tl","").replace(",","")
                    Kampanyali_Satis_Fiyati_int = Kampanyali_Satis_Fiyati.replace(".","").replace(" ","").replace("TL","").replace("tl","").replace(",","")
                    query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                        "Kia", str(fiyat_int), Kampanyali_Satis_Fiyati_int, car_detail, today)
                    QueryToDB(YuceDB, query_dashboard)

                    amount_of_cars_inserted += 1
                x += 1
    driver.quit()
    print("Kia_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Volkswagen" and inserts data to db
# [Raporlar].[dbo].[Volkswagen_auto_data]
def Volkswagen_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Volkswagen_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Volkswagen'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    amount_of_cars_inserted = 0

    options = Options()
    #options.add_argument('--disable-javascript')
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://binekarac.vw.com.tr/app/local/fiyatlar/arac-fiyatlari.html")
    time.sleep(1)

    try:
        # Clicks to popping up cookies thingy
        driver.find_element("xpath", '//*[@id="bannerAcceptButton"]').click()
        time.sleep(0.5)
    except:pass

    collapsed_btns = driver.find_elements('class name', 'collapsed')

    # Opens each model's table in the loop
    for collapsed_btn in collapsed_btns:
        try:
            collapsed_btn.click()
            time.sleep(2)
            tables = driver.find_elements("tag name", 'table')
            for table in tables:

                # The table selected below is the correct table to be scraped
                if len(table.text) != 0:
                    table_ok = True # if the table headers order change in future, this variable will return False
                    # Headers are here
                    thead = table.find_element("tag name", 'thead')
                    tr_tag_in_thead = thead.find_element("tag name", 'tr')
                    th_tags = tr_tag_in_thead.find_elements("tag name", 'th')
                    headers = []
                    for th_tag in th_tags:
                        headers.append(th_tag.text)
                    if "Model" in headers[0]:
                        pass
                    else:
                        table_ok = False
                    if "Donanım" in headers[1]:
                        pass
                    else:
                        table_ok = False
                    if "Fiyat" in headers[2]:
                        pass
                    else:
                        table_ok = False
                    if len(headers) == 4:
                        pass
                    else:
                        table_ok = False
                    # Body data is here
                    tbody = table.find_element("tag name", 'tbody')
                    tr_tags_in_body = tbody.find_elements("tag name", 'tr')

                    # Each row of the table is below
                    for tr_tag in tr_tags_in_body:
                        td_tags = tr_tag.find_elements("tag name", 'td')
                        car_info = []
                        for td_tag in td_tags:
                            car_info.append(td_tag.text)
                        car_name = car_info[0].replace("yeni ", "").replace("Yeni ", "")
                        paket = car_info[1]
                        fiyat = car_info[2].replace("₺", "").replace(".00", "").replace(",","")
                        car_detail = car_name + " " + paket

                        query = "Insert INTO [Raporlar].[dbo].[Volkswagen_auto_data] (Marka, Model, Paket, Fiyat, Kampanyali_Fiyat, tarih, car_detail) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                            "Volswagen", car_name, paket, fiyat, "-", today, car_detail)
                        QueryToDB(YuceDB, query)

                        query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                            "Volkswagen", fiyat, "-", car_detail, today)
                        QueryToDB(YuceDB, query_dashboard)

                        amount_of_cars_inserted += 1

                    break
            collapsed_btn.click()
            time.sleep(1)
        except:
            pass
    driver.quit()
    print("Volkswagen_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))



    #print("Volkswagen_Scraper function is completed...")

# Scrapes the brand "Ford" and inserts data to db
# [Raporlar].[dbo].[Ford_auto_data]
def Ford_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery = "delete FROM [Raporlar].[dbo].[Ford_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Ford'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://www.ford.com.tr/arastir/size-uygun-araci-secin/brosur-ve-fiyat-listeleri/otomobil")
    time.sleep(1)
    car_count = 0
    count = 0
    car_info_links = []
    amount_of_cars_inserted = 0

    cars_are_here = driver.find_element("xpath", '//*[@id="collapse1"]/div/div/div/div/div')
    carz = cars_are_here.find_elements("tag name", 'a')
    for car in carz:
        car_info_links.append(car.get_attribute('href'))

    for link in car_info_links:
        driver.get(link)
        model = driver.current_url.replace("https://www.ford.com.tr/fiyat-listesi/ford-", "").replace("-fiyat-listesi", "")
        table = driver.find_element("tag name", "table")
        tr_tags = table.find_elements("tag name", "tr")
        tr_tag_count = 0
        for tr_tag in tr_tags:
            if tr_tag_count != 0:
                td_tags = tr_tag.find_elements("tag name", "td")
                cc = 0
                for td_tag in td_tags:
                    if cc == 0:
                        Model_yil = td_tag.text
                    if cc == 1:
                        Donanim = td_tag.text
                    if cc == 2:
                        Govde = td_tag.text
                    if cc == 3:
                        Motor = td_tag.text
                    if cc == 4:
                        Sanziman = td_tag.text
                    if cc == 5:
                        Yakit = td_tag.text
                    if cc == 6:
                        Emisyon = td_tag.text
                    if cc == 7:
                        T_Edilen_Anahtar_Teslim_fiyat = td_tag.text
                    if cc == 8:
                        T_Edilen_Kampanyali_Anahtar_Teslim_fiyat = td_tag.text
                    else:
                        T_Edilen_Kampanyali_Anahtar_Teslim_fiyat = "-"
                    cc += 1
                car_detail = model + ' ' + Donanim + ' ' + Govde + ' ' + Motor + ' ' + Sanziman + ' ' + Yakit
                car_detail = car_detail.replace("Yeni ", "").replace("yeni-","")

                query = "Insert INTO [Raporlar].[dbo].[Ford_auto_data] (Model, Model_yil, Donanim, Govde, Motor, Sanziman, Yakit, Emisyon, T_Edilen_Anahtar_Teslim_fiyat, T_Edilen_Kampanyali_Anahtar_Teslim_fiyat, tarih, car_detail) " \
                    "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                    model, Model_yil, Donanim, Govde, Motor, Sanziman, Yakit, Emisyon, T_Edilen_Anahtar_Teslim_fiyat, T_Edilen_Kampanyali_Anahtar_Teslim_fiyat, today, car_detail)
                QueryToDB(YuceDB, query)

                fiyat_int = T_Edilen_Anahtar_Teslim_fiyat.replace(".", "").replace(" ", "").replace("TL", "").replace("tl", "").replace(",", "")
                Kampanyali_Satis_Fiyati_int = T_Edilen_Kampanyali_Anahtar_Teslim_fiyat.replace(".", "").replace(" ", "").replace("TL","").replace("tl", "").replace(",", "")
                query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                    "Ford", str(fiyat_int), Kampanyali_Satis_Fiyati_int, car_detail, today)
                QueryToDB(YuceDB, query_dashboard)

                amount_of_cars_inserted += 1
            tr_tag_count += 1
    driver.quit()
    print("Ford_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Toyota" and inserts data to db
# [Raporlar].[dbo].[Toyota_auto_data]
def Toyota_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Toyota_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Toyota'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://turkiye.toyota.com.tr/middle/fiyatl_aksesuar.html?gclid=EAIaIQobChMI8N-iuczf_AIVtY9oCR11BAQbEAAYASABEgIrg_D_BwE&gclsrc=aw.ds#")
    tables_div = driver.find_element("xpath", '//*[@id="ContentWrapper"]/div[4]/div')
    car_names = tables_div.find_elements("class name", 'Title')
    tables = tables_div.find_elements("tag name", 'table')
    table_count = 0
    amount_of_cars_inserted = 0
    for table in tables:
        car_name = car_names[table_count].text.replace("Fiyatları", "")
        tr_tags = table.find_elements("tag name", 'tr')
        jk = 0
        for tr_tag in tr_tags:
            fiyat2 = "-"
            if jk != 0:
                td_tags = tr_tag.find_elements("tag name", 'td')
                leng = 0
                for td_tag in td_tags:
                    if td_tag.text != "":
                        if leng == 0:
                            modelname = td_tag.text
                        elif leng == 1:
                            fiyat1 = td_tag.text
                        elif leng == 2:
                            fiyat2 = td_tag.text
                        leng += 1
            elif jk == 0:
                td_tags = tr_tag.find_elements("tag name", 'td')
                for td_tag in td_tags:
                    versiyon = "-"
                    kampanyali_fiyat = "-"
                    tavsiyeli_fiyat = "-"
                    if td_tag.text != "-":
                        if "Versiyon" in td_tag.text:
                            versiyon = td_tag.text
                        elif "Kampanya" in td_tag.text:
                            kampanyali_fiyat = td_tag.text
                        else:
                            tavsiyeli_fiyat = td_tag.text
            jk += 1
            try:
                x = fiyat1
            except:
                fiyat1 = "-"
            try:
                x = fiyat2
            except:
                fiyat2 = "-"
            try:
                if jk != 1:
                    car_detail = car_name + ' ' + modelname
                    car_detail = car_detail.replace("Yeni ", "")
                    query = "Insert INTO [Raporlar].[dbo].[Toyota_auto_data] (car_name, modelname, fiyat1, fiyat2, tarih, car_detail) " \
                            "VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(car_name, modelname, fiyat1, fiyat2, today, car_detail)
                    QueryToDB(YuceDB, query)

                    fiyat_int_1 = fiyat1.replace(".", "").replace(" ", "").replace("TL","").replace("tl", "").replace(",", "")
                    fiyat_int_2 = fiyat2.replace(".", "").replace(" ","").replace("TL", "").replace("tl", "").replace(",", "")
                    if fiyat2 != "-":
                        Kampanyali_Satis_Fiyati_int = str(min(int(fiyat_int_1), int(fiyat_int_2)))
                        fiyat_int = str(max(int(fiyat_int_1), int(fiyat_int_2)))
                    elif fiyat2 == "-":
                        fiyat_int = fiyat1
                        Kampanyali_Satis_Fiyati_int = "-"
                        

                    query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                        "Toyota", str(fiyat_int), Kampanyali_Satis_Fiyati_int, car_detail, today)
                    QueryToDB(YuceDB, query_dashboard)

                    amount_of_cars_inserted += 1
            except:
                pass
        table_count += 1
    driver.quit()
    print("Toyota_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Renault" and inserts data to db
# [Raporlar].[dbo].[Renault_auto_data]
def Toyota_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Toyota_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Toyota'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://turkiye.toyota.com.tr/middle/fiyatl_aksesuar.html?gclid=EAIaIQobChMI8N-iuczf_AIVtY9oCR11BAQbEAAYASABEgIrg_D_BwE&gclsrc=aw.ds#")
    tables_div = driver.find_element("xpath", '//*[@id="ContentWrapper"]/div[4]/div')
    car_names = tables_div.find_elements("class name", 'Title')
    tables = tables_div.find_elements("tag name", 'table')
    table_count = 0
    amount_of_cars_inserted = 0
    for table in tables:
        car_name = car_names[table_count].text.replace("Fiyatları", "")
        tr_tags = table.find_elements("tag name", 'tr')
        jk = 0
        for tr_tag in tr_tags:
            fiyat2 = "-"
            if jk != 0:
                td_tags = tr_tag.find_elements("tag name", 'td')
                leng = 0
                for td_tag in td_tags:
                    if td_tag.text != "":
                        if leng == 0:
                            modelname = td_tag.text
                        elif leng == 1:
                            fiyat1 = td_tag.text
                        elif leng == 2:
                            fiyat2 = td_tag.text
                        leng += 1
            elif jk == 0:
                td_tags = tr_tag.find_elements("tag name", 'td')
                for td_tag in td_tags:
                    versiyon = "-"
                    kampanyali_fiyat = "-"
                    tavsiyeli_fiyat = "-"
                    if td_tag.text != "-":
                        if "Versiyon" in td_tag.text:
                            versiyon = td_tag.text
                        elif "Kampanya" in td_tag.text:
                            kampanyali_fiyat = td_tag.text
                        else:
                            tavsiyeli_fiyat = td_tag.text
            jk += 1
            try:
                x = fiyat1
            except:
                fiyat1 = "-"
            try:
                x = fiyat2
            except:
                fiyat2 = "-"
            try:
                if jk != 1:
                    car_detail = car_name + ' ' + modelname
                    car_detail = car_detail.replace("Yeni ", "")
                    query = "Insert INTO [Raporlar].[dbo].[Toyota_auto_data] (car_name, modelname, fiyat1, fiyat2, tarih, car_detail) " \
                            "VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(car_name, modelname, fiyat1, fiyat2, today, car_detail)
                    QueryToDB(YuceDB, query)

                    fiyat_int_1 = fiyat1.replace(".", "").replace(" ", "").replace("TL","").replace("tl", "").replace(",", "")
                    fiyat_int_2 = fiyat2.replace(".", "").replace(" ","").replace("TL", "").replace("tl", "").replace(",", "")
                    if fiyat2 != "-":
                        Kampanyali_Satis_Fiyati_int = str(min(int(fiyat_int_1), int(fiyat_int_2)))
                        fiyat_int = max(int(fiyat_int_1), int(fiyat_int_2))
                    elif fiyat2 == "-":
                        fiyat_int = fiyat_int_1
                        Kampanyali_Satis_Fiyati_int = "-"
                        

                    query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', {}, '{}', '{}', '{}')".format(
                        "Toyota", str(fiyat_int), Kampanyali_Satis_Fiyati_int, car_detail, today)
                    QueryToDB(YuceDB, query_dashboard)

                    amount_of_cars_inserted += 1
            except:
                pass
        table_count += 1
    driver.quit()
    print("Toyota_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Honda" and inserts data to db
# [Raporlar].[dbo].[Honda_auto_data]
def Honda_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Honda_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Honda'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = False
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://www.honda.com.tr/otomobil/modeller/jazz-hibrit/jazz-hibrit-fiyat-listesi")
    time.sleep(1.5)

    car_tags = driver.find_element("xpath", '//*[@id="root"]/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div')
    a_tags = car_tags.find_elements("tag name", 'a')
    amount_of_cars_inserted = 0
    time.sleep(2)
    for a_tag in a_tags:
        a_tag.click()
        time.sleep(5)

        model = driver.find_element("xpath", '//*[@id="root"]/div/div[2]/div/div/div[1]/div[3]/div/div[1]/div[1]/a[1]').text

        table_price_container = driver.find_element("class name", 'table-price-container')
        table_containers = table_price_container.find_elements("class name", 'table-container')

        for table_container in table_containers:
            data = table_container.text.split("\n")
            motor = data[0]
            sanziman = data[1]
            paket_fiyat = data[2:]
            for i in range(len(paket_fiyat)):
                if i % 2 == 0:
                    paket = paket_fiyat[i]
                elif i % 2 == 1:
                    fiyat = paket_fiyat[i]
                    car_detail = model + ' ' + motor + ' ' + sanziman + ' ' + paket
                    car_detail = car_detail.replace("Yeni ", "")

                    query = "Insert INTO [Raporlar].[dbo].[Honda_auto_data] (Model, Motor, Sanziman, Paket, Fiyat, Kampanyali_Fiyat, tarih, car_detail) " \
                        "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(model, motor, sanziman, paket, fiyat, '-', today, car_detail)
                    QueryToDB(YuceDB, query)

                    fiyat_int = fiyat.replace(".", "").replace(" ", "").replace("TL", "").replace("tl","").replace(",", "")
                    Kampanyali_Satis_Fiyati_int = "-"
                    query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                        "Honda", str(fiyat_int), Kampanyali_Satis_Fiyati_int, car_detail, today)
                    QueryToDB(YuceDB, query_dashboard)

                    amount_of_cars_inserted += 1
    driver.quit()
    print("Honda_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Nissan" and inserts data to db
# [Raporlar].[dbo].[Nissan_auto_data]
def Nissan_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Nissan_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Nissan'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://www.nissan.com.tr/fiyat-listesi/sifir-arac-fiyatlari.html")

    model_name_areas = driver.find_elements("class name", "c_001")
    modelNames = []

    for model_names in model_name_areas:
        model_name = driver.find_elements("tag name", "p")
        for model2 in model_name:
            mo = driver.find_elements("class name", "strapline")

    for m in mo:
        if m.text != "NISSAN TÜRKİYE":
            new_m = m.text.replace("2023 MODEL YENİ ","").replace("2023 MODEL ","").replace("YENİ ", "").replace("NISSAN ", "")
            modelNames.append(new_m)

    table_data_list = []

    price_tables = driver.find_elements("class name", "c_153")
    j = 0
    for price_table in price_tables:
        table_data = []
        i = 0
        e_counter = 0
        for row in price_table.find_elements("tag name", "tr"):
            row_data = []
            row_data.append(modelNames[j])
            for cell in row.find_elements("tag name", "td"):
                if i != 0:
                    if cell.text[:2] == "e-":
                        e_counter += 1
                        row_data.pop()
                        row_data.append(modelNames[j-1])
                        row_data.append(cell.text)
                    else:
                        row_data.append(cell.text)
            i += 1
            if len(row_data) == 1:
                pass
            else:
                table_data.append(row_data)

        if e_counter > 0:
            pass
        else:
            j += 1

        table_data_list.append(table_data)
    amount_of_cars_inserted = 0
    for table in table_data_list:
        for row in table:
            model = row[0].replace("*", "")
            specs = row[1].replace("*", "")
            fiyat = row[2].replace("*", "")
            kredi_kampanyali_fiyat = row[3].replace("*", "")
            nakit_kampanyali_fiyat = row[4].replace("*", "")

            car_detail = model + " " + specs

            query = "Insert INTO [Raporlar].[dbo].[Nissan_auto_data] (Marka, Model, Specs, Fiyat, Kredi_Kampanyali_Fiyat, Nakit_Kampanyali_Fiyat, tarih, car_detail) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                "Nissan", model, specs, fiyat, kredi_kampanyali_fiyat, nakit_kampanyali_fiyat, today, car_detail)
            QueryToDB(YuceDB, query)

            fiyat_int = fiyat.replace("TL", "").replace(" ", "").replace(".", "")
            nakit_kampanyali_fiyat_int = nakit_kampanyali_fiyat.replace("TL", "").replace(" ", "").replace(".", "")

            query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', {}, '{}', '{}', '{}')".format(
                "Nissan", fiyat_int, nakit_kampanyali_fiyat_int, car_detail, today)
            QueryToDB(YuceDB, query_dashboard)
            amount_of_cars_inserted += 1

    driver.quit()
    print("Nissan_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Seat" and inserts data to db
# [Raporlar].[dbo].[Seat_auto_data]
def Seat_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Seat_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Seat'".format(today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://www.seat.com.tr/firsatlar/fiyat-listesi/my-23/ibiza")
    time.sleep(2)
    detayli_list_btn = driver.find_element("xpath", '//*[@id="disclaimer_copy"]/div/div/div/div/div[4]/div/a')
    link = detayli_list_btn.get_attribute('href')


    # Downloads the PDF with Seat auto prices
    def download_pdf(url, filename):
        import requests

        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)

    # Converts the PDF table to Excel table
    def pdf_to_excel_seat(pdf_path, excel_path):
        import tabula
        import pandas as pd

        tables = tabula.read_pdf(pdf_path, pages=1)

        if isinstance(tables, list):
            df_combined = pd.concat(tables)
        else:
            df_combined = tables
        df_combined.to_excel(excel_path, index=False)

    # Returns a nested list of car details and prices
    def scrape_excel_seat(excel_path):
        import openpyxl

        workbook = openpyxl.load_workbook(excel_path)
        sheet = workbook['Sheet1']

        nested_list = []
        i = 0
        for row in sheet.iter_rows(values_only=True):
            row_list = []
            if i > 1:
                for cell_value in row:
                    if cell_value != None:
                        row_list.append(cell_value.replace("\n",""))
                nested_list.append(row_list)
            i += 1
        return nested_list

    download_pdf(link, "seat_fiyat_listesi.pdf")
    pdf_to_excel_seat("seat_fiyat_listesi.pdf", "seat_excel.xlsx")
    nested_list = scrape_excel_seat("seat_excel.xlsx")

    amount_of_cars_inserted = 0
    for each_list in nested_list:
        if len(each_list) > 2:
            car_detail = each_list[0]
            fiyat_2sondan = each_list[-2].replace("₺","")
            fiyat_1sondan = each_list[-1].replace("₺","")

            if fiyat_1sondan == "-":
                fiyat = fiyat_2sondan
                kampanyali_fiyat = "-"
            else:
                kampanyali_fiyat = fiyat_1sondan
                fiyat = fiyat_2sondan

            space_char_first = car_detail.find(" ")
            model = car_detail[:space_char_first]

            query = "Insert INTO [Raporlar].[dbo].[Seat_auto_data] (Marka, Model, Paket, Fiyat, Kampanyali_Fiyat, tarih, car_detail) " \
                    "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format("Seat", model, "-", fiyat, kampanyali_fiyat, today, car_detail)
            QueryToDB(YuceDB, query)

            fiyat_int = fiyat.replace(".", "").replace(" ", "").replace("TL", "").replace("tl", "").replace(",", "").replace("₺","")
            kampanyali_fiyat = kampanyali_fiyat.replace(".", "").replace(" ", "").replace("TL", "").replace("tl", "").replace(",", "").replace("₺","")

            query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                "Seat", fiyat_int, kampanyali_fiyat, car_detail, today)
            QueryToDB(YuceDB, query_dashboard)

            amount_of_cars_inserted += 1

    os.remove("seat_fiyat_listesi.pdf")
    os.remove("seat_excel.xlsx")

    driver.quit()

    print("Seat_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Citroen" and inserts data to db
# [Raporlar].[dbo].[Citroen_auto_data]
def Citroen_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime('%d.%m.%Y')

    amount_of_cars_inserted = 0

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Citroen_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Citroen'".format(today)
    QueryToDB(YuceDB, qu_ery2)
    try:
        options = Options()
        options.headless = True
        driver = uc.Chrome(use_subprocess=True, options=options)

        driver.get("https://talep.citroen.com.tr/fiyat-listesi")

        # Finds the div that includes all "a" tags inside
        model_link = driver.find_element("class name", "ModelTabs_models__sQg7P")

        # car models are here
        carmodels = model_link.find_elements("class name", "ModelTabs_CarWithImage__cjC_W ")

        car_links= []
        for carmodel in carmodels:
            car_links.append(carmodel.get_attribute("href"))

        table_data_list = []

        for link in car_links:
            driver.get(link)

            #Finds the model name of each link
            model_div = driver.find_element("class name", "DijitalKatalog_PriceListMain__kSp5e")
            model_name = model_div.find_element("tag name", "h1").text

            #Finds the table that has the price info
            price_table = driver.find_element("class name", "DijitalKatalog_PriceList__lJ07h")

            table_data = []

            for row in price_table.find_elements("tag name", "tr"):
                row_data = []
                i = 0
                if len(row.find_elements("tag name", "td"))>1:
                    row_data.append(model_name)
                    i+=1
                for cell in row.find_elements("tag name", "td"):
                    if i == 1:
                        row_data.append(cell.text.replace("\n", " "))
                    elif i > 1:
                        row_data.append(cell.text.split("\n"))
                    i += 1
                table_data.append(row_data)

            for item in table_data:
                if item == []:
                    table_data.remove(item)

            table_data_list.append(table_data)

        for table in table_data_list:
            for row in table:
                for i in range(len(row[-1])):
                    model = row[0].replace("CITROËN ","")
                    versiyon = row[1]
                    paket = row[2][i]
                    yil = row[3][i]
                    fiyat = row[4][i]
                    car_detail = model + " " + versiyon + " " + paket
                    car_detail = car_detail.replace("YENİ ", "").replace("Yeni ", "").replace("yeni ", "")

                    amount_of_cars_inserted += 1

                    query = "Insert INTO [Raporlar].[dbo].[Citroen_auto_data] (Marka, Model, Versiyon, Paket, Fiyat, Kampanyali_Fiyat, tarih, car_detail) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        "Citroen", model, versiyon, paket, fiyat, '-', today, car_detail)
                    QueryToDB(YuceDB, query)

                    fiyat_int = fiyat.replace("TL", "").replace(" ", "").replace(".", "")

                    query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                        "Citroen", fiyat_int, "-", car_detail, today)
                    QueryToDB(YuceDB, query_dashboard)
    except:
        pass
    driver.quit()
    print("Citroen_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Hyundai" and inserts data to db
# [Raporlar].[dbo].[Hyundai_auto_data]
def Hyundai_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime("%d.%m.%Y")

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Hyundai_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Hyundai'".format(
        today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://www.hyundai.com/tr/tr/arac-satis/arac-fiyat-listesi")

    table_data_list = []

    list_wrap = driver.find_element("class name", "togListWrap")
    divs = list_wrap.find_elements("class name", "togList")
    j = 0
    for div in divs:
        try:
            h3_tag = div.find_element("tag name", "h3")
            outer_element_of_h3 = h3_tag.find_element("xpath", "..")

            if j == 0:
                pass
            else:
                driver.execute_script("arguments[0].scrollIntoView();", outer_element_of_h3)
                outer_element_of_h3.click()
                time.sleep(1)

            table_data = []

            i = 0
            price_table = div.find_element("class name", "tableTypeCol4")
            for row in price_table.find_elements("tag name", "tr"):
                row_data = []
                if i != 0:
                    row_data.append(h3_tag.text.replace("Yeni ", "").replace("YENİ ", ""))
                    for cell in row.find_elements("tag name", "td"):
                        row_data.append(cell.text)
                    table_data.append(row_data)
                i += 1
            table_data_list.append(table_data)

            j += 1
        except:
            pass
    amount_of_cars_inserted = 0
    for table in table_data_list:
        for row in table:
            model = row[0].replace("*","")
            specs = row[1].replace("*","")
            yakit = row[2].replace("*","")
            sanziman = row[3].replace("*","")
            fiyat = row[4].replace("*","")
            kampanyali_fiyat = row[5].replace("*","")

            car_detail = model + " " + specs + " " + yakit + " " + sanziman

            query = "Insert INTO [Raporlar].[dbo].[Hyundai_auto_data] (Marka, Model, Specs, Yakit, Sanziman, Fiyat, Kampanyali_Fiyat, tarih, car_detail) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                "Hyundai", model, specs, yakit, sanziman, fiyat, kampanyali_fiyat, today, car_detail)
            QueryToDB(YuceDB, query)

            fiyat_int = fiyat.replace("TL", "").replace(" ", "").replace(".", "")
            kampanyali_fiyat_int = kampanyali_fiyat.replace("TL", "").replace(" ", "").replace(".", "")

            query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', {}, '{}', '{}', '{}')".format(
                "Hyundai", fiyat_int, kampanyali_fiyat_int, car_detail, today)
            QueryToDB(YuceDB, query_dashboard)
            amount_of_cars_inserted += 1

    driver.quit()
    print("Hyundai_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))

# Scrapes the brand "Dacia" and inserts data to db
# [Raporlar].[dbo].[Dacia_auto_data]
def Dacia_Scraper():
    sene = datetime.datetime.now().year
    today = datetime.datetime.today()
    today = today.strftime("%d.%m.%Y")

    qu_ery1 = "delete FROM [Raporlar].[dbo].[Dacia_auto_data] where tarih = '{}'".format(today)
    QueryToDB(YuceDB, qu_ery1)

    qu_ery2 = "delete FROM [Raporlar].[dbo].[dashboard_auto_data] where tarih = '{}' and Marka = 'Dacia'".format(
        today)
    QueryToDB(YuceDB, qu_ery2)

    options = Options()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get("https://www.dacia.com.tr/dacia-fiyat-listesi.html")
    time.sleep(5)

    iframe = driver.find_element("tag name", "iframe")
    driver.switch_to.frame(iframe)

    car_models = driver.find_element("class name", "col-md")
    model_tables = car_models.find_elements("tag name", "fiyat-list")

    model_names = []

    for model_table in model_tables:
        model_name = model_table.find_element("tag name", "h2")
        model_names.append(model_name.text)

    price_tables = []

    for model_table in model_tables:
        price_table = model_table.find_element("class name", "price-table")
        price_tables.append(price_table)

    table_data_list = []

    j = 0

    for table in price_tables:
        i = 0
        table_data = []
        for row in table.find_elements("tag name", "tr"):
            row_data = []
            if i != 0:
                row_data.append(model_names[j])
                for cell in row.find_elements("tag name", "td"):
                    row_data.append(cell.text)
                table_data.append(row_data)
            i += 1
        table_data_list.append(table_data)

        j += 1
    amount_of_cars_inserted = 0
    for table in table_data_list:
        for row in table:
            model = row[0].replace("YENİ ", "").replace("\nSATIN ALIN", "")
            specs = row[1]
            fiyat = row[2].replace("₺", "")

            car_detail = model + " " + specs

            query = "Insert INTO [Raporlar].[dbo].[Dacia_auto_data] (Marka, Model, Specs, Fiyat, tarih, car_detail) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                "Dacia", model, specs, fiyat, today, car_detail)
            QueryToDB(YuceDB, query)

            fiyat_int = fiyat.replace("TL", "").replace(" ", "").replace(".", "")

            query_dashboard = "Insert INTO [Raporlar].[dbo].[dashboard_auto_data] (Marka, Fiyat, Kampanyali_Fiyat, car_detail, tarih) VALUES ('{}', {}, '{}', '{}', '{}')".format(
                "Dacia", fiyat_int, "-", car_detail, today)
            QueryToDB(YuceDB, query_dashboard)
            amount_of_cars_inserted += 1

    driver.quit()
    print("Dacia_Scraper function is completed... ({} cars inserted)".format(amount_of_cars_inserted))




