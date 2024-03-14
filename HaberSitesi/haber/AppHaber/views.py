from django.shortcuts import render, redirect
import requests
from .models import *
from pprint import pprint
import feedparser
import re
from datetime import datetime
from bs4 import BeautifulSoup
from django.utils.text import slugify
from email.utils import parsedate_to_datetime
from django.db.models import Q
from django.core.paginator import Paginator
import random
def Hava_durumu(request, sehir):
    hava_durumu_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={sehir}&lang=tr&appid=5828e876152d743e173d232647e516c1')

    hava_durumu = hava_durumu_response.json()
    sıcaklık = int(hava_durumu['main']['temp'] - 273.15)
    return hava_durumu, sıcaklık
    

def Kur(request):
    kur_response = requests.get("https://api.genelpara.com/embed/doviz.json")

    kur = kur_response.json()
    return kur


def index(request):
    categorys = Category.objects.all() # SELECT * FROM Category;
    haber_sites = HaberSites.objects.all()

    haberler = []
    # Haber
    ensonhaber_url = "https://www.ensonhaber.com/rss/ensonhaber.xml"

    ensonhaber = feedparser.parse(ensonhaber_url)

    for haber in ensonhaber.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "EN SON HABER"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        ensonhaber_summary_value = haber["summary_detail"]["value"]

        # img etiketini içeren düzenli ifade
        a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

        img_match = re.search(a_tag_pattern, ensonhaber_summary_value)

        if img_match:
            img_src = img_match.group(2)  # img etiketinin src özelliği
            haber_dict['img_url'] = img_src

        else:
            print("img etiketi bulunamadı.")

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(ensonhaber_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
          

        haberler.append(haber_dict)

    ntv_url = "https://www.ntv.com.tr/son-dakika.rss"

    ntv = feedparser.parse(ntv_url)

    for haber in ntv.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "NTV"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = datetime.strptime(haber.published, '%Y-%m-%dT%H:%M:%S%z')
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        ntv_summary_value = haber["summary"]

        # img etiketini içeren düzenli ifade
        a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

        matches = re.findall(a_tag_pattern, ntv_summary_value)
        for match in matches:
            haber_dict['img_url'] = match
            
        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(ntv_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
        

        haberler.append(haber_dict)


    sabah_url = "https://www.sabah.com.tr/rss/anasayfa.xml"

    sabah = feedparser.parse(sabah_url)

    for haber in sabah.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "SABAH"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        sabah_summary_value = haber["summary"]
        haber_dict['img_url'] = haber["media_content"][0]["url"]

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(sabah_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
        

        haberler.append(haber_dict)


    milliyet_url = "https://www.milliyet.com.tr/rss/rssNew/SonDakikaRss.xml"

    milliyet = feedparser.parse(milliyet_url)

    for haber in milliyet.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "MİLLİYET"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        milliyet_summary_value = haber["summary"]

        # img etiketini içeren düzenli ifade
        a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

        matches = re.findall(a_tag_pattern, milliyet_summary_value)
        for match in matches:
            haber_dict['img_url'] = match
            
        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(milliyet_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
        

        haberler.append(haber_dict)


    sozcu_url = "https://www.sozcu.com.tr/feeds-haberler"

    sozcu = feedparser.parse(sozcu_url)

    for haber in sozcu.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "SÖZCÜ"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        haber_dict['img_url'] = haber["media_content"][0]["url"]
        sozcu_summary_value = haber["summary_detail"]["value"]

        # img etiketini içeren düzenli ifade
        a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(sozcu_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
        

        haberler.append(haber_dict)


    mynet_url = "https://www.mynet.com/yerel-haberler/rss/kategori/ana"

    mynet = feedparser.parse(mynet_url)

    for haber in mynet.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "MYNET"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = parsedate_to_datetime(haber.published)
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        haber_dict['img_url'] = haber["img640x360"]
        mynet_summary_value = haber["summary_detail"]["value"]

        # img etiketini içeren düzenli ifade
        a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(mynet_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
        

        haberler.append(haber_dict)


    a_haber_url = "https://www.ahaber.com.tr/rss/anasayfa.xml"
    
    a_haber = feedparser.parse(a_haber_url)

    for haber in a_haber.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "A HABER"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = parsedate_to_datetime(haber.published)
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        haber_dict['img_url'] = "https://play-lh.googleusercontent.com/pT42M09UJOnDJ0zF7FjVQJBC7DZ1ovUDN8-lHBpGrbZGAohwmrIbpl67BX5nnEbw2Jw=w600-h300-pc0xffffff-pd"
        a_haber_summary_value = haber["summary_detail"]["value"]

        # img etiketini içeren düzenli ifade
        a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(a_haber_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
        

        haberler.append(haber_dict)
    
    haberturk_url = "https://www.haberturk.com/rss"

    haberturk = feedparser.parse(haberturk_url)

    for haber in haberturk.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "HABER TÜRK"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = parsedate_to_datetime(haber.published)
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        haber_dict['img_url'] = haber["media_content"][0]["url"]
        haberturk_summary_value = haber["summary"]

        # img etiketini içeren düzenli ifade

        a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(haberturk_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag

        haberler.append(haber_dict)

    trt_haber_url = "https://www.trthaber.com/manset_articles.rss"

    trt_haber = feedparser.parse(trt_haber_url)

    for haber in trt_haber.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "TRT HABER"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = parsedate_to_datetime(haber.published)
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        haber_dict['img_url'] = haber["media_content"][0]["url"]
        trt_haber_summary_value = haber["summary"]

        # img etiketini içeren düzenli ifade

        a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(trt_haber_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
        

        haberler.append(haber_dict)

    haber_global_url = "https://haberglobal.com.tr/rss"

    haber_global = feedparser.parse(haber_global_url)

    for haber in haber_global.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "HABER GLOBAL"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = parsedate_to_datetime(haber.published)
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        haber_dict['img_url'] = haber["media_content"][0]["url"]
        haber_global_summary_value = haber["summary"]

        # img etiketini içeren düzenli ifade

        a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(haber_global_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
        

        haberler.append(haber_dict)

    cnn_turk_url = "https://www.cnnturk.com/feed/rss/all/news"

    cnn_turk = feedparser.parse(cnn_turk_url)

    for haber in cnn_turk.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "CNN TÜRK"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = parsedate_to_datetime(haber.published)
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        haber_dict['img_url'] = "https://yt3.googleusercontent.com/ShuHogS_oo3tsc3tCTX38tSKoFHUzCYgnQ-Vrun8QiFgWAQoaBE5ZRld8vZkZU40gAVibg2WRw=s900-c-k-c0x00ffffff-no-rj"
        cnn_turk_summary_value = haber["summary"]

        # img etiketini içeren düzenli ifade

        a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(cnn_turk_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
            

        haberler.append(haber_dict)

    atv_url = "https://www.atv.com.tr/rss/haberler.xml"

    atv = feedparser.parse(atv_url)

    for haber in atv.entries:
        # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
        haber_dict = {}
        haber_dict["kaynak"] = "ATV"
        haber_dict['baslik'] = haber.title
        haber_dict['link'] = haber.link
        dt = parsedate_to_datetime(haber.published)
        haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
        haber_dict['img_url'] = haber["media_content"][0]["url"]
        atv_summary_value = haber["summary"]

        # img etiketini içeren düzenli ifade

        a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

        # <a> etiketi dışındaki metni içeren düzenli ifade
        soup = BeautifulSoup(atv_summary_value, 'html.parser')

        # Metindeki <a> etiketi dışındaki metni al
        text_outside_a_tag = soup.get_text()

        haber_dict['description'] = text_outside_a_tag
        

        haberler.append(haber_dict)
    
    random.shuffle(haberler)

    paginator = Paginator(haberler, 20)
    page_number = request.GET.get('page')
    haberler = paginator.get_page(page_number)

    sehir = "Karabük"
    if request.method == "POST":
        sehir = request.POST.get("sehir")
        print(sehir)
        request.session['sehir'] = sehir

    if sehir == "Karabük":
        sehir = "Karabük"
    else:
        sehir = request.session.get('sehir')

    context={
        "haberler":haberler,
        "categorys":categorys,
        "haber_sites":haber_sites,
        "kur":Kur(request),
        "hava_durumu":Hava_durumu(request,sehir)
    }

    return render(request, "index.html", context)


def category(request,haber_site):
    haber_sites = HaberSites.objects.all()
    if haber_site == "sozcu":
        new = HaberSites.objects.get(title__icontains=haber_site.replace("u","ü").replace("o","ö").replace("-"," ").capitalize())
    else:
        new = HaberSites.objects.get(title__icontains=haber_site.replace("u","ü").replace("-"," ").capitalize())


    if haber_site == "ensonhaber":

        ensonhaber_url = "https://www.ensonhaber.com/rss/ensonhaber.xml"

        ensonhaber = feedparser.parse(ensonhaber_url)

        haberler = []

        for haber in ensonhaber.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            ensonhaber_summary_value = haber["summary_detail"]["value"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

            img_match = re.search(a_tag_pattern, ensonhaber_summary_value)

            if img_match:
                img_src = img_match.group(2)  # img etiketinin src özelliği
                haber_dict['img_url'] = img_src

            else:
                print("img etiketi bulunamadı.")

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(ensonhaber_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "sabah":

        sabah_url = "https://www.sabah.com.tr/rss/anasayfa.xml"

        sabah = feedparser.parse(sabah_url)

        haberler = []

        for haber in sabah.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            sabah_summary_value = haber["summary"]
            haber_dict['img_url'] = haber["media_content"][0]["url"]

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(sabah_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "ntv":

        ntv_url = "https://www.ntv.com.tr/gundem.rss"

        ntv = feedparser.parse(ntv_url)

        haberler = []

        for haber in ntv.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%Y-%m-%dT%H:%M:%S%z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            ntv_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            matches = re.findall(a_tag_pattern, ntv_summary_value)
            for match in matches:
                print(match)
                haber_dict['img_url'] = match
                
            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(ntv_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)


    elif haber_site == "milliyet":

        milliyet_url = "https://www.milliyet.com.tr/rss/rssNew/SonDakikaRss.xml"

        milliyet = feedparser.parse(milliyet_url)

        print(milliyet["entries"][0])

        haberler = []

        for haber in milliyet.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            milliyet_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            matches = re.findall(a_tag_pattern, milliyet_summary_value)
            for match in matches:
                print(match)
                haber_dict['img_url'] = match
                
            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(milliyet_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "sozcu":

        sozcu_url = "https://www.sozcu.com.tr/feeds-haberler"

        sozcu = feedparser.parse(sozcu_url)

        pprint(sozcu["entries"][0])

        haberler = []

        for haber in sozcu.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            sozcu_summary_value = haber["summary_detail"]["value"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(sozcu_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "mynet":

        mynet_url = "https://www.mynet.com/yerel-haberler/rss/kategori/ana"

        mynet = feedparser.parse(mynet_url)

        pprint(mynet["entries"][0])

        haberler = []

        for haber in mynet.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["img640x360"]
            mynet_summary_value = haber["summary_detail"]["value"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(mynet_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "a-haber":

        a_haber_url = "https://www.ahaber.com.tr/rss/anasayfa.xml"

        a_haber = feedparser.parse(a_haber_url)

        pprint(a_haber["entries"][0])

        haberler = []

        for haber in a_haber.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = "https://play-lh.googleusercontent.com/pT42M09UJOnDJ0zF7FjVQJBC7DZ1ovUDN8-lHBpGrbZGAohwmrIbpl67BX5nnEbw2Jw=w600-h300-pc0xffffff-pd"
            a_haber_summary_value = haber["summary_detail"]["value"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(a_haber_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)
        
    elif haber_site == "haberturk":

        haberturk_url = "https://www.haberturk.com/rss"

        haberturk = feedparser.parse(haberturk_url)

        pprint(haberturk["entries"][0])

        haberler = []

        for haber in haberturk.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            haberturk_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade

            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(haberturk_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "trt-haber":

        trt_haber_url = "https://www.trthaber.com/manset_articles.rss"

        trt_haber = feedparser.parse(trt_haber_url)

        pprint(trt_haber["entries"][0])

        haberler = []

        for haber in trt_haber.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            trt_haber_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade

            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(trt_haber_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "haber-global":

        haber_global_url = "https://haberglobal.com.tr/rss"

        haber_global = feedparser.parse(haber_global_url)

        pprint(haber_global["entries"][0])

        haberler = []

        for haber in haber_global.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            haber_global_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade

            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(haber_global_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "cnn-turk":

        cnn_turk_url = "https://www.cnnturk.com/feed/rss/all/news"

        cnn_turk = feedparser.parse(cnn_turk_url)

        pprint(cnn_turk["entries"][0])

        haberler = []

        for haber in cnn_turk.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = "https://yt3.googleusercontent.com/ShuHogS_oo3tsc3tCTX38tSKoFHUzCYgnQ-Vrun8QiFgWAQoaBE5ZRld8vZkZU40gAVibg2WRw=s900-c-k-c0x00ffffff-no-rj"
            cnn_turk_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade

            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(cnn_turk_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "atv":

        atv_url = "https://www.atv.com.tr/rss/haberler.xml"

        atv = feedparser.parse(atv_url)

        pprint(atv["entries"][0])

        haberler = []

        for haber in atv.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            atv_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade

            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(atv_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)


    paginator = Paginator(haberler, 10)
    page_number = request.GET.get('page')
    haberler = paginator.get_page(page_number)


    sehir = "Karabük"
    if request.method == "POST":
        sehir = request.POST.get("sehir")

    context={
        "haberler":haberler,
        "haber_sites":haber_sites,
        "new":new,
        "kur":Kur(request),
        "hava_durumu":Hava_durumu(request, sehir)
    }
    return render(request, "category.html",context)

def subcategory(request, haber_site, category):
    haber_sites = HaberSites.objects.all()
    if haber_site == "sozcu":
        new = HaberSites.objects.get(title__icontains=haber_site.replace("u","ü").replace("o","ö").replace("-"," ").capitalize())
    else:
        new = HaberSites.objects.get(title__icontains=haber_site.replace("u","ü").replace("-"," ").capitalize())

    if haber_site == "ensonhaber":

        if category == "politika":

            ensonhaber_url = "https://www.ensonhaber.com/rss/ekonomi.xml"

        elif category == "ekonomi":

            ensonhaber_url = "https://www.ensonhaber.com/rss/ekonomi.xml"

        elif category == "dunya":

            ensonhaber_url = "https://www.ensonhaber.com/rss/dunya.xml"

        elif category == "saglik":

            ensonhaber_url = "https://www.ensonhaber.com/rss/saglik.xml"

        elif category == "otomobil":

            ensonhaber_url = "https://www.ensonhaber.com/rss/otomobil.xml"

        elif category == "kultur-sanat":

            ensonhaber_url = "https://www.ensonhaber.com/rss/kultur-sanat.xml"

        elif category == "teknoloji":

            ensonhaber_url = "https://www.ensonhaber.com/rss/teknoloji.xml"
            
        elif category == "medya":

            ensonhaber_url = "https://www.ensonhaber.com/rss/medya.xml"

        elif category == "yasam":

            ensonhaber_url = "https://www.ensonhaber.com/rss/yasam.xml"

        elif category == "spor":

            ensonhaber_url = "https://www.ensonhaber.com/rss/kralspor.xml"

        elif category == "3-sayfa":

            ensonhaber_url = "https://www.ensonhaber.com/rss/3-sayfa.xml"

        elif category == "magazin":

            ensonhaber_url = "https://www.ensonhaber.com/rss/magazin.xml"

        elif category == "kadin":

            ensonhaber_url = "https://www.ensonhaber.com/rss/kadin.xml"

        ensonhaber = feedparser.parse(ensonhaber_url)

        haberler = []

        for haber in ensonhaber.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            ensonhaber_summary_value = haber["summary_detail"]["value"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

            img_match = re.search(a_tag_pattern, ensonhaber_summary_value)

            if img_match:
                img_src = img_match.group(2)  # img etiketinin src özelliği
                haber_dict['img_url'] = img_src

            else:
                print("img etiketi bulunamadı.")

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(ensonhaber_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)
    
    elif haber_site == "sabah":

        if category == "roza":

            sabah_url = "https://www.sabah.com.tr/rss/roza.xml"

        elif category == "ekonomi":

            sabah_url = "https://www.sabah.com.tr/rss/ekonomi.xml"

        elif category == "dunya":

            sabah_url = "https://www.sabah.com.tr/rss/dunya.xml"

        elif category == "saglik":

            sabah_url = "https://www.sabah.com.tr/rss/saglik.xml"

        elif category == "otomobil":

            sabah_url = "https://www.sabah.com.tr/rss/otomobil.xml"

        elif category == "kultur-sanat":

            sabah_url = "https://www.sabah.com.tr/rss/kultur-sanat.xml"

        elif category == "teknoloji":

            sabah_url = "https://www.sabah.com.tr/rss/teknoloji.xml"

        elif category == "yasam":

            sabah_url = "https://www.sabah.com.tr/rss/yasam.xml"

        elif category == "spor":

            sabah_url = "https://www.sabah.com.tr/rss/spor.xml"

        sabah = feedparser.parse(sabah_url)

        haberler = []

        for haber in sabah.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            sabah_summary_value = haber["summary"]
            haber_dict['img_url'] = haber["media_content"][0]["url"]

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(sabah_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "ntv":

        if category == "turkiye":

            ntv_url = "https://www.ntv.com.tr/turkiye.rss"

        elif category == "ekonomi":

            ntv_url = "https://www.ntv.com.tr/ekonomi.rss"

        elif category == "dunya":

            ntv_url = "https://www.ntv.com.tr/dunya.rss"

        elif category == "saglik":

            ntv_url = "https://www.ntv.com.tr/saglik.rss"

        elif category == "otomobil":

            ntv_url = "https://www.ntv.com.tr/otomobil.rss"

        elif category == "kultur-sanat":

            ntv_url = "https://www.ntv.com.tr/sanat.rss"

        elif category == "teknoloji":

            ntv_url = "https://www.ntv.com.tr/teknoloji.rss"
            
        elif category == "egitim":

            ntv_url = "https://www.ntv.com.tr/egitim.rss"

        elif category == "yasam":

            ntv_url = "https://www.ntv.com.tr/yasam.rss"

        elif category == "spor":

            ntv_url = "https://www.ntv.com.tr/spor.rss"

        ntv = feedparser.parse(ntv_url)

        haberler = []

        for haber in ntv.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%Y-%m-%dT%H:%M:%S%z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            ntv_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            matches = re.findall(a_tag_pattern, ntv_summary_value)
            for match in matches:
                print(match)
                haber_dict['img_url'] = match
                
            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(ntv_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "milliyet":

        if category == "siyaset":

            milliyet_url = "https://www.milliyet.com.tr/rss/rssNew/siyasetRss.xml"

        elif category == "dunya":

            milliyet_url = "https://www.milliyet.com.tr/rss/rssNew/dunyaRss.xml"

        elif category == "otomobil":

            milliyet_url = "https://www.milliyet.com.tr/rss/rssNew/otomobilRss.xml"

        elif category == "magazin":

            milliyet_url = "https://www.milliyet.com.tr/rss/rssNew/magazinRss.xml"

        elif category == "teknoloji":

            milliyet_url = "https://www.milliyet.com.tr/rss/rssNew/teknolojiRss.xml"

        elif category == "yasam":

            milliyet_url = "https://www.milliyet.com.tr/rss/rssNew/yasamRss.xml"


        milliyet = feedparser.parse(milliyet_url)

        haberler = []

        for haber in milliyet.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            milliyet_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            matches = re.findall(a_tag_pattern, milliyet_summary_value)
            for match in matches:
                print(match)
                haber_dict['img_url'] = match
                
            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(milliyet_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "sozcu":

        if category == "gundem":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-gundem"

        elif category == "dunya":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-dunya"

        elif category == "ekonomi":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-ekonomi"

        elif category == "otomobil":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-otomotiv"

        elif category == "magazin":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-magazin"

        elif category == "teknoloji":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-bilim-teknoloji"

        elif category == "yasam":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-yasam"

        elif category == "spor":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-spor"

        elif category == "kultur-sanat":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-kultur-sanat"

        elif category == "saglik":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-saglik"

        elif category == "egitim":

            sozcu_url = "https://www.sozcu.com.tr/feeds-rss-category-egitim"


        sozcu = feedparser.parse(sozcu_url)

        haberler = []

        for haber in sozcu.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            sozcu_summary_value = haber["summary_detail"]["value"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(sozcu_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "mynet":
        
        if category == "politika":

            mynet_url = "https://www.mynet.com/haber/rss/kategori/politika/"

        elif category == "dunya":

            mynet_url = "https://www.mynet.com/haber/rss/kategori/dunya/"

        elif category == "ekonomi":

            mynet_url = "https://finans.mynet.com/haber/rss/gununozeti/"

        elif category == "magazin":

            mynet_url = "https://www.mynet.com/magazin/rss"

        elif category == "teknoloji":

            mynet_url = "https://www.mynet.com/haber/rss/kategori/teknoloji/"

        elif category == "yasam":

            mynet_url = "https://www.mynet.com/haber/rss/kategori/yasam/"

        elif category == "spor":

            mynet_url = "https://www.mynet.com/spor/rss"

        elif category == "saglik":

            mynet_url = "https://www.mynet.com/haber/rss/kategori/saglik/"

        mynet = feedparser.parse(mynet_url)

        pprint(mynet["entries"][0])

        haberler = []

        for haber in mynet.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            try:
                haber_dict['img_url'] = haber["img640x360"]
            except:
                haber_dict["img_url"] = "https://imgrosetta.mynet.com/file/1585522/640xauto.jpg"
            mynet_summary_value = haber["summary_detail"]["value"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(mynet_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "a-haber":

        if category == "gundem":

            a_haber_url = "https://www.ahaber.com.tr/rss/gundem.xml"

        elif category == "dunya":

            a_haber_url = "https://www.ahaber.com.tr/rss/dunya.xml"

        elif category == "ekonomi":

            a_haber_url = "https://www.ahaber.com.tr/rss/ekonomi.xml"

        elif category == "otomobil":

            a_haber_url = "https://www.ahaber.com.tr/rss/otomobil.xml"

        elif category == "magazin":

            a_haber_url = "https://www.ahaber.com.tr/rss/magazin.xml"

        elif category == "teknoloji":

            a_haber_url = "https://www.ahaber.com.tr/rss/teknoloji.xml"

        elif category == "yasam":

            a_haber_url = "https://www.ahaber.com.tr/rss/yasam.xml"

        elif category == "spor":

            a_haber_url = "https://www.ahaber.com.tr/rss/spor.xml"

        elif category == "kultur-sanat":

            a_haber_url = "https://www.ahaber.com.tr/rss/video/kultursanat.xml"

        elif category == "saglik":

            a_haber_url = "https://www.ahaber.com.tr/rss/saglik.xml"

        
        a_haber = feedparser.parse(a_haber_url)

        # pprint(a_haber["entries"][0])

        haberler = []

        for haber in a_haber.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            a_haber_summary_value = haber["summary_detail"]["value"]

            # img etiketini içeren düzenli ifade
            a_tag_pattern = r'<a\s+.*?href="(.*?)".*?>\s*<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(a_haber_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "haberturk":

        if category == "gundem":

            haberturk_url = "https://www.haberturk.com/rss/kategori/gundem.xml"

        elif category == "dunya":

            haberturk_url = "https://www.haberturk.com/rss/kategori/dunya.xml"

        elif category == "ekonomi":

            haberturk_url = "https://www.haberturk.com/rss/ekonomi.xml"

        elif category == "otomobil":

            haberturk_url = "https://www.haberturk.com/rss/kategori/otomobil.xml"

        elif category == "magazin":

            haberturk_url = "https://www.haberturk.com/rss/magazin.xml"

        elif category == "teknoloji":

            haberturk_url = "https://www.haberturk.com/rss/kategori/teknoloji.xml"

        elif category == "yasam":

            haberturk_url = "https://www.haberturk.com/rss/kategori/yasam.xml"

        elif category == "spor":

            haberturk_url = "https://www.haberturk.com/rss/spor.xml"

        elif category == "kultur-sanat":

            haberturk_url = "https://www.haberturk.com/rss/kategori/kultur-sanat.xml"

        elif category == "saglik":

            haberturk_url = "https://www.haberturk.com/rss/kategori/saglik.xml"

        elif category == "kadin":

            haberturk_url = "https://www.haberturk.com/rss/kategori/kadin.xml"

        elif category == "sinema":

            haberturk_url = "https://www.haberturk.com/rss/kategori/sinema.xml"
    


        haberturk = feedparser.parse(haberturk_url)

        pprint(haberturk["entries"][0])

        haberler = []

        for haber in haberturk.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            haberturk_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade

            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(haberturk_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "trt-haber":

        if category == "gundem":

            trt_haber_url = "https://www.trthaber.com/gundem_articles.rss"

        elif category == "dunya":

            trt_haber_url = "https://www.trthaber.com/dunya_articles.rss"

        elif category == "ekonomi":

            trt_haber_url = "https://www.trthaber.com/ekonomi_articles.rss"

        elif category == "egitim":

            trt_haber_url = "https://www.trthaber.com/egitim_articles.rss"

        elif category == "teknoloji":

            trt_haber_url = "https://www.trthaber.com/bilim_teknoloji_articles.rss"

        elif category == "yasam":

            trt_haber_url = "https://www.trthaber.com/yasam_articles.rss"

        elif category == "spor":

            trt_haber_url = "https://www.trthaber.com/spor_articles.rss"

        elif category == "kultur-sanat":

            trt_haber_url = "https://www.trthaber.com/kultur_sanat_articles.rss"

        elif category == "saglik":

            trt_haber_url = "https://www.trthaber.com/saglik_articles.rss"

        elif category == "turkiye":

            trt_haber_url = "https://www.trthaber.com/turkiye_articles.rss"

        
        trt_haber = feedparser.parse(trt_haber_url)

        pprint(trt_haber["entries"][0])

        haberler = []

        for haber in trt_haber.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            trt_haber_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade

            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(trt_haber_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "haber-global":

        if category == "gundem":

            haber_global_url = "https://haberglobal.com.tr/rss/gundem"

        elif category == "dunya":

            haber_global_url = "https://haberglobal.com.tr/rss/dunya"

        elif category == "ekonomi":

            haber_global_url = "https://haberglobal.com.tr/rss/ekonomi"

        elif category == "magazin":

            haber_global_url = "https://haberglobal.com.tr/rss/magazin"

        elif category == "teknoloji":

            haber_global_url = "https://haberglobal.com.tr/rss/bilim-teknoloji"

        elif category == "yasam":

            haber_global_url = "https://haberglobal.com.tr/rss/yasam"

        elif category == "spor":

            haber_global_url = "https://haberglobal.com.tr/rss/spor"

        elif category == "kultur-sanat":

            haber_global_url = "https://haberglobal.com.tr/rss/kultur-sanat"

        elif category == "saglik":

            haber_global_url = "https://haberglobal.com.tr/rss/saglik"

        elif category == "otomobil":

            haber_global_url = "https://haberglobal.com.tr/rss/otomobil"
        

        haber_global = feedparser.parse(haber_global_url)

        haberler = []

        for haber in haber_global.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = haber["media_content"][0]["url"]
            haber_global_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade

            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(haber_global_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    elif haber_site == "cnn-turk":

        if category == "turkiye":

            cnn_turk_url = "https://www.cnnturk.com/feed/rss/turkiye/news"

        elif category == "dunya":

            cnn_turk_url = "https://www.cnnturk.com/feed/rss/dunya/news"

        elif category == "ekonomi":

            cnn_turk_url = "https://www.cnnturk.com/feed/rss/ekonomi/news"

        elif category == "magazin":

            cnn_turk_url = "https://www.cnnturk.com/feed/rss/magazin/news"

        elif category == "yasam":

            cnn_turk_url = "https://www.cnnturk.com/feed/rss/yasam/news"

        elif category == "spor":

            cnn_turk_url = "https://www.cnnturk.com/feed/rss/spor/news"

        elif category == "kultur-sanat":

            cnn_turk_url = "https://www.cnnturk.com/feed/rss/kultur-sanat/news"

        elif category == "saglik":

            cnn_turk_url = "https://www.cnnturk.com/feed/rss/saglik/news"

        elif category == "otomobil":

            cnn_turk_url = "https://www.cnnturk.com/feed/rss/otomobil/news"



        cnn_turk = feedparser.parse(cnn_turk_url)

        haberler = []

        for haber in cnn_turk.entries:
            # Her bir haber için başlık ve img URL'si saklayacak bir sözlük oluştur
            haber_dict = {}

            haber_dict['baslik'] = haber.title
            haber_dict['link'] = haber.link
            dt = parsedate_to_datetime(haber.published)
            haber_dict['date'] = dt.strftime('%d-%m-%Y %H:%M:%S')
            haber_dict['img_url'] = "https://yt3.googleusercontent.com/ShuHogS_oo3tsc3tCTX38tSKoFHUzCYgnQ-Vrun8QiFgWAQoaBE5ZRld8vZkZU40gAVibg2WRw=s900-c-k-c0x00ffffff-no-rj"
            cnn_turk_summary_value = haber["summary"]

            # img etiketini içeren düzenli ifade

            a_tag_pattern = r'<img\s+.*?src="(.*?)".*?>'

            # <a> etiketi dışındaki metni içeren düzenli ifade
            soup = BeautifulSoup(cnn_turk_summary_value, 'html.parser')

            # Metindeki <a> etiketi dışındaki metni al
            text_outside_a_tag = soup.get_text()

            haber_dict['description'] = text_outside_a_tag
            

            haberler.append(haber_dict)

    paginator = Paginator(haberler, 10)
    page_number = request.GET.get('page')
    haberler = paginator.get_page(page_number)


    sehir = "Karabük"
    if request.method == "POST":
        sehir = request.POST.get("sehir")

    context={
        "new":new,
        "haberler":haberler,
        "category":category,
        "haber_sites":haber_sites,
        "kur":Kur(request),
        "hava_durumu":Hava_durumu(request, sehir)
    }

    return render(request, "subcategory.html", context)