email_html = """<html>
  <head></head>
  <body>
    <p>Değerli Yöneticilerim ve Çalışma Arkadaşlarım,
    <br>
    <br>
    <p>Günlük Perakende Parça Satış Raporunu bilgilerinize sunarım.</p>
    <p>İyi Çalışmalar</p>
    <p><b>{} {}</b></p>
    <p><b>Kalan İş Günü Sayısı:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}</b></p>
    <div class="container" style="width:100%;">
          <hr style="border-style: solid; width:90%;">
            <table>
                <tr>
                    <th colspan="1" style="background-color:#F1F2F2; width:320px">Günlük Perakende Parça Satış Raporu<br>{}</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">Gün</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">Kümüle</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">Hedef</th>
                </tr>
                <tr>
                    <td style="text-align:center;"><b>Orijinal Parça Satışı</b></td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center;"><b>Servis Girişi</b></td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                </tr>
            </table>
            <br>
            <br>
            <table>
                <tr>
                    <th colspan="1" style="background-color:#F1F2F2; width:320px">Orijinal Parça Satış Raporu Kırılımı</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">Gün</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">Kümüle</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">{} Gerçekleşen</th>
                </tr>
                <tr>
                    <td style="text-align:center;">İş Emri</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center;">Garanti</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center;">Banko</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center;">Servis Girişi</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                    <td style="text-align:center;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center; background-color:#78FAAE"><b>Toplam</b></td>
                    <td style="text-align:center; background-color:#78FAAE"><b>{}</b></td>
                    <td style="text-align:center; background-color:#78FAAE"><b>{}</b></td>
                    <td style="text-align:center; background-color:#78FAAE"><b>{}</b></td>
                </tr>
            </table>
            <br>
            <img src="data:image/png;base64,{}" style="width:200px !important; height: auto;">
            <img src="data:image/png;base64,{}" style="width:200px !important; height: auto;">
            <img src="data:image/png;base64,{}" style="width:200px !important; height: auto;">
            <br>
            <img src="data:image/png;base64,{}">
            <br>
            <img src="data:image/png;base64,{}">
    </div>
    <div class="container" style="width:100%; display:flex;">
        <br>
        <p>Kurumsal bilgiler içermektedir. Sadece ilgili ekipler ve 3. taraflar ile kontrollü olarak paylaşılmalıdır. \\ Contains corporate information. It should only be shared in a controlled manner with the relevant teams and third parties.</p>
    </div>
  </body>
</html>"""
