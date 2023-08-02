import matplotlib.pyplot as plt
from datetime import datetime
import calendar
import pymysql


# Gelen Müşteri ve Gelen Telefon Grafiğini oluşturup kaydeder
def plot_visitor_phonecall_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)

    result = cursor.execute(query)

    datas = cursor.fetchall()

    Gelen_Telefon_list = []
    Gelen_Musteri_list = []
    week_list = []
    i = 1
    for data in datas:
        week_list.append(int(data[2]))
        """
        #print('Tarih : ' + data[1])
        #print('Day : ' + data[2])
        if int(data[2]) == i:
            week_list.append(i)
            i += 1
        elif int(data[2]) != i:
            i = i + 2
            week_list.append(i)
            i += 1
        """
        

        #print('Month : ' + data[3])
        #print('Year : ' + data[4])
        Gelen_Telefon_list.append(int(data[5]))
        Gelen_Musteri_list.append(int(data[6]))
        #print('Baglanti : ' + data[7])
        #print('P Satis : ' + data[8])
        #print('Euro : ' + data[9])

    conn.commit()
    cursor.close()
    conn.close()
    x = week_list
    
    y1 = Gelen_Telefon_list
    y2 = Gelen_Musteri_list
    max_y1 = max(y1)
    max_y2 = max(y2)
    if max_y1 > max_y2:
        max_val = max_y1
    else:
        max_val = max_y2

    # Create a figure and axis object
    fig, ax = plt.subplots()
    # Plot the data as two line graphs
    
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='Gelen Telefon', marker='o', markerfacecolor='#0E3A2F')
    ax.plot(x, y2, color='#FAEB67', linewidth=3, label='Gelen Müşteri', marker='o', markerfacecolor='#F7B046')


    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('Adet')
    ax.set_title('Gelen Müşteri - Gelen Telefon', fontweight='bold')

    ax.legend() # Add legend

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 25, f"{y1[i]}", fontsize=9, weight='bold')
        plt.text(x[i], y2[i]+ 25, f"{y2[i]}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=90)

    x = 0
    while x <= max_val + 100 :
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 100
    fig.set_size_inches(12, 5)
    fig.savefig('Gelen_Musteri_Telefon_Graph.png')
    #plt.show()

#Bağlantı Grafiğini oluşturup kaydeder
def plot_Baglanti_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)

    result = cursor.execute(query)

    datas = cursor.fetchall()

    Baglanti_list = []
    week_list = []
    i = 1
    for data in datas:
        week_list.append(int(data[2]))
        """
        if int(data[2]) == i:
            week_list.append(i)
            i += 1
        elif int(data[2]) != i:
            i = i + 2
            week_list.append(i)
            i += 1
        """
        
        #print('Month : ' + data[3])
        #print('Year : ' + data[4])
        Baglanti_list.append(int(data[7]))
        #print('P Satis : ' + data[8])
        #print('Euro : ' + data[9])

    conn.commit()
    cursor.close()
    conn.close()

    x = week_list
    y1 = Baglanti_list
    max_val = max(y1)

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data as two line graphs
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='Bağlantı', marker='o', markerfacecolor='#0E3A2F')

    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('Adet')
    ax.set_title('Bağlantı', fontweight='bold')
    ax.legend() # Add legend

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 2, f"{y1[i]}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)

    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=90)

    x = 0
    while x < max_val + 10:
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 10

    fig.set_size_inches(12, 5)
    fig.savefig('Baglanti_Graph.png')
    #plt.show()

#Perakende Satış Grafiğini oluşturup kaydeder
def plot_Perakende_Satis_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)

    result = cursor.execute(query)

    datas = cursor.fetchall()

    PerakendeSatis_list = []
    week_list = []
    i = 1
    for data in datas:
        #print('Tarih : ' + data[1])
        #print('Day : ' + data[2])
        week_list.append(int(data[2]))
        """
        if int(data[2]) == i:
            week_list.append(i)
            i += 1
        elif int(data[2]) != i:
            i = i + 2
            week_list.append(i)
            i += 1
        """
        
        PerakendeSatis_list.append(int(data[8]))

    conn.commit()
    cursor.close()
    conn.close()

    x = week_list
    y1 = PerakendeSatis_list
    max_value = max(y1)

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data as two line graphs
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='Perakende Satış', marker='o', markerfacecolor='#0E3A2F')

    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('Adet')
    ax.set_title('Perakende Satış', fontweight='bold')
    ax.legend()  # Add legend

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 2, f"{y1[i]}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)

    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=90)

    x = 0
    while x <= max_value + 20:
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 20

    fig.set_size_inches(12, 5)
    fig.savefig('Perakende_Satis_Graph.png')
    #plt.show()

#Euro/TL Kur Grafiğini oluşturup kaydeder
def plot_Kur_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)

    result = cursor.execute(query)

    datas = cursor.fetchall()

    EuroKur_list = []
    week_list = []
    i = 1
    for data in datas:
        week_list.append(int(data[2]))
        """
        if int(data[2]) == i:
            week_list.append(i)
            i += 1
        elif int(data[2]) != i:
            i = i + 2
            week_list.append(i)
            i += 1
        """

        EuroKur_list.append(float(data[9]))

    conn.commit()
    cursor.close()
    conn.close()

    x = week_list
    y1 = EuroKur_list
    max_val = max(y1)
    min_val = min(y1)

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data as two line graphs
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='€/₺', marker='o', markerfacecolor='#0E3A2F')

    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('TL')
    ax.set_title('Kur €/₺', fontweight='bold')
    ax.legend()  # Add legend

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 0.02, f"{y1[i]}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)

    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=90)

    x = round(min_val)
    while x < max_val + 0.2:
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 0.2

    fig.set_size_inches(12, 5)
    fig.savefig('Kur_Graph.png')
    #plt.show()
