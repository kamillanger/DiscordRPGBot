import json
import discord
import os
from datetime import datetime, timedelta
from Functions import EmbedFunctions as ef


async def getQuestFinishTime(levelName):
    with open(f'Quests/{levelName}.json') as quest:
        questInfo = json.load(quest)

    questFinishTime = datetime.now() + timedelta(hours=int(questInfo['duration']))
    return questFinishTime


async def showQuestInformation():
    embed = discord.Embed(
        title="Available quests are:",
        color=0xf35ff0
    )

    for file in os.listdir("Quests"):
        with open(f'Quests/{file}') as quest:
            questInfo = json.load(quest)
            questDuration = str(questInfo['duration']) + " hours"
            await ef.addEmbedField(embed, "Name:", questInfo['name'], True)
            await ef.addEmbedField(embed, "Description:", questInfo['description'], True)
            await ef.addEmptyEmbedField(embed, True)
            await ef.addEmbedField(embed, "Duration:", questDuration, True)
            goldRewardInfo = str(questInfo['goldReward']['min']) + "-" + str(questInfo['goldReward']['max']) + " gold"
            await ef.addEmbedField(embed, "Gold reward:", goldRewardInfo, True)
            xpRewardInfo = str(questInfo['xpReward']) + "xp"
            await ef.addEmbedField(embed, "Experience reward:", xpRewardInfo, True)
            await ef.addEmptyEmbedField(embed, False)

    return embed


async def sendCharacterOnQuest(clientId, levelName):
    with open(f'characters/{clientId}.json') as char:
        characterData = json.load(char)

    temp = characterData['onQuest']
    characterData['onQuest'] = True

    questFinishTime = await getQuestFinishTime(levelName)
    characterData['questInfo'] = {
        "name": levelName,
        "finishTime": str(questFinishTime)
    }

    with open(f'characters/{clientId}.json', 'w') as char:
        json.dump(characterData, char)


async def checkIfQuestExists(levelName):
    return os.path.isfile(f'Quests/{levelName}.json')


async def showQuestRemainingTimeInfo(ctx, clientId):
    with open(f'characters/{clientId}.json') as char:
        characterData = json.load(char)

    finishTime = datetime.strptime(str(characterData['questInfo']['finishTime']), '%Y-%m-%d %H:%M:%S.%f')
    remainingTime = finishTime - datetime.now()
    timeToShow = remainingTime - timedelta(microseconds=remainingTime.microseconds)
    await ctx.send(f"Your character is still on a quest for additional: {str(timeToShow)}")