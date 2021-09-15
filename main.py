import discord
from keep_alive import keep_alive
import praw
import random
import os
from discord.ext import commands
from discord.ext.commands import Bot
from time import sleep

os.system("pip install topggpy")

import topgg

print("Importing finished")

reddit = praw.Reddit(
    client_id=str(os.environ['redditid']),
    client_secret=str(os.environ['redditsecret']),
    password=str(os.environ['reddit']),
    user_agent="Discord bot called \"CopyPasta\". This bot gets a random copypasta from r/copypasta and sends it to the server in which it was requested. For more info, visit https://github.com/kevlu8/copypasta.",
    username="DiscordCopypastaBot",
    check_for_async = False
)

print("Reddit done")

try:
  print("Logged in as " + str(reddit.user.me()) + " on Reddit")
except:
  print("Forbidden. Try switching the user agent.")

intents = discord.Intents.default()
intents.members = True

bot = Bot(':', intents = intents)
bot.remove_command('help')
bot.nsfwenabled = False
bot.amountToGet = 100
bot.string = "placeholder. if you're seeing this something seriously went wrong"

@bot.event
async def on_message(message):
    message.content = message.content.lower()
    pingMaybe = message.content.replace(" ", "")
    if pingMaybe == '<@882832904605020190>' or pingMaybe == "@CopyPasta#7051":
      channel = message.channel 
      await channel.send('fuck you, stop pinging me or i will start fucking swearing, if you want to know my prefix its : are you happy now')
    await bot.process_commands(message)

kevlu8 = None

@bot.event
async def on_ready():
  await bot.wait_until_ready()

  print('We have logged in as {0.user}'.format(bot))

  activity = discord.Game(name=":help - over " + str(len(bot.guilds)) + " servers!", type=3)
  await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("Command not found, skipping..")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing parameters! Run :help to see correct parameters. <:kek:789556121954025492> <:emoji_37:787733584542171196>')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to run this command. <:thonk:725866060166856764> <a:Supper:803963737622839316>")
    else:
      error = str(error)
      guild = bot.get_guild(855275010556821524)
      kevlu8 = guild.get_member(458684594703695872)
      if kevlu8 == None:
        kevlu8 = guild.get_member_named("kevlu8#5240")
      try: 
        await kevlu8.send(error + " when command " + str(ctx.message.content) + " was run.")
      except:
        splitatchar = 2000
        one, two = error[:splitatchar], error[splitatchar:]
        try:
          await ctx.send(one)
          await ctx.send(two)
        except:
            mid1, mid2 = two[:splitatchar], two[splitatchar:]
            try:
              await ctx.send(mid1)
              await ctx.send(mid2)
            except:
              await kevlu8.send("Bro there's an error go check console")
              print(error) # I can't use raise() or else the program stops

dbl_token = os.environ['dbl_token']

keep_alive()

bot.topggpy = topgg.DBLClient(bot, dbl_token, autopost=True, post_shard_count=True)

@bot.event
async def on_autopost_success():
    print(
        f"Posted server count ({bot.topggpy.guild_count}), shard count ({bot.shard_count})"
    )

# bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", "password")
# bot.topgg_webhook.run(5000)

@bot.event
async def on_dbl_vote(data):
    # When someone votes for bot
    if data["type"] == "test":
        return bot.dispatch("dbl_test", data)
    print(f"Received a vote:\n{data}")
    f = open('db.txt', 'a')
    f.write(data)

@bot.event
async def on_dbl_test(data):
    # Vote test lol
    print(f"Received a test vote:\n{data}")

@bot.command()
async def profile(ctx):
  hasvoted = False
  f = open("db.txt", "r")
  for line in f:
    user, votes = line.split('-')
    if str(ctx.message.author.id) == user:
      hasvoted = True
      await ctx.send("Hi, <@" + user + "> ! You have voted for CopyPasta " + votes + " times. Rewards are coming soon!")
  if not hasvoted:
    await ctx.send("Hi, <@" + str(ctx.message.author.id) + "> ! You haven't voted for CopyPasta yet. If you have, we apologise, as currently the system is really, really, really broken.")

@bot.command()
async def nsfw(ctx):
  if ctx.channel.is_nsfw():
    bot.nsfwenabled = True
  else:
    bot.nsfwenabled = False
  await ctx.send("NSFW is currently " + str(bot.nsfwenabled))

@bot.command()
async def copypasta(ctx):
  if ctx.channel.is_nsfw():
    bot.nsfwenabled = True
  else:
    bot.nsfwenabled = False
  try:
          sub = reddit.subreddit("copypasta")
          limit = bot.amountToGet
          posts = sub.top("day", limit = limit)
          random_post_number = random.randint(0, limit)
          print("Getting posts...")
          for i,post in enumerate(posts):
              if i == random_post_number:
                bot.string = post.selftext
                if post.over_18:
                  if bot.nsfwenabled == True:
                    content = "**" + post.title.replace("*", "\*") + "**" + "\n" + post.selftext + " (from " + post.url + ")"
                  elif bot.nsfwenabled == False:
                    content = "This submission was NSFW, and this is a non-NSFW channel. Switch to an NSFW channel to enable NSFW. If you still want to see it, the url is ||<" + post.url + ">||"
                  else: 
                    content = "This is an error that should never happen. You win. <:mad_cry:786804608986382377>"
                else:
                  content = "**" + post.title.replace("*", "\*") + "**" + "\n" + post.selftext + " (from " + post.url + ")"
                
  except:
          await ctx.send("It seems that Reddit is experiencing issues. Either that, or you've been spamming this bot so much that it's being rate limited. Please try again later. <:mad_cry:786804608986382377>")
          await ctx.send("This issue has been reported to the creator.")
          guild = bot.get_guild(855275010556821524)
          kevlu8 = guild.get_member(458684594703695872)
          if kevlu8 == None:
            kevlu8 = guild.get_member_named("kevlu8#5240")
          await kevlu8.send("Issue was found! Check to see if it was Reddit's end, or your end!")
          
  try: 
    print(content)
    await ctx.send(content)
  except:
    print("too long! splitting...")
    splitat = 2000
    left, right = bot.string[:splitat], bot.string[splitat:]
    try:
      await ctx.send(left)
      await ctx.send(right + " (from " + post.url + ")")
    except:
        middle1, middle2 = right[:splitat], right[splitat:]
        try:
          await ctx.send(middle1)
          await ctx.send(middle2 + " (from " + post.url + ")")
        except:
          await ctx.send("This post was way too long (over 6000 characters) and we couldn't send it. Link: " + post.url)

@bot.command(pass_context=True)
async def update(ctx):
	if ctx.message.author.id == 458684594703695872:
		activity = discord.Game(name="restarting in 5 minutes.", type=3)
		await bot.change_presence(status=discord.Status.online, activity=activity)
		await ctx.send("Done. I will remind you in 5 minutes when it is safe to restart.")
		sleep(240)
		activity2 = discord.Game(name = "restarting in 1 minute.", type = 3)
		await bot.change_presence(status=discord.Status.online, activity = activity2)
		sleep(60)
		await ctx.send("<@458684594703695872> restart ready!")

	else: 
		await ctx.send("how tf did you find this command it's reserved for the bot owner only")

@bot.command()
async def vote(ctx):
  await ctx.send("Vote for CopyPasta here: https://top.gg/bot/882832904605020190/vote")


@bot.command(pass_context = True)
async def invite(ctx):
  prsn = ctx.message.author
  await ctx.message.add_reaction("<:success:883760173880057906>")
  await prsn.send("Invite CopyPasta to your server! https://discord.com/oauth2/authorize?client_id=882832904605020190&permissions=18432&scope=bot")

@bot.command()
async def help(ctx):
    embedVar = discord.Embed(title="Commands", description="If you changed the prefix with :prefix, replace the : in all these with your prefix.", color=0x00ff00)
    embedVar.add_field(name=":help", value="Displays this help message!", inline=False)
    embedVar.add_field(name=":copypasta", value="Sends a random copypasta from top", inline=False)
    embedVar.add_field(name = ":invite", value = "DMs you the link to invite CopyPasta to your server!")
    embedVar.add_field(name = ":nsfw", value = "Displays if NSFW is currently enabled in the channel. Using this bot in a non-nsfw channel will limit the amount of copypastas available. Use: :nsfw status")
    embedVar.add_field(name = ":randomnumber", value = "Pick a random number between 2 numbers! Use: :random [num1] [num2]")
    embedVar.add_field(name = ":8ball", value = "Gives a random copypasta response! Use: :8ball [question]")
    embedVar.add_field(name = ":vote", value = "Feeling generous and want to support the bot? Vote for it by running this command!")
    embedVar.add_field(name = ":amount", value = "Amount of posts to randomly choose from! Warning: higher values may cause a slower response time. Recommended amount is 100. Use: :amount [num]")
    embedVar.add_field(name = ":servercount", value = "Sends the amount of servers this bot is in. Use: :servercount")
    # embedVar.add_field(name = ":prefix", value = "Changes the prefix to whatever you want. Use: :prefix [prefix]")
    # embedVar.add_field(name = ":profile", value = "Sends your profile. So far, it only contains amount of votes, but more coming soon.")
    await ctx.send(embed=embedVar)
  
@bot.command()
async def amount(ctx, amount):
	amount = int(amount)
	if amount < 1000:
		bot.amountToGet = amount
		await ctx.send("Success! The amount of posts to get was successfully changed to " + str(amount))
	else:
		await ctx.send(str(amount) + " is waaaaayyyy too much. Are you kidding ??? Are you trying to get the bot's useragent blacklisted from Reddit ??? The limit is 1000 to prevent people like you from trolling. <:shut:778791758519336972>")

@bot.command()
async def servercount(ctx):
  await ctx.send("CopyPasta is in " + str(len(bot.guilds)) + " servers. Want to raise this number? Run `:invite`!")

@bot.command()
async def randomnumber(ctx, num1, num2):
  await ctx.send("Your random number between " + num1 + " and " + num2 + " is " + str(random.randint(int(num1), int(num2))) + ".")

@bot.command(name="8ball")
async def _8ball(ctx):
  if ctx.channel.is_nsfw():
    bot.nsfwenabled = True
  else:
    bot.nsfwenabled = False
  answers = [
    "I would say \"Yes\" to this question, but you'd respond with \"You think you're funny, huh? You think you're funny saying 'yes' to a non 'yes or no' question? I bet you think you're really witty saying that rehashed meme again. Well you aren't. You aren't funny. You aren't hilarious in the slightest. I didn't laugh. I didn't grin, I didn't even exhale out of my nose. Your joke wasn't funny. Your joke was shit. It's stale and shitty. If you're going to make a joke, make an original one or at least improve the one you're taking. This was low effort. Step up your game, or just don't make jokes in the comment section at all.\"",

    'Are you kidding ??? What the \*\*\*\* are you talking about man ? You are a biggest looser i ever seen in my life ! You was doing PIPI in your pampers when i was beating players much more stronger then you! You are not proffesional, because proffesionals knew how to lose and congratulate opponents, you are like a girl crying after i beat you! Be brave, be honest to yourself and stop this trush talkings!!! Everybody know that i am very good blitz player, i can win anyone in the world in single game! And "w"esley "s"o is nobody for me, just a player who are crying every single time when loosing, ( remember what you say about Firouzja ) !!! Stop playing with my name, i deserve to have a good name during whole my chess carrier, I am Officially inviting you to OTB blitz match with the Prize fund! Both of us will invest 5000$ and winner takes it all! I suggest all other people who\'s intrested in this situation, just take a look at my results in 2016 and 2017 Blitz World championships, and that should be enough... No need to listen for every crying babe, Tigran Petrosyan is always play Fair ! And if someone will continue Officially talk about me like that, we will meet in Court! God bless with true! True will never die ! Liers will kicked off...',

    "No\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\n**FUCK YOU.**",

    'The problem is you\'re focusing on the things in life that don\'t really matter. When I was a kid I had hopes and dreams. We all did. But over time, the daily grind gets in the way and you miss the things that really matter, even though they are right in front of you, staring you in the face. I think the next time you should ask yourself "Am I on the right track here?". I don\'t mean to be rude but people like you I really pity. So maybe you could use the few brain cells you have and take advantage of the knowledge I have given you now. Good luck.',

    "I’ve been laughing at this for the past 20 years. I laughed so hard that my lung collapsed and I have been bedridden in hospital for the past two decades, please someone burn my eyes out of my skill because whenever I read this I laugh so hard that the doctors have to open me back up and replace my lung with the lung of a swine. So many pigs have been slaughtered in the name of this meme. \n\nPlease donate to my gofundme",

    "I made a copypasta response to this but i'm to lazyto sned it.",

    "STOP POSTING ABOUT DISCORD. IM TIRED OF DISCORD. MY FRIENDS SEND ME TIKTOKS AND AMONG US MEMES AND PENIS MEMES AND CHUNGUS MEMES. I was in a server, right? And ***ALL*** OF THE CHANNELS ARE JUST FURRY RP. I showed my among us meme to my girlfriend and I said, \"Hey babe, WHEN THE SUSSY SUS AMONG US IS SUS HAHA\" __***DING DING DING DING DING. DING. DING DING DING DING DING. DING. DING DING DING DING DING. DING. DING DING DING DING DING.***__ I FUCKING LOOKED AT A DISCORD MOD AND I SAID \"THATS A BIT SUSSY.\" I LOOKED AT MY PINGS AND I GO \"STOP PINGING ME IN THE AMONG US CHANNEL!\" I was in a server, right? And OHHHHHHHHHH and the logo like OHHHHHHHHHHHHHHHHHHHHHHH I flip on light mode and I go AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
  ]

  answersNSFW = [
    "I would say \"Yes\" to this question, but you'd respond with \"You think you're funny, huh? You think you're funny saying 'yes' to a non 'yes or no' question? I bet you think you're really witty saying that rehashed meme again. Well you aren't. You aren't funny. You aren't hilarious in the slightest. I didn't laugh. I didn't grin, I didn't even exhale out of my nose. Your joke wasn't funny. Your joke was shit. It's stale and shitty. If you're going to make a joke, make an original one or at least improve the one you're taking. This was low effort. Step up your game, or just don't make jokes in the comment section at all.\"",

    'Are you kidding ??? What the \*\*\*\* are you talking about man ? You are a biggest looser i ever seen in my life ! You was doing PIPI in your pampers when i was beating players much more stronger then you! You are not proffesional, because proffesionals knew how to lose and congratulate opponents, you are like a girl crying after i beat you! Be brave, be honest to yourself and stop this trush talkings!!! Everybody know that i am very good blitz player, i can win anyone in the world in single game! And "w"esley "s"o is nobody for me, just a player who are crying every single time when loosing, ( remember what you say about Firouzja ) !!! Stop playing with my name, i deserve to have a good name during whole my chess carrier, I am Officially inviting you to OTB blitz match with the Prize fund! Both of us will invest 5000$ and winner takes it all! I suggest all other people who\'s intrested in this situation, just take a look at my results in 2016 and 2017 Blitz World championships, and that should be enough... No need to listen for every crying babe, Tigran Petrosyan is always play Fair ! And if someone will continue Officially talk about me like that, we will meet in Court! God bless with true! True will never die ! Liers will kicked off...',

    "No\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\nNo\n\n**FUCK YOU.**",

    "MAYBE?!💥Never😤say🍕maybe🤩, only😙say👑yes🙈or👟no💦because🍪I⚽️want💯to🅱️know💖the💚answer🏩.You✈️should🥇know🍑that🥚maybe🌨is⭐️for🌈wimps🐡and⚡️pussies 👀, ok👁👅👁?! I🖖don’t🤡want🤛to☠️hear👿a😔maybe🙅‍♀️anymore🐷you🌸stupid🌻cunt💫. Just👌suck📖my☯️dick🖍you🎀little🎤cum⚔️dumpster🛴😫😫😫👉👌🙏💦💦💯💯🔥🔥",

    "The problem is you're focusing on the things in life that don't really matter. When I was a kid I had hopes and dreams. We all did. But over time, the daily grind gets in the way and you miss the things that really matter, even though they are right in front of you, staring you in the face. I think the next time you should ask yourself \"Am I on the right track here?\". I don't mean to be rude but people like you I really pity. So maybe you could use the few brain cells you have and take advantage of the knowledge I have given you now. Good luck.",

    "Idk. I’ve been laughing at this for the past 20 years. I laughed so hard that my lung collapsed and I have been bedridden in hospital for the past two decades, please someone burn my eyes out of my skill because whenever I read this I laugh so hard that the doctors have to open me back up and replace my lung with the lung of a swine. So many pigs have been slaughtered in the name of this meme. \n\nPlease donate to my gofundme",

    "Fuck off liberal nutbag. You miserable slut. I'll have you know I graduated from stanford with a masters degree in cock suckingology. You absolute buffoon, the fact that you believe you can challenge me is of unparralled stupidity. You ought to consider yourself lucky I didn't fingerbang your cat over that comment. Stupid libcuck heterosexual trash.",

    "Shut up and go away. You swine. You vulgar little maggot. You worthless bag of filth. I wager you couldn't empty a boot of excrement were the instructions on the heel. You are a canker. A sore that won't go away. I would rather kiss a lawyer than be seen with you. Try to edit your responses of unnecessary material before attempting to impress us with your insight. The evidence that you are a nincompoop will still be available to readers, but they will be able to access it more rapidly. You snail-skulled little rabbit. Would that a hawk pick you up, drive its beak into your brain, and upon finding it rancid set you loose to fly briefly before spattering the ocean rocks with the frothy pink shame of your ignoble blood. May you choke on the queasy, convulsing nausea of your own trite, foolish beliefs. You are weary, stale, flat and unprofitable. You are grimy, squalid, nasty and profane. You are foul and disgusting. You're a fool, an ignoramus. And what meaning do you expect your delusional self-important statements of unknowing, inexperienced opinion to have to us who think and reason? What fantasy do you hold that you would believe that your tiny-fisted tantrums would have more weight than that of a leprous desert rat, spinning rabidly in a circle, waiting for the bite of the snake? You are a waste of flesh. You have no rhythm. You are ridiculous and obnoxious. You are the moral equivalent of a leech. You are a living emptiness, a meaningless void. You are sour and senile. You are a disease, you puerile one-handed slack-jawed, drooling meatslapper. You smarmy lagerlout git. You bloody woofter sod. Bugger off, pillock. You grotty wanking oik artless base-court apple-john. You clouted boggish foot-licking twit. You dankish clack-dish plonker. You gormless crook-pated tosser. You churlish boil-brained clotpole ponce. You cockered bum-bailey poofter. You gob-kissing gleeking flap-mouthed coxcomb. You dread-bolted fobbing beef-witted clapper-clawed flirt-gill. You are a fiend and a coward, and you have bad breath. You are degenerate, noxious and depraved. I feel debased just for knowing you exist. I despise everything about you, and I wish you would go away. I cannot believe how incredibly stupid you are. I mean rock-hard stupid. Dehydrated-rock-hard stupid. Stupid so stupid that it goes way beyond the stupid we know into a whole different dimension of stupid. You are trans-stupid stupid. Meta-stupid. Some pure essence of a stupid so uncontaminated by anything else as to be beyond the laws of physics that we know. I'm sorry. I can't go on. This is an epiphany of stupid for me. After this, you may not hear from me again for a while. I don't have enough strength left to deride your ignorant questions and half-baked comments about unimportant trivia, or any of the rest of this drivel. Duh. I mean, really, stringing together a bunch of insults among a load of babbling was hardly effective. True, these are rudimentary skills that many of us \"normal\" people take for granted that everyone has an easy time of mastering. But we sometimes forget that there are \"challenged\" persons in this world who find these things more difficult. If I had known, that this was your case then I would have never read your post. It just wouldn't have been \"right\". Sort of like parking in a handicap space. I wish you the best of luck in the emotional, and social struggles that seem to be placing such a demand on you. You're an idiot. A moron of the highest order. You're so stupid it's a wonder and a pity you can remember to breathe. Intelligent ideas bounce off your head as if it were coated with teflon. Creative thoughts take alternate transportation in order to avoid even being in the same state as you. If you had an original thought it would die of loneliness before the hour was out. On an intelligence scale of 1 to 10 (10 corresponding to the highest attainable IQ) you're rating is so far into negative numbers that one would need to travel into another quantum reality in order to even catch a distant glimpse of it. Your personality is that of a rabid Chihuahua intent on destroying its own tail. Your powers of observation are akin to those of the bird that keeps slamming into the picture window trying to get that other bird it keeps seeing. You are walking, talking proof that you don't have to be sentient to survive, and that Barnum was thinking of you when he uttered his immortal phrase regarding the birth of a sucker. You are, at varying times, tedious, boring, and even occasionally earth shatteringly hilarious in your idiocy, routinely childish, moronic, pathetic, wretched, disgusting and pitiful. You are wholly without any redeeming social grace or value. If God ever decides to give the planet an enema you'd better run like the wind because anywhere you stand is a suitable place for The Insertion. There is no animal so disgusting, so vile that it deserves comparison to you, for even the lowest, dirtiest, most parasitic member of the animal kingdom fills an ecological niche. You fill no niche. To call you a parasite would be injurious and defamatory to the thousands of honest parasitic species. You are worse than vermin, for vermin do not pretend to be what it is not. You are truly human garbage. You are a fraudulent, lying, predatory charlatan. You are of less worth than a burnt-out light bulb. You will forever live in shame. You have nothing to say, and Godwin's Law does not apply when writing about you. You are the anti-Midas, for all that you touch becomes valueless and unusable. Mothers gather their children close when you appear. You are an aberration, a corruption, and a boil that needs to be lanced. You are a poison in need of being vomited. You are a tooth so rotten it infects the whole body. You are sperm that should have been captured in a condom and flushed down a toilet. I don't like you. I don't like anybody who has as little respect for others as you do. Go away, you swine. You're a putrescent mass, a walking vomit. You are a spineless little worm deserving nothing but the profoundest contempt. You are a jerk, a cad, and a weasel. Your life is a monument to stupidity. You are a stench, a revulsion, a big suck on a sour lemon. You are a curdled staggering mutant dwarf smeared richly with the effluvia and offal accompanying your alleged birth into this world. Meaningful to no one, abandoned by the puke-drooling, giggling beasts that sired you and then killed themselves in recognition of what they had done. I will never get over the embarrassment of belonging to the same species as you. You are a monster, an ogre, a malformity. I wretch at the very thought of you. You have all the appeal of a paper cut. Lepers avoid you. You are vile, worthless, less than nothing. You are a weed, a fungus, and the dregs of this earth. And did I mention you smell? Monkeys look down on you. Even sheep won't have sex with you. You are unreservedly pathetic, starved for attention, and lost in a land that reality forgot. You are a waste of flesh. On a good day you're a halfwit. You are deficient in all that lends character. You have the personality of wallpaper. You are dank and filthy. You are asinine and benighted. You are the source of all unpleasantness. You spread misery and sorrow wherever you go.You are hypocritical, greedy, violent, malevolent, vengeful, cowardly, deadly, mendacious, meretricious, loathsome, despicable, belligerent, opportunistic, barratrous, contemptible, criminal, fascistic, bigoted, racist, sexist, avaricious, tasteless, idiotic, brain-damaged, imbecilic, insane, arrogant, deceitful, demented, lame, self-righteous, byzantine, conspiratorial, satanic, fraudulent, libellous, bilious, splenetic, spastic, ignorant, clueless, illegitimate, harmful, destructive, dumb, evasive, double-talking, devious, revisionist, narrow, manipulative, paternalistic, fundamentalist, dogmatic, idolatrous, unethical, cultic, diseased, suppressive, controlling, restrictive, malignant, deceptive, dim, crazy, weird, dystrophic, stifling, uncaring, plantigrade, grim, unsympathetic, jargon-spouting, censorious, secretive, aggressive, mind-numbing, abrasive, poisonous, flagrant, self-destructive, abusive, and socially-retarded. Shut up and go away",

    "STOP POSTING ABOUT DISCORD. IM TIRED OF DISCORD. MY FRIENDS SEND ME TIKTOKS AND AMONG US MEMES AND PENIS MEMES AND CHUNGUS MEMES. I was in a server, right? And ***ALL*** OF THE CHANNELS ARE JUST FURRY RP. I showed my among us meme to my girlfriend and I said, \"Hey babe, WHEN THE SUSSY SUS AMONG US IS SUS HAHA\" __***DING DING DING DING DING. DING. DING DING DING DING DING. DING. DING DING DING DING DING. DING. DING DING DING DING DING.***__ I FUCKING LOOKED AT A DISCORD MOD AND I SAID \"THATS A BIT SUSSY.\" I LOOKED AT MY PINGS AND I GO \"STOP PINGING ME IN THE AMONG US CHANNEL!\" I was in a server, right? And OHHHHHHHHHH and the logo like OHHHHHHHHHHHHHHHHHHHHHHH I flip on light mode and I go AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
  ]

  if bot.nsfwenabled:
    ans = answersNSFW[random.randint(0, len(answersNSFW) - 1)]
    try:
      await ctx.send(ans)
    except:
        print("too long! splitting...")
        string2 = ans
        splitat2 = 5000
        left, right = string2[:splitat2], string2[splitat2:]
        left1, left2 = left[:4000], left[4000:]
        left3, left4 = left1[:2000], left1[2000:]
        right1, right2 = right[:4000], right[4000:]
        right3, right4 = right1[:2000], right1[2000:]
        try:
          await ctx.send(left3)
          await ctx.send(left4)
          await ctx.send(left2)
          await ctx.send(right3)
          await ctx.send(right4)
        except:
              await ctx.send("This is an error that should never happen. You win. <:mad_cry:786804608986382377>")

  else:
    ans2 = answers[random.randint(0, len(answers) - 1)]
    try:
      await ctx.send(ans2)
    except:
        print("too long! splitting...")
        string2 = ans
        splitat2 = 5000
        left, right = string2[:splitat2], string2[splitat2:]
        left1, left2 = left[:4000], left[4000:]
        left3, left4 = left1[:2000], left1[2000:]
        right1, right2 = right[:4000], right[4000:]
        right3, right4 = right1[:2000], right1[2000:]
        try:
          await ctx.send(left3)
          await ctx.send(left4)
          await ctx.send(left2)
          await ctx.send(right3)
          await ctx.send(right4)
          await ctx.send(right2)
        except:
              await ctx.send("This is an error that should never happen. You win. <:mad_cry:786804608986382377>")

bot.run(str(os.environ['discordtoken']))
