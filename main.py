import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
import time
import asyncio
import datetime
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


my_secret = os.environ['TOKEN']
dota2_api_key = os.environ['dota2_api_key']

client = discord.Client()

sad_words=["sad","depressing", "depressed", "unhappy", "miserable"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
  "Remember, benn still OT atm."
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)

def get_hist(userid):
  response = requests.get("https://api.opendota.com/api/players/" + userid + "/matches")
  json_data = json.loads(response.text)
  print (json_data)
  return (json_data)


def check(userid1, userid2):
  response1 = requests.get("https://api.opendota.com/api/players/" + userid1 + "/matches?included_account_id=" + userid2 + "&limit=10")
  json_data1 = json.loads(response1.text)
  if len(json_data1) > 0:
    message =json_data1
  else:
    message = "No match found."
  return message


def checkwl(userid1, day):
  response1 = requests.get("https://api.opendota.com/api/players/" + userid1 + "/wl?date=" + day)
  json_data1 = json.loads(response1.text)
  return json_data1


def transformMatchResult(json_match):
  length = len(json_match)
  embed=discord.Embed(title="Last " + str(length) + " match stat", color=0x00ff2a)
  embed.set_author(name="霹雳烽火狼")
  for dic in json_match:
    slot = dic['player_slot']
    hero = get_heroes(dic['hero_id'])
    if slot <= 127:
      team = 'Radiant'
    else:
      team = 'Dire'
    if team == 'Radiant' and dic['radiant_win'] is True:
      result = 'Win'
    elif team == 'Dire' and dic['radiant_win'] is False:
      result = 'Win'
    else:
       result = 'Lose'
    embed.add_field(name='Match ID : ' + str(dic['match_id']) + '\nTeam : ' + team + '\nHero : ' + hero + '\nResult : ' + result , value=" Match details : "+ "https://www.dotabuff.com/matches/" + str(dic['match_id']), inline=False)
  embed.set_footer(text="有了兄弟，绝对无敌")
  return embed


  def transformMatchResult(json_match):
    length = len(json_match)
    embed=discord.Embed(title="Last " + str(length) + " match stat", color=0x00ff2a)
    embed.set_author(name="霹雳烽火狼")
    for dic in json_match:
      slot = dic['player_slot']
      hero = get_heroes(dic['hero_id'])
      if slot <= 127:
        team = 'Radiant'
      else:
        team = 'Dire'
      if team == 'Radiant' and dic['radiant_win'] is True:
        result = 'Win'
      elif team == 'Dire' and dic['radiant_win'] is False:
        result = 'Win'
      else:
        result = 'Lose'
      embed.add_field(name='Match ID : ' + str(dic['match_id']) + '\nTeam : ' + team + '\nHero : ' + hero + '\nResult : ' + result , value=" Match details : "+ "https://www.dotabuff.com/matches/" + str(dic['match_id']), inline=False)
    embed.set_footer(text="有了兄弟，绝对无敌")
    return embed


def reg_uid(uid, authorid):
  if authorid in db.keys():
    db[authorid] = uid
    s = "User ID registered."
  else:
    db[authorid] = [uid]
    s = "User ID updated."
  return s


def check_uid(authorid):
  if authorid in db.keys():
    username1 = db[authorid]
    result = "\n".join(username1)
    s = result
  else:
    s = 1
  return s


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
      db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_heroes(s):
  f = open('heroes.json', )
  data = json.load(f)
  for i in data['heroes']:
    if i.get('id') == s:
      return (i['localized_name'])

async def user_metrics_background_task():
    await client.wait_until_ready()
    ctoday = datetime.datetime.today()
    cdmy = ctoday.strftime("%d%m%Y")
    print(db["dateCovid"])
    print(cdmy)
    if db["dateCovid"] != cdmy:
      session = requests.Session()
      retry = Retry(connect=3, backoff_factor=0.5)
      adapter = HTTPAdapter(max_retries=retry)
      session.mount('http://', adapter)
      session.mount('https://', adapter)
      g_channel = await client.fetch_channel(868907046370676757)

      while not client.is_closed():
          today = datetime.datetime.today()
          dmy = today.strftime("%d%m%Y")
          # url = "https://covid-19.moh.gov.my/terkini-negeri/" + str(today.year) + "/kemaskini-negeri-covid-19-di-malaysia-sehingga-" + str(
          #     dmy)
          url = "https://covid-19.moh.gov.my/terkini-negeri/" + str(today.year) + "/" + today.strftime("%m") + "/kemaskini-negeri-covid-19-di-malaysia-" + str(
              dmy)
          print(url)
          try:
              page = session.get(url)
          except Exception as e:
              print(e)
              pass
          else:
              soup = BeautifulSoup(page.content, "html.parser")
              x = soup.find("div", class_="e-content")
              if x:
                  z = str(x.p.find("img"))
                  split = z[18:-6]
                  img = "https://covid-19.moh.gov.my/" + split
                  x = datetime.datetime(today.year, today.month, today.day, 23, 59)
                  diff = x - today
                  sleeptimer = 21660 + int(diff.total_seconds())
                  embed = discord.Embed(title="Malaysia Covid Status on " + dmy, url=url, color=0x00ff2a)
                  embed.set_author(name="霹雳烽火狼")
                  embed.set_image(url=img)
                  print(img)
                  print(sleeptimer)
                  embed.set_footer(text="有了兄弟，绝对无敌")
                  db["dateCovid"] = dmy
                  await g_channel.send(embed=embed)
                  await asyncio.sleep(sleeptimer)
              else:
                  print("Error 404")
                  await asyncio.sleep(600)     
    
    else:
      y = datetime.datetime(ctoday.year, ctoday.month, ctoday.day, 23, 59)
      cdiff = y - ctoday
      csleeptimer = 21660 + int(cdiff.total_seconds())
      print(csleeptimer)
      await asyncio.sleep(csleeptimer)

async def play():
    vcguild = client.get_guild(515911308969902090)
    voiceChannel = discord.utils.get(vcguild.voice_channels, id=839420813714128947)
    print(voiceChannel)
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=vcguild)
    voice.play(discord.FFmpegPCMAudio("asd.mp3"))
    await asyncio.sleep(13)
    await voice.disconnect()

async def playrace():
    vcguild = client.get_guild(515911308969902090)
    voiceChannel = discord.utils.get(vcguild.voice_channels, id=839420813714128947)
    print(voiceChannel)
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=vcguild)
    voice.play(discord.FFmpegPCMAudio("racestart.mp3"))
    await asyncio.sleep(13)
    await voice.disconnect()

async def playtr():
    vcguild = client.get_guild(515911308969902090)
    voiceChannel = discord.utils.get(vcguild.voice_channels, id=839420813714128947)
    print(voiceChannel)
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=vcguild)
    voice.play(discord.FFmpegPCMAudio("teamrocket.mp3"))
    await asyncio.sleep(26)
    await voice.disconnect()

async def join():
    vcguild = client.get_guild(515911308969902090)
    voiceChannel = discord.utils.get(vcguild.voice_channels, id=839420813714128947)
    print(voiceChannel)
    await voiceChannel.connect()

async def leave():
    vcguild = client.get_guild(515911308969902090)
    voice = discord.utils.get(client.voice_clients, guild=vcguild)
    await voice.disconnect()

@client.event
async def on_ready():
  # global g_guild
  # global g_user
  # g_guild = client.get_guild(515911308969902090)
  # # g_user = client.get_user(int(331410456604311552))
  # g_user = await client.fetch_user(240535818488250378)
  print('We have loggedin as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  channel = message.channel.id

  if channel != 859346771544899584 and channel != 841295650040971264:
    return

  msg = message.content
  user = message.author

  if message.content.startswith('$history'):
    userid = msg.split("$history ",1) [1]
    quote = get_hist(userid)
    await message.channel.send(quote)

  if message.content.startswith('$rstdate'):
    db["dateCovid"] = "26072021"
    await message.channel.send("resetted")

  if message.content.startswith('$zy'):
    await message.channel.send("https://www.youtube.com/watch?v=SPuoPwyHQLg&t=2s&ab_channel=HOOK")

  if message.content.startswith('$inform'):
    today = datetime.datetime.today()
    x = datetime.datetime(today.year, today.month, today.day, 23, 59)
    diff = x - today
    sleeptimer = int(diff.total_seconds()) - 28800 + 60
    print(sleeptimer)
    await asyncio.sleep(sleeptimer)
    await message.channel.send('@everyone Happy 虎 year! `\n` 給你虎虎的祝福，虎虎的甜蜜，虎虎的運氣，虎虎的健康，虎虎的快樂，虎虎的心情，虎虎的欣慰，虎虎的順利，虎虎的幸福，虎虎的人生！:tiger: :tiger: :tiger:')

  if message.content.startswith('$play'):
    await play()

  if message.content.startswith('$rstt'):
    await playrace()

  if message.content.startswith('$tr'):
    await playtr()

  if message.content.startswith('$join'):
    await join()

  if message.content.startswith('$leave'):
    await leave()

  if message.content.startswith('$reg '):
    uid = msg.split(" ")[1]
    if represents_int(uid) == True:
      response = reg_uid(uid, user)
      await message.channel.send(response)
    else:
      await message.channel.send("Player ID must be interger.")

  if message.content.startswith('$checkmewith '):
    searchid = msg.split(" ")[1]
    if represents_int(searchid) == True:
      username = str(user)
      result = check_uid(username)
      if result == 1:
        await user.send("Please register your d2 id by command \" ?reg [d2id] \"")
      else:
        uid = str(result)
        json_match = check(uid, searchid)
        if json_match == 'No match found.':
          await message.channel.send(json_match)
        else:
          embed = transformMatchResult(json_match)
          await message.channel.send(embed=embed)
    else:
      await message.channel.send("Both player ID must be interger.")

  if message.content.startswith('$wl '):
    searchid = msg.split(" ")[1]
    day = msg.split(" ")[2]
    if not day:
      day = 0
    if represents_int(searchid) == True and represents_int(day) and int(day) <= 10:
      result = checkwl(searchid, day)
      res = json.dumps(result)
      await message.channel.send(username + " "+ res)
    elif int(day) > 10:
      await message.channel.send("Number of day can't be greater than 10")
    else:
      await message.channel.send("Both dota2id and day(optional) must be interger.")

  if message.content.startswith('$mywl'):
    if len(msg.split(" ")) == 1:
      day = "0"
    else:
      day = str(msg.split(" ")[1])
    username = str(user)
    searchid = check_uid(username)
    if represents_int(searchid) == True and int(day) <= 10:
      if searchid == 1:
        await user.send("Please register your d2 id by command \" ?reg [d2id] \"")
      else:
        result = checkwl(searchid, day)
        res = json.dumps(result)
      await message.channel.send(username + " "+ res)
    elif int(day) > 10:
      await message.channel.send("Number of day can't be greater than 10")
    else:
      await message.channel.send("Both dota2id and day(optional) must be interger.")

  if message.content.startswith('$check '):
    if len( msg.split(" ")) == 3:
      userid1 = msg.split(" ")[1]
      userid2 = msg.split(" ")[2]
      if represents_int(userid1) == True and represents_int(userid2) == True:
        res = check(userid1, userid2)
        if res == 'No match found.':
          await message.channel.send(res)
        else:
          embed = transformMatchResult(res)
          await message.channel.send(embed=embed)
      else:
        await message.channel.send("Both player ID must be interger.")
    else:
      await message.channel.send("Please ensure that you are inputting correct format.")

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await user.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])
    
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1) [1]
    update_encouragements(encouraging_message)
    await message.channel.send('New encouraging_message added.')

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      listofstring = "\n".join(encouragements)
    await message.channel.send(listofstring)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")

    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

  if message.content.startswith('有了兄弟'):
    await message.channel.send('绝对无敌!!!')

  if message.content.startswith('$chant'):
    await message.channel.send('球场上谁给我们支援??\n兄弟！！\n球场上谁给我们勇气??\n兄弟！！\n球场上谁给我们信心??\n兄弟！！！')

client.loop.create_task(user_metrics_background_task())
keep_alive()
client.run(my_secret)