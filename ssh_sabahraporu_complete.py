from datetime import datetime, timedelta, date
import calendar
import pymysql
import base64
import time
import os
from SSH_datascraper import TurkuazDataReader1, ParcaSatis_excel_downloader
from format_with_period import format_with_period
from ssh_email_html import email_html
from send_email import send_email
from ssh_excel_readers import *
from ssh_graphs import *
from ssh_datefuncs import *
from config import *

def SSH_sabahraporu_complete(Turkuaz_username, Turkuaz_password, first_day_check):
    today = date.today()
    start_day_last_year = datetime(today.year - 1, today.month, 1).strftime('%d.%m.%Y')
    start_day_thismonth_thisyear = datetime(today.year, today.month, 1).strftime('%d.%m.%Y')

    last_day_worked = last_work_day()
    formatted_last_day_worked = convert_date_Turkish_num(last_day_worked)
    sene = datetime.now().year
    month = datetime.now().month
    gecen_sene = sene - 1
    if first_day_check == True:
        month = month - 1


    last_year_end_date = Return_lastyear_enddate()
    Parca_Satis_Hedef, İs_Emri_Hedef = Read_Hedefler_from_Excel('Copy of Tatil Günleri ve Hedef.xlsx', 'Hedef', month)

    today = datetime.today().strftime("%d.%m.%Y")

    howmanydaysleft_ = howmanydaysleft()
    
    if first_day_check == True:
        current_date = datetime.now()
        first_day_of_current_month = current_date.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        
        last_day_worked = last_work_day(first_day_check)

        start_day_thismonth_thisyear = last_day_of_previous_month.replace(day=1).strftime('%d.%m.%Y')

        last_year_end_date = last_day_of_previous_month.replace(year=last_day_of_previous_month.year - 1).strftime('%d.%m.%Y')

        start_day_last_year = "01" + last_year_end_date[2:]

        howmanydaysleft_ = 0


    #TurkuazDataReader1(Turkuaz_username, Turkuaz_password, last_day_worked, last_day_worked)
    #RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls", "Iscilik_Parca_SonCalisilanGun_Raporu.xls")
    İsemri_Adedi, ServisGiris = Read_SSH_Iscilik_ParcaGelirleri_Excel(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_SonCalisilanGun_Raporu.xls", 'Marka Bazlı Fatura Detayları')
    isEmri_Gun, Garanti_Gun = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_SonCalisilanGun_Raporu.xls", 'Marka Bazlı Fatura Detayları')
    #os.remove(r"C:\Users\dogao\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls")


    #TurkuazDataReader1(Turkuaz_username, Turkuaz_password, start_day_last_year, last_year_end_date)
    #RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls", "Iscilik_Parca_GecenSeneAylik_Rapor.xls")
    İsemri_Adedi_Gecensene, ServisGiris_Gecensene = Read_SSH_Iscilik_ParcaGelirleri_Excel(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenSeneAylik_Rapor.xls", 'Marka Bazlı Fatura Detayları')
    isEmri_Gecensene, Garanti_Gecensene = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenSeneAylik_Rapor.xls", 'Marka Bazlı Fatura Detayları')
    #os.remove(r"C:\Users\dogao\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls")
    

    #TurkuazDataReader1(Turkuaz_username, Turkuaz_password, start_day_thismonth_thisyear, last_day_worked)
    #RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls", "Iscilik_Parca_BuAyKumule_Rapor.xls")
    İsemri_Adedi_Ay, ServisGiris_Ay = Read_SSH_Iscilik_ParcaGelirleri_Excel(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuAyKumule_Rapor.xls", 'Marka Bazlı Fatura Detayları')
    isEmri_Ay, Garanti_Ay = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuAyKumule_Rapor.xls", 'Marka Bazlı Fatura Detayları')
    #os.remove(r"C:\Users\dogao\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls")


    #ParcaSatis_excel_downloader(Turkuaz_username, Turkuaz_password, last_day_worked, last_day_worked) # Downloads The excel starting date : lastwork_day, ending date: lastwork_day
    #RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\PRC-YSA-GBU-007+SSH+Parça+Satış.xls", "ParcaSatis_SonCalisilanGun_Raporu.xls")
    Banko_son_gun = Read_SSH_ParcaSatis_Excel(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_SonCalisilanGun_Raporu.xls", "BANKO")
    #os.remove(r"C:\Users\dogao\Downloads\PRC-YSA-GBU-007+SSH+Parça+Satış.xls")


    #ParcaSatis_excel_downloader(Turkuaz_username, Turkuaz_password, start_day_last_year, last_year_end_date) # Downloads The excel starting date : first day of this month last year, ending date: Chosen with func
    #RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\PRC-YSA-GBU-007+SSH+Parça+Satış.xls", "ParcaSatis_GecenSeneAylik_Rapor.xls")
    Banko_kumule_gecensene = Read_SSH_ParcaSatis_Excel(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_GecenSeneAylik_Rapor.xls", "BANKO")
    #os.remove(r"C:\Users\dogao\Downloads\PRC-YSA-GBU-007+SSH+Parça+Satış.xls")


    #ParcaSatis_excel_downloader(Turkuaz_username, Turkuaz_password, start_day_thismonth_thisyear, last_day_worked)
    #RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\PRC-YSA-GBU-007+SSH+Parça+Satış.xls", "ParcaSatis_BuAyKumule_Rapor.xls")
    Banko_kumule_busene = Read_SSH_ParcaSatis_Excel(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_BuAyKumule_Rapor.xls", "BANKO")
    #os.remove(r"C:\Users\dogao\Downloads\PRC-YSA-GBU-007+SSH+Parça+Satış.xls")


    Toplam_day = isEmri_Gun + Garanti_Gun + Banko_son_gun + ServisGiris
    Toplam_gecensene = isEmri_Gecensene + Garanti_Gecensene + Banko_kumule_gecensene + ServisGiris_Gecensene
    Toplam_kumule = isEmri_Ay + Garanti_Ay + Banko_kumule_busene + ServisGiris_Ay
    orijinal_parca_satisi_gun = isEmri_Gun + Garanti_Gun + Banko_son_gun
    orijinal_parca_satisi_kumule = isEmri_Ay + Garanti_Ay + Banko_kumule_busene

    is_emri_graph = int(round(ServisGiris_Ay / İs_Emri_Hedef, 2) * 100)
    parca_graph = int(round(orijinal_parca_satisi_kumule / Parca_Satis_Hedef, 2) * 100)

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    dateob = datetime.strptime(last_day_worked, "%d.%m.%Y")
    gun = dateob.strftime("%A")
    if gun == "Monday":
        gun = "Pzt"
    elif gun == "Tuesday":
        gun = "Sal"
    elif gun == "Wednesday":
        gun = "Çrş"
    elif gun == "Thursday":
        gun = "Prş"
    elif gun == "Friday":
        gun = "Cum"
    elif gun == "Saturday":
        gun = "Cmt"
    elif gun == "Sunday":
        gun = "Pzr"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "INSERT INTO sshparca_data (Tarih, Day, Month, Year, OrijinalParcaSatisAdet, gun) VALUES ('{}', {}, {}, {}, {}, '{}');"
    Month_tobe_inserted = today[3:5].lstrip("0")
    query = query.format(last_day_worked, last_day_worked[:2], Month_tobe_inserted, last_day_worked[-4:], round(orijinal_parca_satisi_gun/1000), gun, last_day_worked)

    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "INSERT INTO sshparca_data2 (Tarih, day, month, year, servisgirisi) VALUES ('{}', {}, {}, {}, {});"
    Month_tobe_inserted = today[3:5].lstrip("0")
    query = query.format(last_day_worked, last_day_worked[:2], Month_tobe_inserted, last_day_worked[-4:], ServisGiris)

    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()

    plot_circlu_(is_emri_graph, 100-is_emri_graph, 'Servis Girişi (kümüle)', 'Hedef Kalan', 'İş Emri', 'isemri_figure')
    plot_circlu_(parca_graph, 100-parca_graph, 'Parça Satışı (kümüle)', 'Hedef Kalan', 'Parça Satışı', 'parca_figure')
    plot_columnu_(isEmri_Gecensene, isEmri_Ay, Garanti_Gecensene, Garanti_Ay, Banko_kumule_gecensene, Banko_kumule_busene, Toplam_gecensene, Toplam_kumule, 'bargraph') ####################################################
    plot_line_('Parça Satışı (BİN ₺)', 'ParcaSatis_graph', first_day_check)
    plot_line_2('Servis Girişi', 'ServisGiris_graph', first_day_check)

    image_paths = []
    encoded_images = []

    isemri_figure = os.path.join(os.getcwd(), "isemri_figure.png")
    resize_image("isemri_figure.png", 300)
    parca_figure = os.path.join(os.getcwd(), "parca_figure.png")
    resize_image("parca_figure.png", 300)
    bargraph_figure = os.path.join(os.getcwd(), "bargraph.png")
    resize_image("bargraph.png", 375)
    parca_satis_line_figure = os.path.join(os.getcwd(), "ParcaSatis_graph.png")
    resize_image("ParcaSatis_graph.png", 957)
    servis_giris_line_figure = os.path.join(os.getcwd(), "ServisGiris_graph.png")
    resize_image("ServisGiris_graph.png", 957)


    image_paths.append(isemri_figure)
    image_paths.append(parca_figure)
    image_paths.append(bargraph_figure)
    image_paths.append(parca_satis_line_figure)
    image_paths.append(servis_giris_line_figure)

    for image_path in image_paths:
            with open(image_path, "rb") as f:
                image_data = f.read()
                encoded_images.append(base64.b64encode(image_data).decode("utf-8"))

    content = email_html.format(formatted_last_day_worked, get_day_of_week(last_day_worked), howmanydaysleft_, sene,
                                format_with_period(orijinal_parca_satisi_gun), format_with_period(orijinal_parca_satisi_kumule),
                                format_with_period(Parca_Satis_Hedef), format_with_period(ServisGiris), format_with_period(ServisGiris_Ay),
                                format_with_period(İs_Emri_Hedef), gecen_sene, format_with_period(isEmri_Gun), format_with_period(isEmri_Ay),
                                format_with_period(isEmri_Gecensene), format_with_period(Garanti_Gun), format_with_period(Garanti_Ay),
                                format_with_period(Garanti_Gecensene), format_with_period(Banko_son_gun), format_with_period(Banko_kumule_busene),
                                format_with_period(Banko_kumule_gecensene), format_with_period(ServisGiris), format_with_period(ServisGiris_Ay),
                                format_with_period(ServisGiris_Gecensene),format_with_period(Toplam_day), format_with_period(Toplam_kumule),
                                format_with_period(Toplam_gecensene), encoded_images[0], encoded_images[1], encoded_images[2], encoded_images[3],
                                encoded_images[4])

    send_email(content, 'Günlük Perakende Parça Satış Raporu', 'aslit@skoda.com.tr', cc_email='dogao@skoda.com.tr', sender_email='sshraporu@skoda.com.tr')
    send_email(content, 'Günlük Perakende Parça Satış Raporu', 'busray@skoda.com.tr', sender_email='sshraporu@skoda.com.tr')
    send_email(content, 'Günlük Perakende Parça Satış Raporu', 'afizeo@skoda.com.tr', sender_email='sshraporu@skoda.com.tr')
    send_email(content, 'Günlük Perakende Parça Satış Raporu', 'b.gerzeli@skoda.com.tr', sender_email='sshraporu@skoda.com.tr')
    #send_email(content, 'Günlük Perakende Parça Satış Raporu', 'dogao@skoda.com.tr', sender_email='sshraporu@skoda.com.tr')

    os.remove("isemri_figure.png")
    os.remove("parca_figure.png")
    os.remove("bargraph.png")
    os.remove("ParcaSatis_graph.png")
    os.remove("ServisGiris_graph.png")

