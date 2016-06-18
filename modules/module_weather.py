# encoding: utf-8
from bs4 import BeautifulSoup
import urllib
import re

SAA_BASE = "http://www.foreca.fi"
SAA_URL = "http://www.foreca.fi/search/"


def command_w(bot, update, args):
    if not args:
        args = ["tampere"]
    args = ' '.join(args)
    weather, meteogram = get_weather(args.encode('utf-8'))
    bot.sendMessage(chat_id=update.message.chat_id, text=weather)
    #bot.sendMessage(chat_id=update.message.chat_id, text=meteogram)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=meteogram)

def get_weather(url):
    url = url.replace("ä", "a").replace("Ä", "A").replace("ö", "o").replace("Ö", "o").replace("å", "a").replace("Å", "A")
    #full_url = saa_url + urllib.quote(url)
    full_url = SAA_URL + urllib.quote(url)
    output = None
    #url = getUrl(full_url)
    f = urllib.urlopen(full_url)
    bs = BeautifulSoup(f)
    if bs is None:
        output = "*Sori* ongelma interwebseissä"
        return output
    v_d = bs.find("div", "left").findAll("strong")
    meteogram = bs.find("img", src=re.compile("meteogram"))['src']
    city = bs.find("div", id="location_header").find("div", "to-left").find("h1").contents[0]
    celsius = v_d[0].contents[0]
    if len(v_d) > 2:
        wind_s = v_d[1].contents[0]
        koska = v_d[2].contents[0]
    else:
        wind_s = "Ei tietoa."
        koska = v_d[1].contents[0]
    #output = "!w- sää kaupungille ".encode('utf-8') + city + " mitattu " + koska + " - Lämpötila: ".encode('utf-8') + celsius + " C" + " Tuuli: " + wind_s
    output = "Sää kaupungille %s mitattu %s - Lämpötila: %s °C Tuuli: %s".decode('utf-8') % (city, koska, celsius, wind_s)
    o_d = bs.find("div", "right")
    for n in o_d.findAll(text=True):
        if len(n.strip()) is not 0:
            n = n.replace("&deg;", " °C".decode('utf-8'))
            output = output + " " + n.strip()
    return output, SAA_BASE + meteogram
