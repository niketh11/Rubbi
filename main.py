import nextcord
from nextcord.ext import commands
import os
import motor.motor_asyncio
import random
import PIL
from PIL import Image,ImageDraw,ImageFont,ImageChops
from io import BytesIO
import requests
from nextcord import ButtonStyle, Interaction
from nextcord.ui import button, View, Button
from nextcord.abc import GuildChannel
from flask import Flask
import asyncio
from webserver import keep_alive
import time
import datetime
global startTime
startTime = time.time()







client = commands.Bot(command_prefix=['<@971724343677689906> ','r',"rubbi","@RUBBI "], intents = nextcord.Intents.all())


client.remove_command('help')

cluster = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO"])
rubbi = cluster["main"]
db = rubbi["eco"]
print("database connected")
@client.event
async def on_ready():
    channel = client.get_channel(1039387444119867523)
    print(f'{client.user} is ONLINE!')
    await channel.send('online')
    await client.change_presence(status=nextcord.Status.dnd,activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"rubbi"))
 

 
@client.event
async def on_command(ctx):
  member = ctx.message.author
  bal = await db.find_one({"id": member.id})
  if bal is None:
    await db.insert_one({"id": member.id, "wallet": 100, "bank": 0})
    ri = await client.get_channel(1039387444119867523)
    await ri.send(f"created new user {member.name} ")
  else:
    print(" command used")



    






  
      
@client.command()
async def bal(ctx, *, member: nextcord.Member = None):
    if member==None:
      member = ctx.message.author
      data = await db.find_one({"id": member.id})
      wal = data["wallet"]
      ban = data["bank"]
      embed = nextcord.Embed(title = f"{member.name} bal")
      embed.add_field(name="<a:RGB:1026016813890420746>|Wallet",value = f"{wal}")
      embed.add_field(name = "<a:RGB:1026016813890420746>|Bank",value = f"{ban}")
      embed.set_thumbnail(url = ctx.author.display_avatar)
      await ctx.send(embed = embed)


 


@client.command()
@commands.cooldown(1, 86400, type = commands.BucketType.user)
async def daily(ctx):
  member = ctx.message.author
  data = await db.find_one({"id": member.id})
  wal = data["wallet"]
  await db.update_many({"id": member.id},{"$inc":{"wallet": +500}})
  embed = nextcord.Embed(title = "<:spookybox:1008693634054488094>|daily",description = "you have received 500 coins as daily reward")
  embed.set_thumbnail(url = ctx.author.display_avatar)

  await ctx.send(embed = embed)



@client.command()
async def withdraw(ctx, *, amount: int):
  member = ctx.message.author
  hi = await db.find_one({"id": member.id})
  if amount > hi['bank']:
    await ctx.send("you can't with draw that much money check your balance ")
  else:
    await db.update_many({"id": member.id},{"$inc": {"bank": -amount, "wallet": +amount}})
    embed = nextcord.Embed(title = " Withdraw",description = f"successfully withdrawn {amount}")
    embed.set_thumbnail(url = ctx.author.display_avatar)
    await ctx.send(embed = embed)

@client.command()
async def deposit(ctx, *, amount: int):
  member = ctx.message.author
  hi = await db.find_one({"id": member.id})
  if amount > hi['wallet']:
    await ctx.send("you can't deposit more money than your wallet")
  else:
    await db.update_many({"id": member.id},{"$inc": {"bank": +amount, "wallet": -amount}})
    embed = nextcord.Embed(title = "Deposit",description = f"successfully deposit {amount}")
    embed.set_thumbnail(url = ctx.author.display_avatar)
    await ctx.send(embed = embed)





@client.command()
@commands.cooldown(1, 3600, type = commands.BucketType.user)
async def work(ctx):
  credits = random.randint(500, 600)
  work = ["fisher","coder","begger"]
  await db.update_one({"id": ctx.author.id},{"$inc": {"wallet": +credits}})
  embed = nextcord.Embed(title = "work",description = f"you have earned {credits} by working {random.choice(work)}")
  embed.set_thumbnail(url = "https://media.discordapp.net/attachments/1039387444119867523/1039513254839472148/pending-1668514445-images.jpg")
  await ctx.send(embed = embed)









@client.command()
async def give(ctx, member:nextcord.Member, amount:int):
  um = ctx.message.author
  await db.update_one({"id": um.id},{"$inc": {"wallet": -amount}})
  await db.update_one({"id": member.id},{"$inc": {"wallet": +amount}})
  embed = nextcord.Embed(title = "transfer",description = f"you have successful fully sent {amount} to {member.name}")
  embed.set_thumbnail(url = ctx.author.display_avatar)
  await ctx.send(embed = embed)










@client.command()
@commands.cooldown(1, 20, type = commands.BucketType.user)
async def coinflip(ctx, *, amount:int):
  um = ctx.message.author
  hm = await db.find_one({"id": um.id})
  if amount > hm['wallet']:
    await ctx.send(" you can't man check you balance")
  else:
    msg = await ctx.send("flipping a coin <a:Coinflip3:1040634512591294535>")
    hi = [
      "Heads",
      "Tails",


    ]
    a = random.choice(hi) 
    if a=="Heads":
      await db.update_many({"id": um.id},{"$inc": {"wallet": +amount}})
  
      await msg.edit(" you won 2x of your money")
    else:
      await db.update_many({"id": um.id},{"$inc": {"wallet": -amount}})
      await msg.edit("you lost your money")
     


    








@client.command() 
async def profile(ctx, *, member: nextcord.Member):
  hm = await db.find_one({"id": member.id})
  wallet = hm['wallet']
  bank = hm['bank']
  name = member.name
  wal = f"Wallet: {wallet}"
  ban = f"bank: {bank}"
  
  
  profile = Image.open('profile.png')
  asset = member.display_avatar.with_size(256)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)
  pfp = pfp.resize((255, 255))
  
  
  draw = ImageDraw.Draw(profile)
  draw.text((850,550),"ye",fill = (0,0,0), stroke_width=2, stroke_fill=(255,255,255))
  draw.text((400, 800)," teste")
 
  profile.paste(pfp, (98, 200))
  profile.save('profilew.png')
  await ctx.send(file=nextcord.File("profilew.png"))




@client.command()
async def rob(ctx, *,member: nextcord.Member):
  hi = await db.find_one({"id": member.id})
  await ctx.send("soon w") 


@client.command()
@commands.cooldown(1, 80, type = commands.BucketType.user)
async def beg(ctx):
  um = ctx.message.author
  b = random.randint(1,500)
  await db.update_many({"id": um.id},{"$inc": {"wallet": +b}})
  await ctx. send(f"you have received {b}")










@client.command() 
@commands.cooldown(1, 80, type = commands.BucketType.user)
async def hunt(ctx):
  um = ctx.message.author
  an = ["🦒","🦬","🐄","🦌","🐘","🦕","🪲🐜🦗"]
  b = random.randint(1,500)
  names = ["raju","ramesh","krishna","grandpa max","rakesh"]
  await db.update_many({"id": um.id},{"$inc": {"wallet": +b}})
  msg = await ctx.send("hunting...")
  await asyncio.sleep(1)
  await msg.edit(embed = nextcord.Embed(title = "hunt",description = f" hey u have hunted {random.choice(an)} and sold it to {random.choice(names)} at {b}")) 
  



@client.command() 
@commands.cooldown(1, 80, type = commands.BucketType.user)
async def fish(ctx):
  um = ctx.message.author
  an = [':fish:',':tropical_fish:',':blowfish:',':octopus:',':squid:',':dolphin:',':shark:',':shrimp:',':crab:', ':lobster:']
  b = random.randint(1,500)
  names = ["raju","ramesh","krishna","grandpa max","rakesh",'Jenny','Lauren','Humble','Dan','Matthew','Blacksmith','Clarke','Simon','Christian','Hector','Albert','Vader','Walker','Phillip']
  await db.update_many({"id": um.id},{"$inc": {"wallet": +b}})
  msg = await ctx.send("🎣fishing")
  await asyncio.sleep(3)
  await msg.edit(embed = nextcord.Embed(title = "hunt",description = f" hey u have Caught {random.choice(an)} and sold it to {random.choice(names)} at {b}")) 
  

  


































 




@client.command()    
async def help(ctx):                
    class Select(nextcord.ui.Select):
        def __init__(self):
            options=[
                nextcord.SelectOption(label="INFO", value="option1",emoji = "<a:blob:1005672414480445450>"),
                nextcord.SelectOption(label="COMMANDS",value="option2",emoji = "<:rubbi3:1024138777154818071>"),
                ]
            super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
        async def callback(self, interaction: nextcord.Interaction):
            if self.values[0] == "option1":
                embed1 = nextcord.Embed(title = "<a:blob:1005672414480445450>|Info",description = """<:rubbi3:1024138777154818071> Rubbi Is Economy Bot With Advance Futures

<:Prolist:1040903135176175626> **__ProList.ml__** :- Coming Soon
<:topGG:1040907570543595540> **__Top.gg__** :- Coming Soon
<:Discord_Bot_List:1040907680417579060> **__Discord Bot List__** :- Coming Soon""")
                embed1.set_thumbnail(url = client.user.display_avatar)
                await interaction.response.send_message(embed = embed1)
            elif self.values[0] == "option2":
                embed2 = nextcord.Embed(title = "<:rubbi3:1024138777154818071>|Commands",description = """bal      
beg      
coinflip 
daily    
deposit  
give      
help 
hunt 
fish
withdraw 
work""")
                embed2.set_thumbnail(url = client.user.display_avatar)
                await interaction.response.send_message(embed = embed2)
                
    class SelectView(nextcord.ui.View):
        def __init__(self, *, timeout = 180):
            super().__init__(timeout=timeout)
            self.add_item(Select())
          
    embed = nextcord.Embed(title = "Rubbi",description = """ <:rubbi3:1024138777154818071> Rubbi Is Economy Bot With Advance Futures

<:Prolist:1040903135176175626> **__ProList.ml__** :- Coming Soon
<:topGG:1040907570543595540> **__Top.gg__** :- Coming Soon
<:Discord_Bot_List:1040907680417579060> **__Discord Bot List__** :- Coming Soon""")
    embed.set_thumbnail(url = client.user.display_avatar)
    await ctx.send(embed = embed, view=SelectView())                            



@client.command()
async def stats(ctx):
  uptimes = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
  s = client.guilds
  servers = len(s) 
  user = client.users
  users = len(user)
  embed = nextcord.Embed(title = "stats",description = " stats of rubbi")
  embed.add_field(name = "servers",value = f" {servers}")
  embed.add_field(name="users",value = f"{users}")
  embed.add_field(name = "uptime",value = f" {uptimes}") 
  await ctx.send(embed = embed)











@client.event
async def on_command_error(ctx, err):
  await ctx.send(f"{err}")
  
keep_alive()
client.run(os.environ['token'])