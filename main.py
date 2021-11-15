import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()


sad_words = ["sad", "depressed", "unhappy", "angry", "kms", "die", "miserable", "depressing", "kill", "fuck", "shit", "pain", "damn"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there :O",
  "You are a great person / bot!",
  "shut the fuck up"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  # quote = json_data[0]['q'] + " -" + json_data[0]['a']
  quote = json_data[0]['q'] + " -some fucker that thought about shit"
  return(quote)

def update_encouragements(m):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(m)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [m]
    
# def delete_encouragements(index):
#   encouragements = db["encouragements"]
#   if len(encouragements) > index:
#     del encouragements[index]
#   db["encouragements"] = encouragements

def delete_encouragements(phrase):
  encouragements = db["encouragements"]
  encouragements.remove(phrase)
  db["encouragements"] = encouragements

@client.event 
async def on_ready(): #called when bot is ready to be used
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content.lower()


  if msg.startswith("$hello"): #returns with hello
    await message.channel.send("am i ok")

  if msg.startswith("$inspire"): #returns an inspiring quote
    await message.channel.send(get_quote())
  

  if db["responding"]: #condition of responding, then inspirational quote on sad message
    options = starter_encouragements

    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])


    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))


  if msg.startswith("$new"): #adds to database of inspiring 
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"): #deletes from inspiring 
    if "encouragements" in db.keys():
      phrase = msg.split("$del ",1)[1]
      delete_encouragements(phrase)
    
    await message.channel.send(list(db["encouragements"]))
  
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = list(db["encouragements"])
    await message.channel.send("Current list: " + encouragements)

  if msg.startswith("$responding"): #sets if responding
    if msg == "$responding" or msg == "$responding ":
      await message.channel.send("incomplete syntax...beep boop bitch")
      return
    value = msg.split("responding ",1)[1]
    
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Will respond to cries for help...")
      return
    elif value.lower() == "false":
      db["responding"] = False
      await message.channel.send("damn you. now the screams of the damned go unanswered")
      return
    
    await message.channel.send("Type in a valid value dipshit I don't take 'option 3'")
    

keep_alive()
client.run(os.getenv('TOKEN'))