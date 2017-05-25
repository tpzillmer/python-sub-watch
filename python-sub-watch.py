import praw
import smtplib
import threading
import sys

reddit = praw.Reddit(client_id='KxlxBCK7CFy1TQ',
                     client_secret=None,
                     user_agent='email_notification')

def watchSubforKey(subreddit, keyList):
    currentTitle = ''
    while(True):
        for entry in subreddit:
            title = entry.title.lower()
            if title != currentTitle:
                currentTitle = title
                for keyword in keyList:
                    if keyword.lower() in title:
                        try:
                            message = "A mention of {} has been posted in /r/{}.".format(keyword, sub)
                            smtp_gmail(username, secondUsername, password, message)
                        except smtplib.SMTPAuthenticationError:
                            print("Incorrect username or password for Gmail, or use fot less secure apps is not turned on in Gmail.")
                            sys.exit()

def smtp_gmail(username, secondUsername, password, message):
    smtp_server = "smtp.gmail.com:587"
    server = smtplib.SMTP(smtp_server)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, secondUsername, message)
    server.quit()

def getKeyList():
    keyList = []
    key = input("Enter a keyword or phrase you would like to watch for in {}: ".format(sub))
    while(len(key) == 0):
            print("Please do not enter nothing.")
            key = input("Enter a keyword or phrase you would like to watch for in {}: ".format(sub))
    keyList.append(key)

    key = ''
    while(key.lower() != 'stop'):
        key = input('Enter an additional keyword or phrase you would like to watch for in {}, otherwise enter "stop": '.format(sub))
        while(len(key) == 0):
            print("Please do not enter nothing.")
            key = input('Enter an additional keyword or phrase you would like to watch for in {}, otherwise enter "stop": '.format(sub))
        if(key.lower()!='no'): keyList.append(key)
            
    return keyList


    

if __name__ == "__main__":
    print('It is reccomended to make a dummy Gmail account for to log in and send in this application. You can use your official email to receive notifications.'
          ' Remember to turn on the "Use for less secure apps" functionality in the Gmail account.\n')
    
    username = input("Please enter your Gmail's username: ")
    while(1):
        if('gmail.com' in username): break
        else: print('Please enter a valid gmail address, including "@gmail.com"')
            
    while(1):
        password = input("Please enter your Gmail's password: ")
        if(len(password) > 0): break
        else: print('Please enter a valid password')

    secondUsername = input('If you would like to be notified using the same email, enter "same". Otherwise enter a new email: ')
    while(1):
        if(secondUsername.lower() == 'same'):
            secondUsername = username
            break
        if(len(secondUsername) == 0) or ('.com' not in secondUsername and '@' not in secondUsername):
            secondUsername = input('Please enter a valid email address or enter "same" to use the same email: ')
        else:
            break

    while(1):
        try:
            sub = input("Enter a subreddit you would like to watch: ")
            subreddit = reddit.subreddit(sub).new(limit=1)
            #for i in subreddit: pass
            break
        except: print("You entered an invalid subreddit.")
    
    keyList = getKeyList()
        
    threading.Thread(target=watchSubforKey, args=[subreddit, keyList]).start()

    while(1):
        while(1):
            sub = input('Enter an additional subreddit you would like to watch, otherwise enter "stop": ')
            if sub == 'stop': sys.exit()
            try:
                subreddit = reddit.subreddit(sub).new(limit=1)
                #for i in subreddit: pass
            except: print("You entered an invalid subreddit.")
                
        keyList = getKeyList()
        threading.Thread(target=watchSubforKey, args=[subreddit, keyList]).start()
