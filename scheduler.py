"""
Made with love to steal all the bumps
from everyone Mitsuha's discord :D
"""

import requests
import sys
import schedule
import time as time_module

token = open("token.txt", "r").read().strip()

def getUserDMChannel(userID):
    post_header = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    r = requests.post(
        f"https://discord.com/api/v9/users/@me/channels",
        json={"recipients": [userID]},
        headers=post_header
    ).json()
    return r['id']

def sendChannelMessage(channelID, message):
    post_header = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    r = requests.post(
        f"https://discord.com/api/v9/channels/{channelID}/messages",
        json={
            "content": message,
            "tts": False
        },
        headers=post_header
    )
    print("Message sent !")

def sendUserMessage(userID, msg):
    channel_id = getUserDMChannel(userID)
    sendChannelMessage(channel_id, msg)

def main():
    if len(sys.argv) < 2:
        print("Please specify a target type")
        return

    if sys.argv[1].lower() == "channel":
        #py program channel id test
        if len(sys.argv) == 2:
            print("You need to specify the channel ID !")
            return
        if len(sys.argv) == 3:
            print("Please specify a time to send the message !")
            return
        if len(sys.argv) == 4:
            print("Please specify a message to send !")
            return
        channelID = sys.argv[2]
        time = sys.argv[3]
        message = ' '.join(sys.argv[4::])
        schedule.every().day.at(time).do(sendChannelMessage, channelID, message)
        print("Message scheduled !")
    elif sys.argv[1].lower() == "user":
        #py prog user id message
        if len(sys.argv) == 2:
            print("You need to specify the user's ID !")
            return
        if len(sys.argv) == 3:
            print("Please specify a time to send the message !")
            return
        if len(sys.argv) == 4:
            print("Please specify a message to send !")
            return
        userID = sys.argv[2]
        time = sys.argv[3]
        message = ' '.join(sys.argv[4::])
        schedule.every().day.at(time).do(sendUserMessage, userID, message)
        print("Message scheduled !")
    else:
        print("Unknown target type ! Correct types are : ")
        print("- channel")
        print("- user")

    while True:
        schedule.run_pending()
        time_module.sleep(1)

if __name__ == "__main__":
    main()