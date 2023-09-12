from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
import pypyodbc
import os

# Excel Tablo Değerleri
sheet_list = ['Geçici Araç Durum Özeti', 'Geçici Araç Tahsis Takip 2023', 'Lena BODRUM Geçici Araç', 'Geçici Araç Tahsis Takip']
table_list = ['GeciciAracDurumOzeti', 'GeciciAracTahsisi2023', 'LenaBodrumGeciciArac', 'GeciciAracTahsisTakip']

YuceDB_alchemy_key = f"mssql+pyodbc://usryuceauto:Reader142536@YUCESQL2\SQL201701/Raporlar?driver=ODBC+Driver+17+for+SQL+Server"

def excel_to_sql_MusteriDeneyimi(Arac_Tahsis_Excel_Path):
    for i in range(len(sheet_list)):
        excel = pd.read_excel(Arac_Tahsis_Excel_Path, sheet_name=sheet_list[i])

        # Düzeltilmiş sütun adlarını oluştur
        cleaned_columns = [col.replace("\n", "_") for col in excel.columns]
        excel.columns = cleaned_columns

        # Connects to the Database given
        db_engine = create_engine(YuceDB_alchemy_key)

        # Boş olmayan sütunları filtrele
        non_empty_columns = [col for col in excel.columns if not excel[col].isnull().all()]
        excel_filtered = excel[non_empty_columns]

        # "Kritik" sütununu kaldır, eğer varsa
        if "Kritik" in excel_filtered.columns:
            excel_filtered = excel_filtered.drop(columns=["Kritik"])

        # İlk sütunu filtrelenmiş DataFrame'den hariç tut
        excel_filtered = excel_filtered.iloc[:, 1:]

        # Tüm değerleri boş olan satırları kaldır
        excel_filtered = excel_filtered.dropna(how='all')

        # Mevcut tarih ve saati içeren bir zaman damgası sütunu ekle
        excel_filtered['Timestamp'] = datetime.now()

        # Veritabanına DataFrame'i yaz
        excel_filtered.to_sql(table_list[i], db_engine, if_exists='replace', index=False)