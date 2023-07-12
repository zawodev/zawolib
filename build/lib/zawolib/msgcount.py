"""  Liczenie wiadomosci poszczegolnych uzytkownikow serwera i sortowanie eleganckie tego rankingu  """
import os
import discord
import progressbar
from datetime import datetime
clear = lambda: os.system('cls')

msgDist = None
messagesCountDict = {} #ile kto ma wiadomosci dictionary par goscia i jego ilosci ([zawo, 3]; [kamil, 2]) itd
avatars = {}
guild = None
percentMsg = None

async def downloadChannelHistory(channel):
    filename = f"{channel.name}.txt"
    maxcount = 99221
    currencount = 0
    with open(filename, "w", encoding="utf-8") as file:
        async for msg in channel.history(limit=None):
            currencount += 1
            clear()
            file.write(f"{msg.author.name}#{msg.clean_content}\n") 
            print(f"{currencount}/{maxcount}\n{currencount*100.0/maxcount}%\n")


async def downloadUserMessagesCount():
    print()


async def downloadServerMessagesCount(bot, ctx, msg, _msgDist = 969, adminOutput = False, guildid = None, adminNumsInterval = None, adminBeforeTime = "now"): #on a whole server | 11/02/22 16:06:35 = 11 luty 2022 16:06:35
    global messagesCountDict
    global guild
    global msgDist
    global percentMsg

    with open("numsinterval.txt", "w", encoding="utf-8") as file:
        file.write("\n")

    if guildid == None: guildid = ctx.guild.id    
    guild = bot.get_guild(int(guildid))

    msgDist = _msgDist

    percentMsg = msg
    msgCount = 0
    maxCount = 0

    messagesCountDict = {}

    messages = []
    messagesChannelsList = []
    channelList = []
    #for server in bot.guilds:
    for channel in guild.channels:
        if str(channel.type) == 'text':
            channelList.append(channel)

    channelMax = len(channelList)

    #percentMsg = await ctx.channel.send(f"`rozpoczynam pobieranie wiadomości na serwerze: {guild.name}\nproszę czekać...`")
    await percentMsg.edit(content=f"`rozpoczynam pobieranie wiadomości na serwerze: {guild.name}\nproszę czekać...`")

    channelCount = 0
    for channel in channelList:
        channelCount += 1

        if(percentMsg != None and ctx != None): await percentMsg.edit(content=f"`ładowanie wiadomości na serwerze: {guild.name}\nwiadomosc: {maxCount}, kanał: {channel} {channelCount}/{channelMax}`")
        print(f"wiadomosc: {maxCount}, {channelCount}/{channelMax}, {channel}")

        if adminBeforeTime != "now": messagesList = await channel.history(limit=None, before=datetime.strptime(adminBeforeTime,"%d/%m/%y %H:%M:%S")).flatten()
        else: messagesList = await channel.history(limit=None).flatten()

        messages.extend(messagesList)
        maxCount += len(messagesList)

        #messagesChannelsList.append(messagesList)
        #if(ctx != None): await ctx.channel.send(f"maxCount: {maxCount}, {channelCount}/{channelMax}, {channel}")

    """ OLD METHOD 

    channelCount = 0
    for messagesList in messagesChannelsList:
        messagesList.reverse()
        channelCount += 1
        for msg in messagesList:
            clear()
            print(messagesCountDict)
            print(f"wiadomosc: {msgCount}/{maxCount}, kanał: {channelCount}/{channelMax} {channelList[channelCount-1]}\n{msgCount*100.0/(maxCount)}%\n")
            if adminLimit == None:
                msgCount += 1
                await countNewMessage(bot, msg, percentMsg, msgCount, maxCount, channelCount, channelMax, channelList[channelCount-1])
            else:
                msgCount += 1
                if adminLimit > msgCount:
                    await countNewMessage(bot, msg, percentMsg, msgCount, maxCount, channelCount, channelMax, channelList[channelCount-1])
                else:
                    await writeOutMessagesCount(ctx, adminOutput, messagesCountDict, msgCount)
                    return
    """

    #sorted(messages, key=lambda x: x.created_at, reverse=False)
    messages.sort(key=lambda x: x.created_at, reverse=False)
    #messages.reverse()
    channelCount = 1
    adminIntervalIndex = 0
    for msg in messages:
        msgCount += 1
        await __countNewMessage(msg, msgCount, maxCount)
        if adminNumsInterval != None and adminOutput and (((msgCount - 1) % max(int(maxCount / adminNumsInterval), 1) == 0) or msgCount == maxCount):
            adminIntervalIndex = await __appendNumsInterval(adminIntervalIndex + 1, msg)

    await __writeOutMessagesCount(ctx, adminOutput, msgCount)

    if adminNumsInterval != None and adminOutput:
        await __writeOutNumsInterval(ctx=ctx)


async def __countNewMessage(msg, msgCount, maxCount):
    global messagesCountDict
    global percentMsg
    global guild
    global avatars
    global msgDist
    
    """ OLD
    #await bot.get_guild(870021183737823262).get_channel(1002292758582669392).send(msg.content)
    try: 
        member = guild.get_member(msg.author.id)
        memberName = str(member.display_name)
    except:
        memberName = "[user left the server]"
    """

    memberName = msg.author.name

    if(percentMsg != None and (msgCount % msgDist == 0 or msgCount == maxCount)):
        print(messagesCountDict)
        s = f"`przeliczanie wiadomości na serwerze: {guild.name}\nwiadomosc: {msgCount}/{maxCount}, {msgCount*100.0/(maxCount)}%\n{progressbar.progress_bar(value=msgCount, minvalue=0, maxvalue=maxCount, length=20)}`"
        print(s)
        await percentMsg.edit(content=s)
    if(memberName not in messagesCountDict): 
        messagesCountDict[memberName] = 1
        avatars[memberName] = msg.author.avatar_url
    else: messagesCountDict[memberName] += 1


async def __writeOutMessagesCount(ctx, adminOutput, msgCount):
    global avatars
    global messagesCountDict

    sortedMessagesByBest = sorted(messagesCountDict.items(), key=lambda x: x[1], reverse=True)
    sortedMessagesByDate = messagesCountDict.items()

    #returnmsg = "```\n" #old method
    returnmsg = ""
    returnnames = ""
    returnnames_bar = ""
    returnavatars = ""
    #with open(filename, "w", encoding="utf-8") as file:
    if adminOutput:
        for user in sortedMessagesByDate:
            returnmsg += f"{user[1]}\n"
            returnnames += f"{user[0]}\n"
            returnavatars += f"{avatars[user[0]]}\n"

    for user in sortedMessagesByBest:
        returnnames_bar += f"{progressbar.progress_bar(user[1], minvalue=0, maxvalue=msgCount, length=20)}{round(user[1]*100.0/msgCount, 2)}% ({user[1]}/{msgCount}) {user[0]}\n"
    
    #else:
        #for user in sortedMessagesByBest:
            #returnmsg += f"{user[0]} | {user[1]} | {user[1]*100.0/msgCount}%\n"

    #returnmsg += "```"
    #returnnames += "```"
    #returnnames_bar += "```"
    #returnavatars += "```"

    if(ctx != None):
        #await ctx.send(returnmsg)
        if adminOutput: 
            #await ctx.send(returnnames) #old method, dziala na krotsze
            with open("nums.txt", "w", encoding="utf-8") as file0:
                #file.write('arg1 = {0}, arg2 = {1}'.format(arg1, arg2))
                file0.write(returnmsg)
            with open("nums.txt", "rb") as file0:
                await ctx.send("Numerki:", file=discord.File(file0, "nums.txt"))


            with open("names.txt", "w", encoding="utf-8") as file1:
                file1.write(returnnames)
            with open("names.txt", "rb") as file1:
                await ctx.send("Nicknamy:", file=discord.File(file1, "names.txt"))
            

            with open("avatars.txt", "w", encoding="utf-8") as file2:
                file2.write(returnavatars)
            with open("avatars.txt", "rb") as file2:
                await ctx.send("Avatary:", file=discord.File(file2, "avatars.txt"))


            with open("result_bar.txt", "w", encoding="utf-8") as file3:
                file3.write(returnnames_bar)
            with open("result_bar.txt", "rb") as file3:
                await ctx.send("Tabelka:", file=discord.File(file3, "result_bar.txt"))

    else:
        #error pv
        print(1)


async def __appendNumsInterval(adminIntervalIndex, msg): #if adminOutput only
    global messagesCountDict
    sortedMessagesByDate = messagesCountDict.items()

    with open("numsinterval.txt", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        lines[0] = lines[0].strip() + f"\t{msg.created_at}\n"
        i = 1
        for user in sortedMessagesByDate:
            try: 
                lines[i] = lines[i].strip() + f"\t{user[1]}\n"
            except: 
                s = ""
                for j in range(0, adminIntervalIndex - 1): s += "0\t"
                lines.append(s + f"{user[1]}\n")
            i += 1

        file.seek(0)
        for line in lines:
            file.write(line)
    
    return adminIntervalIndex
    

async def __writeOutNumsInterval(ctx):
    if(ctx != None):
        with open("numsinterval.txt", "rb") as file:
            await ctx.send(":flushed:", file=discord.File(file, "numsinterval.txt"))




    #await percentMsg.edit(content=f"`wiadomosc: {msgCount}/{maxCount}, kanał: {channelCount}/{channelMax} {channel}\n{msgCount*100.0/(maxCount)}%\n`")

#display_name or name or nick in member
#only name in user
#async def countNewMessage(bot, msg, percentMsg, msgCount, maxCount, channelCount, channelMax, channel):