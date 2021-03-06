import discord
import asyncio
import requests
import json
import random
import codecs

films = open('kino.json', 'r', encoding='utf-8')

parsed_films = json.loads(films.read())

DISCORD_BOT_TOKEN = 'Insert your key here'

client = discord.Client()

words = {
    "title": ["название","title"],
    "originalTitle": ["оригинальное название","original title"],
    "year": ["год","year"],
    "rating": ["рейтинг","rating"],
    "tags": ["тэг","tag"],
    "genres": ["жанр","genre"],
    "countries": ["страна","страны","country","countries"],
}

@client.event
async def on_message(message):
        if message.content.startswith('!film'):
            message2 = message.content.lower()
            message2 = message2.split()
            randomindex = random.randint(0,len(parsed_films))
            film = parsed_films[randomindex]
            parse = {}
            for k,v in words.items():
                for param in v:
                    param = param.lower()
                    if message.content.find(param) != -1:
                        for mes in message2:
                            if mes.find(param) != -1:
                                parse[k] = message2[message2.index(mes)+1]
            goodfilmes = []
            if len(parse) > 0:
                for maybethis in parsed_films:
                    parseCount = 0
                    for k,v in parse.items():
                        if type(maybethis[k]) is not list:
                            mystring = str(maybethis[k]).lower()
                            if mystring == v.lower():
                                parseCount = parseCount + 1
                                if parseCount == len(parse):
                                    goodfilmes.append(maybethis)
                        else:
                            for value in maybethis[k]:
                                mystring = str(value).lower()
                                if mystring == v.lower():
                                    parseCount = parseCount + 1
                                    if parseCount == len(parse):
                                        goodfilmes.append(maybethis)
                if len(goodfilmes) > 0:
                    randomindex = random.randint(1,len(goodfilmes))-1
                    film = goodfilmes[randomindex]
                else:
                    await client.send_message(message.channel, 'С такими параметрами фильма не найдено.')
                    return
            em=discord.Embed(title=film['title'], description=film['description'], color=0x5bf970)
            em.set_image(url="http:"+film['poster'])
            em.add_field(name="Оригинальное название", value=film['originalTitle'], inline=True)
            em.add_field(name="Год и страна", value=film['production'], inline=True)
            em.add_field(name="Длительность", value=str(round(film['duration']/60)) + " мин.", inline=True)
            em.add_field(name="Рейтинг", value=film['rating'], inline=True)
            tags = ""
            if len(film['tags']) > 0:
                i = 0
                for tag in film['tags']:
                    if len(film['tags']) > 1 and i != len(film['tags'])-1:
                        tag = tag + ","
                    tags = tags + " " + tag
                    i = i + 1
                em.add_field(name="Тэги", value=tags, inline=True)
            genres = ""
            if len(film['genres']) > 0:
                i = 0
                for gen in film['genres']:
                    if len(film['genres']) > 1 and i != len(film['genres'])-1:
                        gen = gen + ","
                    genres = genres + " " + gen
                    i = i + 1
                em.add_field(name="Жанры", value=genres, inline=True)
            countries = ""
            if len(film['countries']) > 0:
                i = 0
                for country in film['countries']:
                    if len(film['countries']) > 1 and i != len(film['countries'])-1:
                        country = country + ","
                    countries = countries + " " + country
                    i = i + 1
                em.add_field(name="Страны", value=countries, inline=True)
            await client.send_message(message.channel, embed=em)

client.run(DISCORD_BOT_TOKEN)
