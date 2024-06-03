import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import datetime
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=".new"))
    print ("Hi, my name is " + bot.user.name)
    print ("My ID is: " + str(bot.user.id))
    print ("I'm ready to create teams!")
    print ("---------------------------------------------------------------------------------")

@bot.command(pass_context = True)
async def new(ctx):
    # Declare global variables to be used across functions
    global idList, cptList, nameList, started, team1, team2, pickNum, mapList, theGuild, emojiList, members, teamMessage, mapMsg

    # Initialize the variables
    idList = []
    cptList = []
    nameList = []
    started = False
    team1 = []
    team2 = []
    mapList = ["Cache", "Dust II", "Inferno", "Mirage", "Nuke", "Overpass", "Train"]
    pickNum = 0
    emojiList = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

    teamMessage = None
    mapMsg = None

    # Check if the user is in a voice channel
    if ctx.author.voice and ctx.author.voice.channel:
        
        # Gather members from the voice channel
        for member in discord.utils.get(ctx.message.guild.channels, id = ctx.message.author.voice.channel.id).members:
            idList.append(member.id)
            nameList.append(member.display_name)      

        # Add the author to the list if not already present
        if ctx.message.author.id not in idList:
            idList.append(ctx.message.author.id)
        
        if ctx.message.author.display_name not in nameList:
            nameList.append(ctx.message.author.display_name)

        theGuild = ctx.message.author.guild
        channel = ctx.message.author.voice.channel.id
        voice_channel = discord.utils.get(ctx.message.guild.channels, id = channel)
        members = voice_channel.members

        # Delete previous bot messages and command messages
        msgList = []
        async for message in ctx.message.channel.history(limit=50):
            if message.author.id == bot.user.id or message.content == ".new":
                msgList.append(message)
        if len(msgList) == 1:
            await msgList[0].delete()
        else:
            await ctx.message.channel.delete_messages(msgList)

        
        # Check the number of users in the voice channel
        if len(idList) < 10:
            await ctx.send("There are fewer than 10 users in your voice channel!")

        elif len(idList) > 10:
            await ctx.send("There are more than 10 users in your voice channel!")

        else:
            # Start the game and send an embedded message with reactions for users to interact with
            started = True
            newEmbed = discord.Embed(colour=discord.Colour(0x1b207))

            newEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

            newEmbed.add_field(name="▶️: Add yourself to the list of captains.", value="\u200b")
            newEmbed.add_field(name="🔀: Choose two random captains.", value="\u200b")
            newEmbed.add_field(name="🆗: Proceed to voting once all captains have entered.", value="\u200b")
            newEmbed.add_field(name="**Captains:**", value="``` ```")

            newMessage = await ctx.send(embed=newEmbed)
            await newMessage.add_reaction('▶')
            await newMessage.add_reaction('🔀')
            await newMessage.add_reaction('🆗')
    
    else:
        # If user is not in a voice channel, delete previous bot messages and command messages
        msgList = []
        async for message in ctx.message.channel.history(limit=50):
            if message.author.id == bot.user.id or message.content == ".new":
                msgList.append(message)
        if len(msgList) == 1:
            await msgList[0].delete()
        else:
            await ctx.message.channel.delete_messages(msgList)

        await ctx.send("You must join a voice channel to do that!")

@bot.event
async def on_reaction_add(reaction, user):
    global started, playerNum, mystring, pickNum, theGuild, voteMessage, helperMsg, removed1, removed2, removed3, removed4, removed5, removed6, removed7, removed8, newMessage, selected, capt1, capt2, firstpick, secondpick, availPlayers, teamMessage, availMaps, mapMsg, mapNum, linerMsg, valorant
    mystring = ""
    playerNum = 0

    captain = user.display_name
    if started == True:
        channel = reaction.message.channel

        if user.id != 463672824922374145: # Ensure the user is not the bot itself
            if newMessage.id == reaction.message.id:
                if reaction.emoji == '▶':
                    captain = user
                    if captain not in cptList:
                        cptList.append(captain)
                        count = 0
                        cptString = ""
                        for captain in cptList:
                            count +=1
                            cptString += (str(count) + ". " + captain.display_name + "\n")



                        newEmbed = discord.Embed(colour=discord.Colour(0x1b207))

                        newEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                        newEmbed.add_field(name="▶️: Add yourself to the list of captains.", value="\u200b")
                        newEmbed.add_field(name="🔀: Choose two random captains.", value="\u200b")
                        newEmbed.add_field(name="🆗: Proceed to voting once all captains have entered.", value="\u200b")
                        newEmbed.add_field(name="**Captains:**", value="```" + cptString + "```")

                        await newMessage.delete()
                        newMessage = await channel.send(embed=newEmbed)

                        await newMessage.add_reaction('▶')
                        await newMessage.add_reaction('🔀')
                        await newMessage.add_reaction('🆗')
                    else:
                        await newMessage.remove_reaction('▶', user)
                        cptList.remove(captain)

                        count = 0
                        cptString = ""
                        for captain in cptList:
                            count +=1
                            cptString += (str(count) + ". " + captain.display_name + "\n")

                        if cptString == "":
                            cptString = " "

                        newEmbed = discord.Embed(colour=discord.Colour(0x1b207))

                        newEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                        newEmbed.add_field(name="▶️: Add yourself to the list of captains.", value="\u200b")
                        newEmbed.add_field(name="🔀: Choose two random captains.", value="\u200b")
                        newEmbed.add_field(name="🆗: Proceed to voting once all captains have entered.", value="\u200b")
                        newEmbed.add_field(name="**Captains:**", value="```" + cptString + "```")

                        await newMessage.delete()
                        newMessage = await channel.send(embed=newEmbed)

                        await newMessage.add_reaction('▶')
                        await newMessage.add_reaction('🔀')
                        await newMessage.add_reaction('🆗')

                elif reaction.emoji == '🆗':
                    if started == True:
                        if len(cptList) >= 2:
                            selected = random.sample(list(cptList), 2)
                            capt1 = selected[0].display_name
                            capt2 = selected[1].display_name
                            msgList = []
                            async for message in channel.history(limit=50):
                                if message.author.id == bot.user.id:
                                    msgList.append(message)
                            if len(msgList) == 1:
                                await msgList[0].delete()
                            else:
                                await ctx.message.channel.delete_messages(msgList)
                            linerMsg = await channel.send("**Captain of team 1 is **" + capt1 + "\n**Captain of team 2 is **" + capt2 + "\n-------------------------------------------------------------")
                            team1.append(capt1)
                            team2.append(capt2)

                            mystring = ""
                            availPlayers = nameList
                            playerNum = 0

                            availPlayers.remove(capt1)
                            availPlayers.remove(capt2)

                            firstpick = int(random.uniform(0, 1))
                            if firstpick == 0:
                                secondpick = 1
                            else:
                                secondpick = 0
                            helperMsg = await channel.send(selected[firstpick].mention + " gets first pick.\nSelect the emoji that corresponds with the player you would like to pick from the list below.")
                            for name in availPlayers:
                                playerNum += 1
                                if playerNum == 1:
                                    mystring += ("```" + str(playerNum) + ". " + str(name) + "\n")

                                elif playerNum == 8:
                                    mystring += (str(playerNum) + ". " + str(name) + "```")

                                else:
                                    mystring += (str(playerNum) + ". " + str(name) + "\n")

                            if selected[firstpick].avatar_url == "":
                                thumbnail = selected[firstpick].default_avatar_url
                            else:
                                thumbnail = selected[firstpick].avatar_url

                            voteEmbed = discord.Embed(title="**" + selected[firstpick].display_name + "'s Pick**", colour=discord.Colour(0xd6fb7))
                            voteEmbed.set_thumbnail(url=thumbnail)
                            voteEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                            voteEmbed.add_field(name="**Team 1:**", value="1. " + selected[firstpick].display_name + " (captain) \n2. \n3. \n4. \n5.", inline=True)
                            voteEmbed.add_field(name="**Team 2:**", value="1. " + selected[secondpick].display_name + " (captain) \n2. \n3. \n4. \n5.", inline=True)
                            voteEmbed.add_field(name="**Select:**", value=mystring)


                            voteMessage = await channel.send(embed=voteEmbed)
                            currPos = 0

                            for name in availPlayers:
                                await voteMessage.add_reaction(emojiList[currPos])
                                currPos += 1
                        else:
                            await newMessage.remove_reaction('🆗', user)
                            await channel.send("There must be at least two captains on the list, click ▶ to join the list!")




                elif reaction.emoji == '🔀':
                    if started == True:
                        msgList = []
                        async for message in channel.history(limit=50):
                            if message.author.id == bot.user.id:
                                msgList.append(message)
                        if len(msgList) == 1:
                            await msgList[0].delete()
                        else:
                            await ctx.message.channel.delete_messages(msgList)
                        for member in members:
                            cptList.append(member)
                        selected = random.sample(list(cptList), 2)
                        capt1 = selected[0].display_name
                        capt2 = selected[1].display_name
                        team1.append(capt1)
                        team2.append(capt2)
                        linerMsg = await channel.send("**Captain of team 1 is **" + capt1 + "\n**Captain of team 2 is **" + capt2 + "\n-------------------------------------------------------------")

                    mystring = ""
                    availPlayers = nameList
                    playerNum = 0

                    availPlayers.remove(capt1)
                    availPlayers.remove(capt2)

                    firstpick = int(random.uniform(0, 1))
                    if firstpick == 0:
                        secondpick = 1
                    else:
                        secondpick = 0
                    helperMsg = await channel.send(selected[firstpick].mention + " gets first pick.\nSelect the emoji that corresponds with the player you would like to pick from the list below.")

                    for name in availPlayers:
                        playerNum += 1
                        if playerNum == 1:
                            mystring += ("```" + str(playerNum) + ". " + str(name) + "\n")

                        elif playerNum == 8:
                            mystring += (str(playerNum) + ". " + str(name) + "```")

                        else:
                            mystring += (str(playerNum) + ". " + str(name) + "\n")

                    if selected[firstpick].avatar_url == "":
                        thumbnail = selected[firstpick].default_avatar_url
                    else:
                        thumbnail = selected[firstpick].avatar_url

                    voteEmbed = discord.Embed(title="**" + selected[firstpick].display_name + "'s Pick**", colour=discord.Colour(0xd6fb7))
                    voteEmbed.set_thumbnail(url=thumbnail)
                    voteEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                    voteEmbed.set_footer(icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    voteEmbed.add_field(name="**Team 1:**", value="1. " + selected[firstpick].display_name + " (captain) \n2. \n3. \n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Team 2:**", value="1. " + selected[secondpick].display_name + " (captain) \n2. \n3. \n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Select:**", value=mystring)



                    voteMessage = await channel.send(embed=voteEmbed)

                    currPos = 0

                    for name in availPlayers:
                        await voteMessage.add_reaction(emojiList[currPos])
                        currPos += 1


            elif voteMessage.id == reaction.message.id and reaction.emoji in emojiList:

                if captain == selected[firstpick].display_name and pickNum == 0:
                    pickNum = 1

                    team1.append(availPlayers[emojiList.index(reaction.emoji)])
                    await helperMsg.edit(content="**" + availPlayers[emojiList.index(reaction.emoji)] + " has been added to team 1.**" + "\n" + selected[secondpick].mention + " may now pick one player from the list below")
                    removed1 = availPlayers.pop(emojiList.index(reaction.emoji))


                    if selected[secondpick].avatar_url == "":
                        thumbnail = selected[secondpick].default_avatar_url
                    else:
                        thumbnail = selected[secondpick].avatar_url

                    for name in availPlayers:
                        playerNum += 1
                        if playerNum == 1:
                            mystring += ("```" + str(playerNum) + ". " + str(name) + "\n")

                        elif playerNum == len(availPlayers):
                            mystring += (str(playerNum) + ". " + str(name) + "```")
                        else:
                            mystring += (str(playerNum) + ". " + str(name) + "\n")

                    voteEmbed = discord.Embed(title="**" + selected[secondpick].display_name + "'s Pick**", colour=discord.Colour(0xcd2128))
                    voteEmbed.set_thumbnail(url=thumbnail)
                    voteEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    voteEmbed.add_field(name="**Team 1:**", value="1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. \n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Team 2:**", value="1. " + selected[secondpick].display_name + " (captain) \n2. \n3. \n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Select:**", value=mystring)


                    await voteMessage.delete()
                    voteMessage = await channel.send(embed=voteEmbed)





                    currPos = 0

                    for name in availPlayers:
                        await voteMessage.add_reaction(emojiList[currPos])
                        currPos += 1

                elif captain == selected[secondpick].display_name and pickNum == 1:
                    pickNum = 2

                    team2.append(availPlayers[emojiList.index(reaction.emoji)])
                    await helperMsg.edit(content="**" + availPlayers[emojiList.index(reaction.emoji)] + " has been added to team 2.**" + "\n" + selected[secondpick].mention + " may now pick another player from the list below")
                    removed2 = availPlayers.pop(emojiList.index(reaction.emoji))


                    if selected[secondpick].avatar_url == "":
                        thumbnail = selected[secondpick].default_avatar_url
                    else:
                        thumbnail = selected[secondpick].avatar_url

                    for name in availPlayers:
                        playerNum += 1
                        if playerNum == 1:
                            mystring += ("```" + str(playerNum) + ". " + str(name) + "\n")

                        elif playerNum == len(availPlayers):
                            mystring += (str(playerNum) + ". " + str(name) + "```")
                        else:
                            mystring += (str(playerNum) + ". " + str(name) + "\n")

                    voteEmbed = discord.Embed(title="**" + selected[secondpick].display_name + "'s Pick**", colour=discord.Colour(0xcd2128))
                    voteEmbed.set_thumbnail(url=thumbnail)
                    voteEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    voteEmbed.add_field(name="**Team 1:**", value="1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. \n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Team 2:**", value="1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. \n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Select:**", value=mystring)


                    await voteMessage.delete()
                    voteMessage = await channel.send(embed=voteEmbed)





                    currPos = 0

                    for name in availPlayers:
                        await voteMessage.add_reaction(emojiList[currPos])
                        currPos += 1

                elif captain == selected[secondpick].display_name and pickNum == 2:
                    pickNum = 3

                    team2.append(availPlayers[emojiList.index(reaction.emoji)])
                    await helperMsg.edit(content="**" + availPlayers[emojiList.index(reaction.emoji)] + " has been added to team 2.**" + "\n" + selected[firstpick].mention + " may now pick a player from the list below")
                    removed3 = availPlayers.pop(emojiList.index(reaction.emoji))


                    if selected[firstpick].avatar_url == "":
                        thumbnail = selected[firstpick].default_avatar_url
                    else:
                        thumbnail = selected[firstpick].avatar_url

                    for name in availPlayers:
                        playerNum += 1
                        if playerNum == 1:
                            mystring += ("```" + str(playerNum) + ". " + str(name) + "\n")

                        elif playerNum == len(availPlayers):
                            mystring += (str(playerNum) + ". " + str(name) + "```")
                        else:
                            mystring += (str(playerNum) + ". " + str(name) + "\n")

                    voteEmbed = discord.Embed(title="**" + selected[firstpick].display_name + "'s Pick**", colour=discord.Colour(0xd6fb7))
                    voteEmbed.set_thumbnail(url=thumbnail)
                    voteEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    voteEmbed.add_field(name="**Team 1:**", value="1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. \n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Team 2:**", value="1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Select:**", value=mystring)


                    await voteMessage.delete()
                    voteMessage = await channel.send(embed=voteEmbed)





                    currPos = 0

                    for name in availPlayers:
                        await voteMessage.add_reaction(emojiList[currPos])
                        currPos += 1


                elif captain == selected[firstpick].display_name and pickNum == 3:
                    pickNum = 4

                    team1.append(availPlayers[emojiList.index(reaction.emoji)])
                    await helperMsg.edit(content="**" + availPlayers[emojiList.index(reaction.emoji)] + " has been added to team 1.**" + "\n" + selected[firstpick].mention + " may now pick another player from the list below")
                    removed4 = availPlayers.pop(emojiList.index(reaction.emoji))


                    if selected[firstpick].avatar_url == "":
                        thumbnail = selected[firstpick].default_avatar_url
                    else:
                        thumbnail = selected[firstpick].avatar_url

                    for name in availPlayers:
                        playerNum += 1
                        if playerNum == 1:
                            mystring += ("```" + str(playerNum) + ". " + str(name) + "\n")

                        elif playerNum == len(availPlayers):
                            mystring += (str(playerNum) + ". " + str(name) + "```")
                        else:
                            mystring += (str(playerNum) + ". " + str(name) + "\n")

                    voteEmbed = discord.Embed(title="**" + selected[firstpick].display_name + "'s Pick**", colour=discord.Colour(0xd6fb7))
                    voteEmbed.set_thumbnail(url=thumbnail)
                    voteEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    voteEmbed.add_field(name="**Team 1:**", value="1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. " + removed4 + "\n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Team 2:**", value="1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Select:**", value=mystring)


                    await voteMessage.delete()
                    voteMessage = await channel.send(embed=voteEmbed)





                    currPos = 0

                    for name in availPlayers:
                        await voteMessage.add_reaction(emojiList[currPos])
                        currPos += 1

                elif captain == selected[firstpick].display_name and pickNum == 4:
                    pickNum = 5

                    team1.append(availPlayers[emojiList.index(reaction.emoji)])
                    await helperMsg.edit(content="**" + availPlayers[emojiList.index(reaction.emoji)] + " has been added to team 1.**" + "\n" + selected[secondpick].mention + " may now pick a player from the list below")
                    removed5 = availPlayers.pop(emojiList.index(reaction.emoji))


                    if selected[secondpick].avatar_url == "":
                        thumbnail = selected[secondpick].default_avatar_url
                    else:
                        thumbnail = selected[secondpick].avatar_url

                    for name in availPlayers:
                        playerNum += 1
                        if playerNum == 1:
                            mystring += ("```" + str(playerNum) + ". " + str(name) + "\n")

                        elif playerNum == len(availPlayers):
                            mystring += (str(playerNum) + ". " + str(name) + "```")
                        else:
                            mystring += (str(playerNum) + ". " + str(name) + "\n")

                    voteEmbed = discord.Embed(title="**" + selected[secondpick].display_name + "'s Pick**", colour=discord.Colour(0xcd2128))
                    voteEmbed.set_thumbnail(url=thumbnail)
                    voteEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    voteEmbed.add_field(name="**Team 1:**", value="1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. " + removed4 + "\n4. " + removed5 + "\n5.", inline=True)
                    voteEmbed.add_field(name="**Team 2:**", value="1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. \n5.", inline=True)
                    voteEmbed.add_field(name="**Select:**", value=mystring)


                    await voteMessage.delete()
                    voteMessage = await channel.send(embed=voteEmbed)





                    currPos = 0

                    for name in availPlayers:
                        await voteMessage.add_reaction(emojiList[currPos])
                        currPos += 1

                elif captain == selected[secondpick].display_name and pickNum == 5:
                    pickNum = 6

                    team2.append(availPlayers[emojiList.index(reaction.emoji)])
                    await helperMsg.edit(content="**" + availPlayers[emojiList.index(reaction.emoji)] + " has been added to team 2.**" + "\n" + selected[secondpick].mention + " may now pick another player from the list below")
                    removed6 = availPlayers.pop(emojiList.index(reaction.emoji))


                    if selected[secondpick].avatar_url == "":
                        thumbnail = selected[secondpick].default_avatar_url
                    else:
                        thumbnail = selected[secondpick].avatar_url

                    for name in availPlayers:
                        playerNum += 1
                        if playerNum == 1:
                            mystring += ("```" + str(playerNum) + ". " + str(name) + "\n")

                        elif playerNum == len(availPlayers):
                            mystring += (str(playerNum) + ". " + str(name) + "```")
                        else:
                            mystring += (str(playerNum) + ". " + str(name) + "\n")

                    voteEmbed = discord.Embed(title="**" + selected[secondpick].display_name + "'s Pick**", colour=discord.Colour(0xcd2128))
                    voteEmbed.set_thumbnail(url=thumbnail)
                    voteEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    voteEmbed.add_field(name="**Team 1:**", value="1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. " + removed4 + "\n4. " + removed5 + "\n5.", inline=True)
                    voteEmbed.add_field(name="**Team 2:**", value="1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. " + removed6 + "\n5.", inline=True)
                    voteEmbed.add_field(name="**Select:**", value=mystring)


                    await voteMessage.delete()
                    voteMessage = await channel.send(embed=voteEmbed)





                    currPos = 0

                    for name in availPlayers:
                        await voteMessage.add_reaction(emojiList[currPos])
                        currPos += 1

                elif captain == selected[secondpick].display_name and pickNum == 6:
                    pickNum = 0


                    team2.append(availPlayers[emojiList.index(reaction.emoji)])
                    removed7 = availPlayers.pop(emojiList.index(reaction.emoji))

                    team1.append(availPlayers[0])
                    await helperMsg.delete()
                    await linerMsg.delete()
                    removed8 = availPlayers.pop(0)

                    teamEmbed = discord.Embed(title="**TEAMS:**", colour=discord.Colour(0x00FF00))
                    teamEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                    teamEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    teamEmbed.add_field(name="**Team 1:**", value="```1. " + selected[firstpick].display_name + " (captain)\n2. " + removed1 + "\n3. " + removed4 + "\n4. " + removed5 + "\n5. " + removed8 + "```", inline=False)
                    teamEmbed.add_field(name="**Team 2:**", value="```1. " + selected[secondpick].display_name + " (captain)\n2. " + removed2 + "\n3. " + removed3 + "\n4. " + removed6 + "\n5. " + removed7 + "```", inline=False)
                    teamEmbed.add_field(name="\u200b\n<:csgo:778647766531833867> Go to map selection for CS:GO.", value="\u200b", inline=False)
                    teamEmbed.add_field(name="\u200b\n<:valorant:778647763411533846> Go to map selection for Valorant.", value="\u200b​", inline=False)


                    await voteMessage.delete()
                    teamMessage = await channel.send(embed=teamEmbed)
                    await teamMessage.add_reaction('<:csgo:778647766531833867>')
                    await teamMessage.add_reaction('<:valorant:778647763411533846>')

                else:
                    return
            elif teamMessage != None and teamMessage.id == reaction.message.id:
                
                if str(reaction.emoji) == '<:csgo:778647766531833867>':
                    valorant = False
                    mapString = ""
                    availMaps = ["Cache", "Dust II", "Inferno", "Mirage", "Nuke", "Overpass", "Train"]
                    mapNum = 0
                    for map in availMaps:
                        mapNum += 1
                        if mapNum == 1:
                            mapString += ("```" + str(mapNum) + ". " + str(map) + "\n")
                        elif mapNum == len(availMaps):
                            mapString += (str(mapNum) + ". " + str(map) + "```")
                        else:
                            mapString += (str(mapNum) + ". " + str(map) + "\n")

                    mapEmbed = discord.Embed(colour=discord.Colour(0xff00))

                    mapEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                    mapEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    mapEmbed.add_field(name="Maps:", value=mapString)
                    mapEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)

                    await teamMessage.delete()
                    mapMsg = await channel.send(selected[firstpick].mention + " may now ban a map.", embed=mapEmbed)

                    currPos = 0
                    for map in availMaps:
                        await mapMsg.add_reaction(emojiList[currPos])
                        currPos += 1
                    await mapMsg.add_reaction("🔀")

                elif str(reaction.emoji) == '<:valorant:778647763411533846>':
                    valorant = True
                    mapString = ""
                    availMaps = ["Ascent", "Bind", "Haven", "Split", "Icebox"]
                    mapNum = 0
                    for map in availMaps:
                        mapNum += 1
                        if mapNum == 1:
                            mapString += ("```" + str(mapNum) + ". " + str(map) + "\n")
                        elif mapNum == len(availMaps):
                            mapString += (str(mapNum) + ". " + str(map) + "```")
                        else:
                            mapString += (str(mapNum) + ". " + str(map) + "\n")

                    mapEmbed = discord.Embed(colour=discord.Colour(0xff00))

                    mapEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                    mapEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                    mapEmbed.add_field(name="Maps:", value=mapString)
                    mapEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)

                    await teamMessage.delete()
                    mapMsg = await channel.send(selected[firstpick].mention + " may now ban a map.", embed=mapEmbed)

                    currPos = 0
                    for map in availMaps:
                        await mapMsg.add_reaction(emojiList[currPos])
                        currPos += 1
                    await mapMsg.add_reaction("🔀")

                elif reaction.emoji == "🔀":
                    reacted = await reaction.users().flatten()
                    if selected[firstpick] in reacted and selected[secondpick] not in reacted:
                        await channel.send(selected[secondpick].mention + ", " + selected[firstpick].display_name + " voted for random map selection. Click 🔀 to choose a random map.")
                    elif selected[secondpick] in reacted and selected[firstpick] not in reacted:
                        await channel.send(selected[firstpick].mention + ", " + selected[secondpick].display_name + " voted for random map selection. Click 🔀 to choose a random map.")
                    elif selected[firstpick] and selected[secondpick] in reacted:
                        msgList = []
                        async for message in channel.history(limit=50):
                            if message.author.id == bot.user.id:
                                msgList.append(message)
                        if len(msgList) == 1:
                            await msgList[0].delete()
                        else:
                            await channel.delete_messages(msgList)
                        msgList = []
                        async for message in channel.history(limit=50):
                            if message.author.id == bot.user.id:
                                msgList.append(message)
                        if len(msgList) == 1:
                            await msgList[0].delete()
                        elif len(msgList) > 1:
                            await channel.delete_messages(msgList)
                        elif valorant == False:
                            availMaps = ["Cache", "Dust II", "Inferno", "Mirage", "Nuke", "Overpass", "Train"]
                            selectedMap = random.choice(availMaps)

                            imageUrl = ""

                            if selectedMap == "Cache":
                                imageUrl = "https://i.imgur.com/ChQQJVj.jpg"
                            elif selectedMap == "Dust II":
                                imageUrl = "https://i.imgur.com/eS7pJ6N.jpg"
                            elif selectedMap == "Inferno":
                                imageUrl = "https://i.imgur.com/ZqQyY4Q.jpg"
                            elif selectedMap == "Mirage":
                                imageUrl = "https://i.imgur.com/MZj4xf9.jpg"
                            elif selectedMap == "Nuke":
                                imageUrl = "https://i.imgur.com/Hci0buQ.jpg"
                            elif selectedMap == "Overpass":
                                imageUrl = "https://i.imgur.com/hLtArFQ.jpg"
                            else:
                                imageUrl = "https://i.imgur.com/idfdTIy.jpg"

                            teamEmbed = discord.Embed(title="**TEAMS:**", colour=discord.Colour(0x00FF00))
                            teamEmbed.set_image(url=imageUrl)
                            teamEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                            teamEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                            teamEmbed.add_field(name="**Team 1:**", value="```1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. " + removed4 + "\n4. " + removed5 + "\n5. " + removed8 + "```", inline=True)
                            teamEmbed.add_field(name="**Team 2:**", value="```1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. " + removed6 + "\n5. " + removed7 + "```", inline=True)
                            teamEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)
                            teamEmbed.add_field(name="**Map: **" + selectedMap, value="\u200b")

                            teamMessage = await channel.send(embed=teamEmbed)
                            await teamMessage.add_reaction("🔀")
                        else:
                            availMaps = ["Ascent", "Bind", "Haven", "Split", "Icebox"]
                            selectedMap = random.choice(availMaps)

                            imageUrl = ""

                            if selectedMap == "Ascent":
                                imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/e/e7/Loading_Screen_Ascent.png"
                            elif selectedMap == "Bind":
                                imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/2/23/Loading_Screen_Bind.png"
                            elif selectedMap == "Haven":
                                imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/7/70/Loading_Screen_Haven.png"
                            elif selectedMap == "Split":
                                imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/d/d6/Loading_Screen_Split.png"
                            else:
                                imageUrl = "https://static.wikia.nocookie.net/valorant/images/3/34/Loading_Icebox.png"

                            teamEmbed = discord.Embed(title="**TEAMS:**", colour=discord.Colour(0x00FF00))
                            teamEmbed.set_image(url=imageUrl)
                            teamEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                            teamEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                            teamEmbed.add_field(name="**Team 1:**", value="```1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. " + removed4 + "\n4. " + removed5 + "\n5. " + removed8 + "```", inline=True)
                            teamEmbed.add_field(name="**Team 2:**", value="```1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. " + removed6 + "\n5. " + removed7 + "```", inline=True)
                            teamEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)
                            teamEmbed.add_field(name="**Map: **" + selectedMap, value="\u200b")

                            teamMessage = await channel.send(embed=teamEmbed)
                            await teamMessage.add_reaction("🔀")
            elif mapMsg != None and mapMsg.id == reaction.message.id:
                if reaction.emoji == "🔀":
                    reacted = await reaction.users().flatten()
                    if selected[firstpick] in reacted and selected[secondpick] not in reacted:
                        firstVoteMsg = await channel.send(selected[secondpick].mention + ", " + selected[firstpick].display_name + " voted for random map selection. Click 🔀 to choose a random map.")
                    elif selected[secondpick] in reacted and selected[firstpick] not in reacted:
                        secondVoteMsg = await channel.send(selected[firstpick].mention + ", " + selected[secondpick].display_name + " voted for random map selection. Click 🔀 to choose a random map.")
                    elif selected[firstpick] and selected[secondpick] in reacted:
                        msgList = []
                        async for message in channel.history(limit=50):
                            if message.author.id == bot.user.id:
                                msgList.append(message)
                        if len(msgList) == 1:
                            await msgList[0].delete()
                        else:
                            await channel.delete_messages(msgList)
                        msgList = []
                        async for message in channel.history(limit=50):
                            if message.author.id == bot.user.id:
                                msgList.append(message)
                        if len(msgList) == 1:
                            await msgList[0].delete()
                        elif len(msgList) > 1:
                            await channel.delete_messages(msgList)
                        elif valorant == False:
                            availMaps = ["Cache", "Dust II", "Inferno", "Mirage", "Nuke", "Overpass", "Train"]
                            selectedMap = random.choice(availMaps)

                            imageUrl = ""

                            if selectedMap == "Cache":
                                imageUrl = "https://i.imgur.com/ChQQJVj.jpg"
                            elif selectedMap == "Dust II":
                                imageUrl = "https://i.imgur.com/eS7pJ6N.jpg"
                            elif selectedMap == "Inferno":
                                imageUrl = "https://i.imgur.com/ZqQyY4Q.jpg"
                            elif selectedMap == "Mirage":
                                imageUrl = "https://i.imgur.com/MZj4xf9.jpg"
                            elif selectedMap == "Nuke":
                                imageUrl = "https://i.imgur.com/Hci0buQ.jpg"
                            elif selectedMap == "Overpass":
                                imageUrl = "https://i.imgur.com/hLtArFQ.jpg"
                            else:
                                imageUrl = "https://i.imgur.com/idfdTIy.jpg"

                            teamEmbed = discord.Embed(title="**TEAMS:**", colour=discord.Colour(0x00FF00))
                            teamEmbed.set_image(url=imageUrl)
                            teamEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                            teamEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                            teamEmbed.add_field(name="**Team 1:**", value="```1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. " + removed4 + "\n4. " + removed5 + "\n5. " + removed8 + "```", inline=True)
                            teamEmbed.add_field(name="**Team 2:**", value="```1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. " + removed6 + "\n5. " + removed7 + "```", inline=True)
                            teamEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)
                            teamEmbed.add_field(name="**Map: **" + selectedMap, value="\u200b")

                            teamMessage = await channel.send(embed=teamEmbed)
                            await teamMessage.add_reaction("🔀")
                        else:
                            availMaps = ["Ascent", "Bind", "Haven", "Split", "Icebox"]
                            selectedMap = random.choice(availMaps)

                            imageUrl = ""

                            if selectedMap == "Ascent":
                                imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/e/e7/Loading_Screen_Ascent.png"
                            elif selectedMap == "Bind":
                                imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/2/23/Loading_Screen_Bind.png"
                            elif selectedMap == "Haven":
                                imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/7/70/Loading_Screen_Haven.png"
                            elif selectedMap == "Split":
                                imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/d/d6/Loading_Screen_Split.png"
                            else:
                                imageUrl = "https://static.wikia.nocookie.net/valorant/images/3/34/Loading_Icebox.png"

                            teamEmbed = discord.Embed(title="**TEAMS:**", colour=discord.Colour(0x00FF00))
                            teamEmbed.set_image(url=imageUrl)
                            teamEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                            teamEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                            teamEmbed.add_field(name="**Team 1:**", value="```1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. " + removed4 + "\n4. " + removed5 + "\n5. " + removed8 + "```", inline=True)
                            teamEmbed.add_field(name="**Team 2:**", value="```1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. " + removed6 + "\n5. " + removed7 + "```", inline=True)
                            teamEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)
                            teamEmbed.add_field(name="**Map: **" + selectedMap, value="\u200b")

                            teamMessage = await channel.send(embed=teamEmbed)
                            await teamMessage.add_reaction("🔀")


                elif reaction.emoji in emojiList:
                    if captain == selected[firstpick].display_name and pickNum == 0:
                        pickNum = 1
                        availMaps.pop(emojiList.index(reaction.emoji))

                        mapString = ""
                        mapNum = 0
                        for map in availMaps:
                            mapNum += 1
                            if mapNum == 1:
                                mapString += ("```" + str(mapNum) + ". " + str(map) + "\n")
                            elif mapNum == len(availMaps):
                                mapString += (str(mapNum) + ". " + str(map) + "```")
                            else:
                                mapString += (str(mapNum) + ". " + str(map) + "\n")

                        mapEmbed = discord.Embed(colour=discord.Colour(0xff00))

                        mapEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                        mapEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                        mapEmbed.add_field(name="Maps:", value=mapString)
                        mapEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)

                        await mapMsg.delete()
                        mapMsg = await channel.send(selected[secondpick].mention + " may now ban a map.", embed=mapEmbed)

                        currPos = 0
                        for map in availMaps:
                            await mapMsg.add_reaction(emojiList[currPos])
                            currPos += 1
                        await mapMsg.add_reaction("🔀")

                    elif captain == selected[secondpick].display_name and pickNum == 1:
                        pickNum = 2
                        availMaps.pop(emojiList.index(reaction.emoji))

                        mapString = ""
                        mapNum = 0
                        for map in availMaps:
                            mapNum += 1
                            if mapNum == 1:
                                mapString += ("```" + str(mapNum) + ". " + str(map) + "\n")
                            elif mapNum == len(availMaps):
                                mapString += (str(mapNum) + ". " + str(map) + "```")
                            else:
                                mapString += (str(mapNum) + ". " + str(map) + "\n")

                        mapEmbed = discord.Embed(colour=discord.Colour(0xff00))

                        mapEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                        mapEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                        mapEmbed.add_field(name="Maps:", value=mapString)
                        mapEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)

                        await mapMsg.delete()
                        mapMsg = await channel.send(selected[firstpick].mention + " may now ban a map.", embed=mapEmbed)

                        currPos = 0
                        for map in availMaps:
                            await mapMsg.add_reaction(emojiList[currPos])
                            currPos += 1
                        await mapMsg.add_reaction("🔀")

                    elif captain == selected[firstpick].display_name and pickNum == 2:
                        pickNum = 3
                        availMaps.pop(emojiList.index(reaction.emoji))

                        mapString = ""
                        mapNum = 0
                        for map in availMaps:
                            mapNum += 1
                            if mapNum == 1:
                                mapString += ("```" + str(mapNum) + ". " + str(map) + "\n")
                            elif mapNum == len(availMaps):
                                mapString += (str(mapNum) + ". " + str(map) + "```")
                            else:
                                mapString += (str(mapNum) + ". " + str(map) + "\n")

                        mapEmbed = discord.Embed(colour=discord.Colour(0xff00))

                        mapEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                        mapEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                        mapEmbed.add_field(name="Maps:", value=mapString)
                        mapEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)

                        await mapMsg.delete()
                        mapMsg = await channel.send(selected[secondpick].mention + " may now ban a map.", embed=mapEmbed)

                        currPos = 0
                        for map in availMaps:
                            await mapMsg.add_reaction(emojiList[currPos])
                            currPos += 1
                        await mapMsg.add_reaction("🔀") 
                        
                    elif captain == selected[secondpick].display_name and pickNum == 3 and valorant == False:
                        pickNum = 4
                        availMaps.pop(emojiList.index(reaction.emoji))

                        mapString = ""
                        mapNum = 0
                        for map in availMaps:
                            mapNum += 1
                            if mapNum == 1:
                                mapString += ("```" + str(mapNum) + ". " + str(map) + "\n")
                            elif mapNum == len(availMaps):
                                mapString += (str(mapNum) + ". " + str(map) + "```")
                            else:
                                mapString += (str(mapNum) + ". " + str(map) + "\n")

                        mapEmbed = discord.Embed(colour=discord.Colour(0xff00))

                        mapEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                        mapEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                        mapEmbed.add_field(name="Maps:", value=mapString)
                        mapEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)

                        await mapMsg.delete()
                        mapMsg = await channel.send(selected[firstpick].mention + " may now ban a map.", embed=mapEmbed)

                        currPos = 0
                        for map in availMaps:
                            await mapMsg.add_reaction(emojiList[currPos])
                            currPos += 1
                        await mapMsg.add_reaction("🔀")

                    elif captain == selected[secondpick].display_name and pickNum == 3 and valorant == True:
                        picknum = 6
                        availMaps.pop(emojiList.index(reaction.emoji))
                        imageUrl = ""
                        "Ascent", "Bind", "Haven", "Split"


                        if availMaps[0] == "Ascent":
                            imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/e/e7/Loading_Screen_Ascent.png"
                        elif availMaps[0] == "Bind":
                            imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/2/23/Loading_Screen_Bind.png"
                        elif availMaps[0] == "Haven":
                            imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/7/70/Loading_Screen_Haven.png"
                        elif availMaps[0] == "Split":
                            imageUrl = "https://vignette.wikia.nocookie.net/valorant/images/d/d6/Loading_Screen_Split.png"
                        else:
                            imageUrl = "https://static.wikia.nocookie.net/valorant/images/3/34/Loading_Icebox.png"

                        teamEmbed = discord.Embed(title="**TEAMS:**", colour=discord.Colour(0x00FF00))
                        teamEmbed.set_image(url=imageUrl)
                        teamEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                        teamEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                        teamEmbed.add_field(name="**Team 1:**", value="```1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. " + removed4 + "\n4. " + removed5 + "\n5. " + removed8 + "```", inline=True)
                        teamEmbed.add_field(name="**Team 2:**", value="```1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. " + removed6 + "\n5. " + removed7 + "```", inline=True)
                        teamEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)
                        teamEmbed.add_field(name="**Map: **" + availMaps[0], value="\u200b")



                        await mapMsg.delete()
                        teamMessage = await channel.send(embed=teamEmbed)
                        await teamMessage.add_reaction("🔀")

                    elif captain == selected[firstpick].display_name and pickNum == 4:
                        pickNum = 5
                        availMaps.pop(emojiList.index(reaction.emoji))

                        mapString = ""
                        mapNum = 0
                        for map in availMaps:
                            mapNum += 1
                            if mapNum == 1:
                                mapString += ("```" + str(mapNum) + ". " + str(map) + "\n")
                            elif mapNum == len(availMaps):
                                mapString += (str(mapNum) + ". " + str(map) + "```")
                            else:
                                mapString += (str(mapNum) + ". " + str(map) + "\n")

                        mapEmbed = discord.Embed(colour=discord.Colour(0xff00))

                        mapEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                        mapEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                        mapEmbed.add_field(name="Maps:", value=mapString)
                        mapEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)

                        await mapMsg.delete()
                        mapMsg = await channel.send(selected[secondpick].mention + " may now ban a map.", embed=mapEmbed)

                        currPos = 0
                        for map in availMaps:
                            await mapMsg.add_reaction(emojiList[currPos])
                            currPos += 1
                        await mapMsg.add_reaction("🔀")

                    elif captain == selected[secondpick].display_name and pickNum == 5:
                        picknum = 6
                        availMaps.pop(emojiList.index(reaction.emoji))
                        imageUrl = ""


                        if availMaps[0] == "Cache":
                            imageUrl = "https://i.imgur.com/ChQQJVj.jpg"
                        elif availMaps[0] == "Dust II":
                            imageUrl = "https://i.imgur.com/eS7pJ6N.jpg"
                        elif availMaps[0] == "Inferno":
                            imageUrl = "https://i.imgur.com/ZqQyY4Q.jpg"
                        elif availMaps[0] == "Mirage":
                            imageUrl = "https://i.imgur.com/MZj4xf9.jpg"
                        elif availMaps[0] == "Nuke":
                            imageUrl = "https://i.imgur.com/Hci0buQ.jpg"
                        elif availMaps[0] == "Overpass":
                            imageUrl = "https://i.imgur.com/hLtArFQ.jpg"
                        else:
                            imageUrl = "https://i.imgur.com/idfdTIy.jpg"

                        teamEmbed = discord.Embed(title="**TEAMS:**", colour=discord.Colour(0x00FF00))
                        teamEmbed.set_image(url=imageUrl)
                        teamEmbed.set_thumbnail(url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")
                        teamEmbed.set_author(name="10 Man Teams", icon_url="https://yt3.ggpht.com/a-/AAuE7mCbx9Cm6M2EeiUGg-ggbRMXD_PIL0ZC2rHIKg=s900-mo-c-c0xffffffff-rj-k-no")

                        teamEmbed.add_field(name="**Team 1:**", value="```1. " + selected[firstpick].display_name + " (captain) \n2. " + removed1 + "\n3. " + removed4 + "\n4. " + removed5 + "\n5. " + removed8 + "```", inline=True)
                        teamEmbed.add_field(name="**Team 2:**", value="```1. " + selected[secondpick].display_name + " (captain) \n2. " + removed2 + "\n3. " + removed3 + "\n4. " + removed6 + "\n5. " + removed7 + "```", inline=True)
                        teamEmbed.add_field(name="\u200b\n🔀: Randomly select a map", value="\u200b​", inline=False)
                        teamEmbed.add_field(name="**Map: **" + availMaps[0], value="\u200b")

                        await mapMsg.delete()
                        teamMessage = await channel.send(embed=teamEmbed)
                        await teamMessage.add_reaction("🔀")
                else:
                    return

@bot.command(pass_context = True)
async def teamrandom(ctx):

    global team1
    global team2
    global nameList

    if started == True:
        for name in nameList:
            picked1 = random.choice(nameList)
            team1.append(picked1)
            nameList.remove(picked1)
            picked2 = random.choice(nameList)
            team2.append(picked2)
            nameList.remove(picked2)

        picked1 = random.choice(nameList)
        team1.append(picked1)
        nameList.remove(picked1)
        picked2 = random.choice(nameList)
        team2.append(picked2)
        nameList.remove(picked2)

        t1string = ""
        t2string = ""
        t1num = 0
        t2num = 0

        team1chan = discord.utils.get(ctx.message.guild.channels, name = 'team 1')
        team2chan = discord.utils.get(ctx.message.guild.channels, name = 'team 2')

        for t1 in team1:
            t1num += 1
            if t1num == 1:
                 t1string += ("**TEAM 1:**\n```" + str(t1num) + ". " + str(t1) + "\n")

            elif t1num == 5:
                    t1string += (str(t1num) + ". " + str(t1) + "```")

            else:
                    t1string += (str(t1num) + ". " + str(t1) + "\n")


        for t2 in team2:
            t2num += 1
            if t2num == 1:
                t2string += ("**TEAM 2:**\n```" + str(t2num) + ". " + str(t2) + "\n")

            elif t2num == 5:
                t2string += (str(t2num) + ". " + str(t2) + "```")

            else:
                 t2string += (str(t2num) + ". " + str(t2) + "\n")

        await ctx.send (t1string)
        await ctx.send (t2string)

    else:
        await ctx.send("You haven't started a 10 Man yet, use .new to start one!")

with open("token.txt", "r") as file:
    for line in file:
        if line.startswith("Your Discord Token"):
            token = line.split('=')[1].strip().strip("'")
            break
    else:
        print("Token not found in token.txt. Please make sure the file is formatted correctly.")
        exit()

bot.run(token)
