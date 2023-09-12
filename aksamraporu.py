from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
#from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from datetime import datetime
import pandas as pd
import warnings
import time
import os
warnings.filterwarnings("ignore", category=DeprecationWarning)
from config import *
from aksamraporu_email_html import aksamraporu_email_html
from format_with_period import format_with_period
from send_email import send_email
from plotting_graphs import *
import base64
from PIL import Image
import pymysql


def AksamRaporuComplete(turkuazusername, turkuazpw):
    today = datetime.today().strftime("%d-%m-%Y")
    today = today.replace("-", ".")
    month_start = "01" + today[2:].replace("-", ".")
    yil = datetime.now().year
    year_start = '01.01.' + str(yil)

    # Opens driver and directs to login page
    options = Options()
    options.headless = True
    driver = uc.Chrome(options=options)

    driver.get("https://turkuaz.dohas.com.tr/Admin/UILogin.aspx?ReturnUrl=%2f&__0186262C9018__=BQTQ4GMAmhTUYA%3d%3d__")
    time.sleep(1.5)

    # Logs in
    driver.find_element("xpath", '//*[@id="txtUserName"]').send_keys(turkuazusername)
    driver.find_element("xpath", '//*[@id="txtPassword"]').send_keys(turkuazpw)
    driver.find_element("xpath", '//*[@id="btnEnter"]').click()
    try:
        driver.find_element("xpath", '//*[@id="btnEnter"]').click()
    except:
        pass

    driver.get("https://turkuaz.dohas.com.tr/UIGeneralTask.aspx?Menu1Selected=16&Menu2Selected=345&mPressed=1&Key=9&__01862656D11D__=BtXa4GMAAJoU1GA%3d__")
    time.sleep(1)
    driver.find_element("xpath", '//*[@id="_ctl0_TaskContent_rptTaskLink_lnkDistributorMonthlySales"]').click()
    time.sleep(1)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(today)
    
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)

    # Clicks to calculate button
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1.5)

    # Gün için olan Toplam Net Satış değeri
    Toplam_net_satis_day = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[6]/td[14]').text


    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(month_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)
    
    # Clicks to calculate button
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1.5)

    # Ay için olan Toplam Net Satış Değeri
    Toplam_net_satis_month = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[6]/td[14]').text


    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(year_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)
    
    # Clicks to calculate button
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1.5)

    Toplam_net_satis_year = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[6]/td[14]').text

    Toptan = {}
    Toptan['day'] = Toplam_net_satis_day
    Toptan['month'] = Toplam_net_satis_month
    Toptan['year'] = Toplam_net_satis_year

    driver.get("https://turkuaz.dohas.com.tr/UIGeneralTask.aspx?Menu1Selected=16&Menu2Selected=345&mPressed=1&Key=9&__01869CCC2077__=BRwu)2MAX7yQZw%3d%3d__")
    driver.find_element("xpath", '//*[@id="_ctl0_TaskContent_rptTaskLink_lnkADMonthlySales"]').click()
    time.sleep(1.5)


    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(today)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)
    
    # Clicks to calculate button
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()

    td_rows = driver.find_elements("tag name", 'td')
    for e in td_rows:
        if 'Toplam Satış' in e.text:
            long_text = e.text
            elements_list = long_text.split("\n")
            for element in elements_list:
                if 'Toplam Satış' in element:
                    Toplam_satis_list = element.split(" ")
                    try:
                        value = Toplam_satis_list[14]
                    except:pass
    try:
        Perakende_satis_day = value
    except:
        Perakende_satis_day = 0

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(month_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)
    
    # Clicks to calculate button
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()

    td_rows = driver.find_elements("tag name", 'td')
    for e in td_rows:
        if 'Toplam Satış' in e.text:
            long_text = e.text
            elements_list = long_text.split("\n")
            for element in elements_list:
                if 'Toplam Satış' in element:
                    Toplam_satis_list = element.split(" ")
                    try:
                        value = Toplam_satis_list[14]
                    except:
                        pass
    try:
        Perakende_satis_month = value
    except:
        Perakende_satis_month = 0

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(year_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)
    
    # Clicks to calculate button
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()

    td_rows = driver.find_elements("tag name", 'td')
    for e in td_rows:
        if 'Toplam Satış' in e.text:
            long_text = e.text
            elements_list = long_text.split("\n")
            for element in elements_list:
                if 'Toplam Satış' in element:
                    Toplam_satis_list = element.split(" ")
                    try:
                        value = Toplam_satis_list[14]
                    except:
                        pass
    Perakende_satis_year = value

    Perakende = {}
    Perakende['day'] = Perakende_satis_day
    Perakende['month'] = Perakende_satis_month
    Perakende['year'] = Perakende_satis_year

    # <-- TABLE II -->


    driver.get("https://turkuaz.dohas.com.tr/Vehicle/Sales/DSSales/Invoice/UIVehicleInvoiceADTotalSalesSearch.aspx?Menu1Selected=16&Menu2Selected=345&mPressed=1&Key=9&__0186B5D87B9A__=BayXBWQAIN0ZVA%3d%3d__")
    time.sleep(0.5)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(today)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1.5)

    try:
        tbodies = driver.find_elements("tag name", "tbody")

        tbody = tbodies[-2]

        tr_tags = tbody.find_elements("tag name", "tr")

        for tr_tag in tr_tags:
            if "Toplam Satış" in tr_tag.text:
                values1 = tr_tag.text.split(" ")
        Toplam_Satis_Day = values1[-3]
    except:
        Toplam_Satis_Day = 0

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(month_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1.5)
    
    try:
        tbodies = driver.find_elements("tag name", "tbody")

        tbody = tbodies[-2]

        tr_tags = tbody.find_elements("tag name", "tr")

        for tr_tag in tr_tags:
            if "Toplam Satış" in tr_tag.text:
                values7 = tr_tag.text.split(" ")
        Toplam_Satis_Month = values7[-3]
    except:
        Toplam_Satis_Month = 0

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(year_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)

    # Clicks to calculate button
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1.5)

    try:
        tbodies = driver.find_elements("tag name", "tbody")

        tbody = tbodies[-2]

        tr_tags = tbody.find_elements("tag name", "tr")

        for tr_tag in tr_tags:
            if "Toplam Satış" in tr_tag.text:
                values4 = tr_tag.text.split(" ")
        Toplam_Satis_Year = values4[-3]
    except:
        Toplam_Satis_Year = 0


    driver.get("https://turkuaz.dohas.com.tr/Vehicle/Sales/DSSales/Invoice/UIVehicleInvoiceADTotalSalesSearch.aspx?Menu1Selected=16&Menu2Selected=345&mPressed=1&Key=9&__0186B5D87B9A__=BayXBWQAIN0ZVA%3d%3d__")
    time.sleep(0.5)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(today)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1.5)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_TurkuazDialogButton2"]').click()
    time.sleep(0.5)

    # Here it uses the popping up iframe part
    iframe = driver.find_element("id", "dialog-body")
    driver.switch_to.frame(iframe)
    driver.find_element("xpath", '//*[@id="_ctl0_DataGridBeforeButtonArea_grdSalesTypeList__ctl3_chkStatus"]').click()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnSave"]').click()
    time.sleep(6)
    driver.switch_to.default_content()

    # Back to the driver Turkuaz is opened
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(2)

    try:
        tbodies = driver.find_elements("tag name", "tbody")

        tbody = tbodies[-2]

        tr_tags = tbody.find_elements("tag name", "tr")

        for tr_tag in tr_tags:
            if "Toplam Satış" in tr_tag.text:
                values5 = tr_tag.text.split(" ")
        Toplam_Satis_Filo_Day = values5[-3]
    except:
        Toplam_Satis_Filo_Day = "0"

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(month_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1.5)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(2)

    try:
        tbodies = driver.find_elements("tag name", "tbody")

        tbody = tbodies[-2]

        tr_tags = tbody.find_elements("tag name", "tr")

        for tr_tag in tr_tags:
            if "Toplam Satış" in tr_tag.text:
                values2 = tr_tag.text.split(" ")
        Toplam_Satis_Filo_Month = values2[-3]
    except:
        Toplam_Satis_Filo_Month = "0"

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(year_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1.5)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(2)

    try:
        tbodies = driver.find_elements("tag name", "tbody")

        tbody = tbodies[-2]

        tr_tags = tbody.find_elements("tag name", "tr")

        for tr_tag in tr_tags:
            if "Toplam Satış" in tr_tag.text:
                values3 = tr_tag.text.split(" ")
        Toplam_Satis_Filo_Year = values3[-3]
    except:
        Toplam_Satis_Filo_Year = "0"


    driver.get("https://turkuaz.dohas.com.tr/UIGeneralTask.aspx?Menu1Selected=16&Menu2Selected=345&mPressed=1&Key=9&__0186A23549EF__=B7aQAGQAAAAW)gYS__")
    driver.find_element("xpath", '//*[@id="_ctl0_TaskContent_rptTaskLink_lnkDistributorMonthlySales"]').click()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(today)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1)

    today_toplamnetsatis = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[6]/td[14]').text
    today_diger_satis = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[3]/td[14]').text

    selectbox = driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_drpSalesType"]')
    select_object = Select(selectbox)
    select_object.select_by_value("2")

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1)

    today_Filo_toplamnetsatis = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[6]/td[14]').text


    driver.get('https://turkuaz.dohas.com.tr/Vehicle/Sales/DSSales/Invoice/UIVehicleInvoiceTotalSalesSearch.aspx?Menu1Selected=16&Menu2Selected=345&mPressed=1&Key=9&__0186A6D4A474__=CKe)AWQAAAAAgQ00XQ%3d%3d__')

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(month_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1)

    thismonth_toplamnetsatis = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[6]/td[14]').text
    thismonth_diger_satis = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[3]/td[14]').text

    selectbox = driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_drpSalesType"]')
    select_object = Select(selectbox)
    select_object.select_by_value("2")

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1)

    thismonth_Filo_toplamnetsatis = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[6]/td[14]').text

    driver.get('https://turkuaz.dohas.com.tr/Vehicle/Sales/DSSales/Invoice/UIVehicleInvoiceTotalSalesSearch.aspx?Menu1Selected=16&Menu2Selected=345&mPressed=1&Key=9&__0186A6D4A474__=CKe)AWQAAAAAgQ00XQ%3d%3d__')


    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(year_start)

    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(today)
    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1)

    thisyear_toplamnetsatis = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[6]/td[14]').text
    thisyear_diger_satis = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[3]/td[14]').text

    selectbox = driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_drpSalesType"]')
    select_object = Select(selectbox)
    select_object.select_by_value("2")

    driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
    time.sleep(1)

    thisyear_Filo_toplamnetsatis = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[6]/td[14]').text

    today_filo_to_bewritten = format_with_period(int(today_Filo_toplamnetsatis.replace(".","")) + int(today_diger_satis.replace(".","")))
    today_Perakende_to_bewritten = format_with_period(int(today_toplamnetsatis.replace(".","")) - (int(today_Filo_toplamnetsatis.replace(".","")) + int(today_diger_satis.replace(".",""))))
    Toptan_Gun = "{} ( {} F + {} P )".format(today_toplamnetsatis, today_filo_to_bewritten, today_Perakende_to_bewritten)

    thismonth_filo_to_bewritten = format_with_period(int(thismonth_Filo_toplamnetsatis.replace(".", "")) + int(thismonth_diger_satis.replace(".", "")))
    thismonth_Perakende_to_bewritten = format_with_period(int(thismonth_toplamnetsatis.replace(".","")) - (int(thismonth_Filo_toplamnetsatis.replace(".","")) + int(thismonth_diger_satis.replace(".",""))))
    Toptan_Ay = "{} ( {} F + {} P )".format(thismonth_toplamnetsatis, thismonth_filo_to_bewritten, thismonth_Perakende_to_bewritten)


    thisyear_filo_to_bewritten = format_with_period(int(thisyear_Filo_toplamnetsatis.replace(".", "")) + int(thisyear_diger_satis.replace(".", "")))
    thisyear_Perakende_to_bewritten = format_with_period(int(thisyear_toplamnetsatis.replace(".","")) - (int(thisyear_Filo_toplamnetsatis.replace(".","")) + int(thisyear_diger_satis.replace(".",""))))
    Toptan_Yil = "{} ( {} F + {} P )".format(thisyear_toplamnetsatis, thisyear_filo_to_bewritten, thisyear_Perakende_to_bewritten)


    # PART III excel download & read
    driver.get("https://turkuaz.dohas.com.tr/UIGeneralTask.aspx?Menu1Selected=16&Menu2Selected=730&mPressed=1&Key=354&__0186A276AE01__=BXShAGQAFv4GEg%3d%3d__")
    time.sleep(1.5)
    driver.find_element("xpath", '//*[@id="_ctl0_ReportContent_rptReportLink_lnkDailyVehicleSalesAndConnectionReportForDS"]').click()
    time.sleep(0.5)

    # Downloads the excel that is required
    driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_lnkModelBasedDailySales"]').click()
    time.sleep(3.0)
    try:
        try:
            df = pd.read_excel(Model_Kirilimli)
        except:
            time.sleep(3.5)
            df = pd.read_excel(Model_Kirilimli)
    except:
        time.sleep(10)
        df = pd.read_excel(Model_Kirilimli)

    def find_sum_in_excel(column_order):
        start_value = 0
        for i in range(40):
            try:
                column_name = 'Unnamed: {}'.format(str(column_order))
                value = df.at[i+30, column_name]
                try:
                    if value >= start_value:
                        start_value = value
                except:
                    pass
            except:
                pass
        return start_value

    Fabia_value = find_sum_in_excel(15)
    Kamiq_value = find_sum_in_excel(16)
    Karoq_value = find_sum_in_excel(17)
    Kodiaq_value = find_sum_in_excel(18)
    Octavia_value = find_sum_in_excel(19)
    Scala_value = find_sum_in_excel(20)
    Superb_value = find_sum_in_excel(21)
    Sum_value = find_sum_in_excel(22)

    os.remove(Model_Kirilimli)

    gun_p1 = int(str(Toplam_Satis_Day).replace(".","")) - int(str(Toplam_Satis_Filo_Day).replace(".",""))
    gun_p1 = format_with_period(gun_p1)
    Perakende_gun = "{} ( {} F + {} P )".format(Toplam_Satis_Day, Toplam_Satis_Filo_Day, gun_p1)

    ay_p2 = int(str(Toplam_Satis_Month).replace(".", "")) - int(str(Toplam_Satis_Filo_Month).replace(".", ""))
    ay_p2 = format_with_period(ay_p2)
    Perakende_ay = "{} ( {} F + {} P )".format(Toplam_Satis_Month, Toplam_Satis_Filo_Month, ay_p2)

    yil_p3 = int(str(Toplam_Satis_Year).replace(".", "")) - int(str(Toplam_Satis_Filo_Year).replace(".", ""))
    yil_p3 = format_with_period(yil_p3)
    Perakende_yil = "{} ( {} F + {} P )".format(Toplam_Satis_Year, Toplam_Satis_Filo_Year, yil_p3)


    driver.get("https://turkuaz.dohas.com.tr/UIGeneralTask.aspx?Menu1Selected=16&Menu2Selected=730&mPressed=1&Key=354&__0186CB5AF5AB__=BlUZC2QAAM(xf1Y%3d__")
    driver.find_element("xpath", '//*[@id="_ctl0_TaskContent_rptTaskLink_lnkDailyVehicleSalesAndConnectionRecordView"]').click()

    for i in range(80, 40, -1):
        try:
            result = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdDealerData"]/tbody/tr[{}]'.format(str(i)))
            break
        except:pass
    result_splitted = result.text.split('\n')

    GelenTelefonAdet_Bugun = result_splitted[0].replace("TOPLAM", "").split(" ")[1]
    GelenMusteriAdet_Bugun = result_splitted[0].replace("TOPLAM", "").split(" ")[2]
    Baglanti_Bugun = result_splitted[2].replace("Toplam(", '').replace(")", "")
    Perakende_Satis_Bugun = gun_p1

    driver.get("https://www.google.com/search?q=eurokuru&rlz=1C1GCEU_trTR1020TR1020&oq=eurokuru&aqs=chrome..69i57j46i10i175i199i433i512j0i512j0i10i512l2j0i10i433i512j0i10i512l3.2328j1j7&sourceid=chrome&ie=UTF-8")
    euro_kur = driver.find_element("xpath", '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').text

    driver.quit()


    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "INSERT INTO graph_data (Tarih, Day, Month, Year, GelenTelefon, GelenMusteri, Baglanti, Perakende_Satis, euro_kur) SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM graph_data WHERE Tarih = %s);"
    Month_tobe_inserted = today[3:5].lstrip("0")
    values = (today, today[:2], Month_tobe_inserted, today[-4:], GelenTelefonAdet_Bugun, GelenMusteriAdet_Bugun, Baglanti_Bugun, Perakende_Satis_Bugun, euro_kur.replace(',','.'), today)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    plot_visitor_phonecall_graph()
    #plot_Baglanti_graph()
    plot_Perakende_Satis_graph()
    plot_Kur_graph()

    image = Image.open('Gelen_Musteri_Telefon_Graph.png')
    width, height = image.size
    top_offset = 15
    bottom_offset = 0
    left_offset = 20
    right_offset = 40
    left = left_offset
    right = width - right_offset
    cropped_image = image.crop((left, top_offset, right, height - bottom_offset))
    cropped_image.save('Gelen_Musteri_Telefon_Graph.png')

    """
    image = Image.open('Baglanti_Graph.png')
    width, height = image.size
    top_offset = 15
    bottom_offset = 0
    left_offset = 20
    right_offset = 40
    left = left_offset
    right = width - right_offset
    cropped_image = image.crop((left, top_offset, right, height - bottom_offset))
    cropped_image.save('Baglanti_Graph.png')
    """

    image = Image.open('Perakende_Satis_Graph.png')
    width, height = image.size
    top_offset = 15
    bottom_offset = 0
    left_offset = 20
    right_offset = 40
    left = left_offset
    right = width - right_offset
    cropped_image = image.crop((left, top_offset, right, height - bottom_offset))
    cropped_image.save('Perakende_Satis_Graph.png')

    image = Image.open('Kur_Graph.png')
    width, height = image.size
    top_offset = 15
    bottom_offset = 0
    left_offset = 20
    right_offset = 40
    left = left_offset
    right = width - right_offset
    cropped_image = image.crop((left, top_offset, right, height - bottom_offset))
    cropped_image.save('Kur_Graph.png')

    image_paths = []
    encoded_images = []
    image_path1 = os.path.join(os.getcwd(), "Gelen_Musteri_Telefon_Graph.png")
    #image_path2 = os.path.join(os.getcwd(), "Baglanti_Graph.png")
    image_path3 = os.path.join(os.getcwd(), "Perakende_Satis_Graph.png")
    image_path4 = os.path.join(os.getcwd(), "Kur_Graph.png")

    image_paths.append(image_path1)
    #image_paths.append(image_path2)
    image_paths.append(image_path3)
    image_paths.append(image_path4)

    for image_path in image_paths:
        with open(image_path, "rb") as f:
            image_data = f.read()
            encoded_images.append(base64.b64encode(image_data).decode("utf-8"))

    email_content = aksamraporu_email_html.format(today, Perakende['day'], Perakende['month'], Perakende['year'],
                                                  Toptan['day'], Toptan['month'], Toptan['year'], Perakende_gun, Perakende_ay, Perakende_yil, Toptan_Gun,
                                                  Toptan_Ay, Toptan_Yil, Fabia_value, Kamiq_value, Karoq_value, Kodiaq_value, Octavia_value, Scala_value,
                                                  Superb_value, Sum_value,
                                                  encoded_images[0],
                                                  encoded_images[1],
                                                  encoded_images[2],
                                                  #encoded_images[3]
                                                  )

    send_email(email_content, "Akşam raporu", "aslis@skoda.com.tr", cc_email="dogao@skoda.com.tr", sender_email='aksamraporu@skoda.com.tr')
    send_email(email_content, "Akşam raporu", "afizeo@skoda.com.tr", sender_email='aksamraporu@skoda.com.tr')
    send_email(email_content, "Akşam raporu", "busray@skoda.com.tr", sender_email='aksamraporu@skoda.com.tr')
    send_email(email_content, "Akşam raporu", "stj_b.basara@skoda.com.tr", sender_email='aksamraporu@skoda.com.tr')

    os.remove('Gelen_Musteri_Telefon_Graph.png')
    #os.remove('Baglanti_Graph.png')
    os.remove('Perakende_Satis_Graph.png')
    os.remove('Kur_Graph.png')
