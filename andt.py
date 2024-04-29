__author__ = 'wdolowicz'

from bs4 import BeautifulSoup
import re
import os
from os.path import abspath
from jinja2 import Template
from collections import Counter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def edit_andt(version, textfile):
    with open(textfile, 'r', encoding='utf-8') as infile, open('temp.txt', 'w', encoding='utf-8') as outfile:
        data = infile.read()
        data = data.replace("-", "<strong>•</strong>  ")
        outfile.write(data)
    changelog_text = open('temp.txt', "r", encoding='utf-8')
    changelog = changelog_text.readlines()
    changelist = changelog
    template = Template("""
                                                          <tr style="height: 7px;">
                                                            <td width="100" height="10" bgColor="#ffffff"></td>
                                                            <td style="width: 440px;
                                                              background: white;
                                                              padding: 0cm; height:
                                                              7px;">
                    {% for item, count in bye.items() %}
                                                        <font
                                                                size="+3"><span
                                                                  style="font-size:
                                                                  12.0pt;
                                                                  font-family:
                                                                  'Arial',sans-serif;
                                                                  color: #666666;">{{item}}</span></font><br><br>
                    {% endfor %}
                                                        </td>
                                                        <td width="100" height="10" bgColor="#ffffff"></td>
                                                      </tr>
            """)
    log = template.render(bye=Counter(changelist))
    file = abspath('andt_data/letter.html')
    html = open(file, 'r', encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    target = soup.find_all(text=re.compile(r'version_placeholder'))
    changes = soup.find_all(text=re.compile(r'changelog_placeholder'))
    for v in target:
        v.replace_with(v.replace('version_placeholder', version))
    for c in changes:
        c.replace_with(c.replace('changelog_placeholder', log))

    html = soup.prettify("utf-8", formatter=None)
    with open("andt_data/letter_mod.html", "wb") as file:
        file.write(html)
    changelog_text.close()


def send_andt(version, me, password, you):
    # Utworzenie zawartości wiadomości
    msg = MIMEMultipart('related')
    msg['Subject'] = str("Wydanie Google for Tablet " + version)
    msg['From'] = me
    msg['To'] = you

    # Import ciała wiadomości z HTML
    file = abspath('andt_data/letter_mod.html')
    HtmlFile = open(file, 'r', encoding="utf-8")
    html = HtmlFile.read()
    HtmlFile.close()

    # Określenie typu zawartości
    part1 = MIMEText(html, 'html')

    # Załączenie zawartości html
    msg.attach(part1)

    # Przypisanie ID do obrazów

    # logo Fibaro
    fp = open('andt_data/image001.jpg', 'rb')
    msgImage = MIMEImage(fp.read(), _subtype="jpg")
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)
    # obraz tytułowy z urządzeniami
    fp = open('andt_data/image002.jpg', 'rb')
    msgImage2 = MIMEImage(fp.read(), _subtype="jpg")
    fp.close()
    msgImage2.add_header('Content-ID', '<image2>')
    msg.attach(msgImage2)
    # logo apple
    fp = open('andt_data/image003.jpg', 'rb')
    msgImage3 = MIMEImage(fp.read(), _subtype="jpg")
    fp.close()
    msgImage3.add_header('Content-ID', '<image3>')
    msg.attach(msgImage3)
    # przycisk pobierania
    fp = open('andt_data/image004.jpg', 'rb')
    msgImage4 = MIMEImage(fp.read(), _subtype="jpg")
    fp.close()
    msgImage4.add_header('Content-ID', '<image4>')
    msg.attach(msgImage4)

    # Wysyłanie wiadmości przez serwer yourmail
    s = smtplib.SMTP('smtp.yourmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(me, password)

    s.sendmail(me, you.split(','), msg.as_string())
    s.quit()
    os.remove("andt_data/letter_mod.html")
    os.remove("temp.txt")
