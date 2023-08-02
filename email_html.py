email_html = """<html>
  <head></head>
  <body>
    <p>Değerli Yöneticilerim ve Çalışma Arkadaşlarım,
    <br>
    <br>
    <b>{}</b> tarihli sabah raporunu bilgilerinize sunarım.
    <br>
    <table>
      <tr>
        <td colspan="1"></td>
        <th colspan="2" style="border: 1px solid black; background-color:#F1F2F2">Satış Adetleri</th>
      </tr>
      <tr>
        <th></th>
        <th style="border: 1px solid black;">AY</th>
        <th style="border: 1px solid black;">YIL</th>
      </tr>
      <tr>
        <td style="border: 1px solid black;"><b>PERAKENDE</b></td>
        <td style="border: 1px solid black; text-align:center;">&nbsp;{}&nbsp;</td>
        <td style="border: 1px solid black; text-align:center;">&nbsp;{}&nbsp;</td>
      </tr>
      <tr>
        <td style="border: 1px solid black;"><b>TOPTAN</b></td>
        <td style="border: 1px solid black; text-align:center;">&nbsp;{}&nbsp;</td>
        <td style="border: 1px solid black; text-align:center;">&nbsp;{}&nbsp;</td>
      </tr>
    </table>
    <p style="color:red"><b>FİLO/PERAKENDE DETAYLI ADETLER AŞAĞIDAKİ GİBİDİR:</b><p>
    <b>Aylık Perakende: {} ({}F + {}P)</b>
    <br>
    <b>Aylık Toptan: {} ({}F + {}P)</b>
    <br>
    <p style="color:red"><b>Fatura + Bağlantı: {} (filo hariç)</b></p>
    <br>
    İthalat: {}
    <br>
    Toptan Fatura: {}
    <br>
    {}
    <br>
    <table>
        <tr>
            <td style="border: 1px solid black; text-align:center; height:90px; width:90px; background-color:#F1F2F2"><b>STATÜ</b></td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2"><b>&nbsp;ADET&nbsp;</b></td>
            <td style="border: 1px solid black; text-align:center; width:60px; background-color:#F1F2F2"; text-align:center><b>MÜŞTERİ İSİMLİ ARAÇ SAYISI</b></td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2"><b>MÜŞTERİ ORANI</b></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">YS STOK</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">DS STOK</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">FİKTİF</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">YOLDA</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">LİMAN</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">INT + TRANS</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F1F2F2">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE"><b>TOPLAM</b></td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE"><b>{}</b></td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE"><b>{}</b></td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE"><b>{}</b></td>
        </tr>
    </table>
    <br>
    <table>
        <tr>
            <td colspan="4" style="border: 1px solid black;"><b>YS STOK ÜST MODEL BAZLI MÜŞTERİLİ ARAÇ ORANI</b></td>
        </tr>
        <tr style="background:#6CBDF6">
            <td style="border: 1px solid black; height:70px; background-color:#F1F2F2"><b>&nbsp;&nbsp;&nbsp;ÜST MODEL&nbsp;&nbsp;&nbsp;</b></td>
            <td style="border: 1px solid black; background-color:#F1F2F2"><b>&nbsp;&nbsp;&nbsp;ADET&nbsp;&nbsp;&nbsp;</b></td>
            <td style="border: 1px solid black; width:60px; background-color:#F1F2F2"><b>&nbsp;&nbsp;MÜŞTERİ İSİMLİ ARAÇ SAYISI&nbsp;&nbsp;</b></td>
            <td style="border: 1px solid black; background-color:#F1F2F2"><b>&nbsp;&nbsp;MÜŞTERİ ORANI&nbsp;&nbsp;</b></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; background-color:#78FAAE">FABIA</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black;  background-color:#F1F2F2">OCTAVIA</td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; background-color:#78FAAE">KAROQ</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; background-color:#F1F2F2">KODIAQ</td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; background-color:#78FAAE">SUPERB</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; background-color:#F1F2F2">SCALA</td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; background-color:#78FAAE">KAMIQ</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
            <td style="text-align:center; border: 1px solid black; background-color:#78FAAE">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; background-color:#F1F2F2"><b>TOPLAM</b></td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2"><b>{}</b></td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2"><b>{}</b></td>
            <td style="text-align:center; border: 1px solid black; background-color:#F1F2F2"><b>{}</b></td>
        </tr>
    </table>
    <br>
    <h4><b>Saygılarımla,</b></h4>
    <p>Kurumsal bilgiler içermektedir. Sadece ilgili ekipler ve 3. taraflar ile kontrollü olarak paylaşılmalıdır. \\ Contains corporate information. It should only be shared in a controlled manner with the relevant teams and third parties.</p>
  </body>
</html>"""