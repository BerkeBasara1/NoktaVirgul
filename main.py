from excelreader import ExcelRead, ExcelRead2, ExcelRead3, format_with_period
from TurkuazDataScraper import TurkuazDataReader
from percantage_calc import perc_calculator
from email_reader import email_reader
from email_html import email_html
from send_email import send_email
from datetime import datetime
from config import Skoda_Satis_Stok_Raporu
import time
import pymysql
import os

def SabahRaporuComplete(turkuazusername, turkuazpassword, ithalat, fatura, Euro_kur):
    email_reader()
    Diger_Satislar_value_ay, Diger_Satislar_value_yil, Bugun_Perakende, Bugun_Olasilik, Islem_Alti = TurkuazDataReader(turkuazusername, turkuazpassword)
    Perakende_Ay, Toptan_Ay , Perakende_Yil, Toptan_Yil, Aylik_YS_Satis_F, YSval_YSF, Aylik_DS_Satis_F, Toptan_Aylik_eksi = ExcelRead(Skoda_Satis_Stok_Raporu, "Satış Stok Durumu", Diger_Satislar_value_ay)
    Fatura_Baglanti = format_with_period(str(YSval_YSF + Bugun_Perakende + Bugun_Olasilik + Islem_Alti))
    YSval_YSF = format_with_period(YSval_YSF)
    FABIA_T, OCTAVIA_T, KAROQ_T, KODIAQ_T, SUPERB_T, SCALA_T, KAMIQ_T, FABIA_M, OCTAVIA_M, KAROQ_M, KODIAQ_M, SUPERB_M, SCALA_M, KAMIQ_M,\
    T_toplam, M_toplam, perc_Fabia, perc_Octavia, perc_Karoq, perc_Kodiaq, perc_Superb, perc_Scala, perc_Kamiq, perc_Toplam = ExcelRead3(Skoda_Satis_Stok_Raporu, "Satış Stok Durumu")
    
    today = datetime.today().strftime("%d-%m-%Y").replace("-",".")

    table = ExcelRead2(Skoda_Satis_Stok_Raporu, "Satış Stok Durumu")
    try:
        Stok_T = table['Stok_T']
        table['Stok_T'] = format_with_period(str(table['Stok_T']))
    except:
        table['Stok_T'] = 0
        Stok_T = 0
    try:
        Stok_M = table['Stok_M']
        table['Stok_M'] = format_with_period(str(table['Stok_M']))
    except:
        table['Stok_M'] = 0
        Stok_M = 0
    try:
        Fiktif_T = table['Fiktif_T']
        table['Fiktif_T'] = format_with_period(str(table['Fiktif_T']))
    except:
        table['Fiktif_T'] = 0
        Fiktif_T = 0
    try:
        Fiktif_M = table['Fiktif_M']
        table['Fiktif_M'] = format_with_period(str(table['Fiktif_M']))
    except:
        table['Fiktif_M'] = 0
        Fiktif_M = 0
    try:
        YSStok_T = table['YSStok_T']
        table['YSStok_T'] = format_with_period(str(table['YSStok_T']))
    except:
        table['YSStok_T'] = 0
        YSStok_T = 0
    try:
        YSStok_M = table['YSStok_M']
        table['YSStok_M'] = format_with_period(str(table['YSStok_M']))
    except:
        table['YSStok_M'] = 0
        YSStok_M = 0
    try:
        Yolda_T = table['Yolda_T']
        table['Yolda_T'] = format_with_period(str(table['Yolda_T']))
    except:
        table['Yolda_T'] = 0
        Yolda_T = 0
    try:
        Yolda_M = table['Yolda_M']
        table['Yolda_M'] = format_with_period(str(table['Yolda_M']))
    except:
        table['Yolda_M'] = 0
        Yolda_M = 0
    try:
        a = table['IntTransfer_T']
    except:
        table['IntTransfer_T'] = 0
    try:
        b = table['IntTransfer_M']
    except:
        table['IntTransfer_M'] = 0
    try:
        c = table['Transport_T']
    except:
        table['Transport_T'] = 0
    try:
        d = table['Transport_M']
    except:
        table['Transport_M'] = 0

    Int_plus_Transport_T = table['IntTransfer_T'] + table['Transport_T']
    Int_plus_Transport_M = table['IntTransfer_M'] + table['Transport_M']
    Int_plus_Transport_TT = table['IntTransfer_T'] + table['Transport_T']
    Int_plus_Transport_MM = table['IntTransfer_M'] + table['Transport_M']
    Int_plus_Transport_T = format_with_period(Int_plus_Transport_T)
    Int_plus_Transport_M = format_with_period(Int_plus_Transport_M)

    try:
        Produced_T = table['Produced_T']
        table['Produced_T'] = format_with_period(str(table['Produced_T']))
    except:
        table['Produced_T'] = 0
        Produced_T = 0
    try:
        Produced_M = table['Produced_M']
        table['Produced_M'] = format_with_period(str(table['Produced_M']))
    except:
        table['Produced_M'] = 0
        Produced_M = 0
    try:
        if table['Liman_T'] != 'empty':
            Liman_T = table['Liman_T']
            table['Liman_T'] = format_with_period(str(table['Liman_T']))
        else:
            table['Liman_T'] = 0
            Liman_T = 0
    except:
        table['Liman_T'] = 0
        Liman_T = 0
    try:
        if table['Liman_M'] != 'empty':
            Liman_M = table['Liman_M']
            table['Liman_M'] = format_with_period(str(table['Liman_M']))
        else:
            table['Liman_M'] = 0
            Liman_M = 0
    except:
        table['Liman_M'] = 0
        Liman_M = 0
    try:
        if YSStok_T == "empty":
            YSStok_T = 0
        if Fiktif_T == "empty":
            Fiktif_T = 0
        if Liman_T == "empty":
            Liman_T = 0
        if Yolda_T == "empty":
            Yolda_T = 0
        if Int_plus_Transport_TT == "empty":
            Int_plus_Transport_TT = 0
        if Stok_T == "empty":
            Stok_T = 0
        TOPLAM_T = YSStok_T + Fiktif_T + Liman_T + Yolda_T + Int_plus_Transport_TT + Stok_T
        table['TOPLAM_T'] = format_with_period(str(TOPLAM_T))
    except:
        table['TOPLAM_T'] = 0
        TOPLAM_T = 0
    try:
        if Fiktif_M == "empty":
            Fiktif_M = 0
        if YSStok_M == "empty":
            YSStok_M = 0
        if Liman_M == "empty":
            Liman_M = 0
        if Int_plus_Transport_MM == "empty":
            Int_plus_Transport_MM = 0
        if Yolda_M == "empty":
            Yolda_M = 0
        if Stok_M == "empty":
            Stok_M = 0
        TOPLAM_M = YSStok_M + Fiktif_M + Liman_M + Yolda_M + Int_plus_Transport_MM + Stok_M
        table['TOPLAM_M'] = format_with_period(str(TOPLAM_M))
    except:
        table['TOPLAM_M'] = 0
        TOPLAM_M = 0
    
    def converto(obje):
        try:
            obje = int(obje)
        except:
            obje = 0
        return obje
    perc_stok = perc_calculator(converto(Stok_T), converto(Stok_M))
    perc_fiktif = perc_calculator(converto(Fiktif_T), converto(Fiktif_M))
    perc_YSstok = perc_calculator(converto(YSStok_T), converto(YSStok_M))
    perc_Yolda = perc_calculator(converto(Yolda_T), converto(Yolda_M))
    perc_IntTrans = perc_calculator(converto(Int_plus_Transport_TT), converto(Int_plus_Transport_MM))
    perc_produced = perc_calculator(converto(Produced_T), converto(Produced_M))
    perc_liman = perc_calculator(converto(Liman_T), converto(Liman_M))
    perc_toplam = perc_calculator(converto(TOPLAM_T), converto(TOPLAM_M))

    ithalat = ithalat
    Toptan_Fatura = fatura

    if Euro_kur == None:
        Euro_kur = ""
    else:
        Euro_kur = '<p style="color:#349051"><b>İthalat Kuru: {}</b></p><br>'.format(Euro_kur)

    mail_index = email_html.format(today, str(Perakende_Ay), str(Perakende_Yil), str(Toptan_Ay), str(Toptan_Yil), Perakende_Ay, Aylik_YS_Satis_F,
        YSval_YSF, Toptan_Ay, format_with_period(Aylik_DS_Satis_F), format_with_period(Toptan_Aylik_eksi), Fatura_Baglanti, ithalat, Toptan_Fatura, Euro_kur,
        table['YSStok_T'], table['YSStok_M'], perc_YSstok, table['Stok_T'], table['Stok_M'], perc_stok, table['Fiktif_T'], table['Fiktif_M'],
        perc_fiktif, table['Yolda_T'], table['Yolda_M'], perc_Yolda, table['Liman_T'], table['Liman_M'], perc_liman, Int_plus_Transport_T,
        Int_plus_Transport_M, perc_IntTrans, table['TOPLAM_T'], table['TOPLAM_M'], perc_toplam, format_with_period(FABIA_T), format_with_period(FABIA_M),  "%" + perc_Fabia, format_with_period(OCTAVIA_T),
        format_with_period(OCTAVIA_M), "%" + perc_Octavia, format_with_period(KAROQ_T), format_with_period(KAROQ_M), "%" + perc_Karoq, format_with_period(KODIAQ_T), format_with_period(KODIAQ_M), "%" + perc_Kodiaq, format_with_period(SUPERB_T), format_with_period(SUPERB_M),
        "%" + perc_Superb, format_with_period(SCALA_T), format_with_period(SCALA_M), "%" + perc_Scala, format_with_period(KAMIQ_T), format_with_period(KAMIQ_M), "%" + perc_Kamiq, format_with_period(T_toplam), format_with_period(M_toplam), "%" + perc_Toplam).replace("em.pty", "0")

    os.remove(Skoda_Satis_Stok_Raporu)

    mail_header = "{} Sabah raporu".format(today)
    send_email(mail_index, mail_header, "aslis@skoda.com.tr", cc_email="dogao@skoda.com.tr")
    send_email(mail_index, mail_header, "afizeo@skoda.com.tr")
    send_email(mail_index, mail_header, "busray@skoda.com.tr")
    send_email(mail_index, mail_header, "stj_b.basara@skoda.com.tr")
    #send_email(mail_index, mail_header, "dogao@skoda.com.tr")
    

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "INSERT INTO sabahraporu (ithalat, fatura, tarih) VALUES (%s, %s, %s)"
    values = (ithalat, fatura, today)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
