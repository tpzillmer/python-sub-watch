import praw
import smtplib

reddit = praw.Reddit(client_id='GWQCwKgHbzFZYw',
                     client_secret=None,
                     user_agent='test')

def watchSubforKey(sub, keyList):
    currentTitle = ''
    try:
        while(True):
            for submission in reddit.subreddit(sub).new(limit=1):
                title = submission.title
                if title != currentTitle:
                    currentTitle = title
                    for keyword in keyList:
                        if keyword in title:
                            try:
                                message = "A mention of {} has been posted in {}.".format(keyword, sub)
                                print(message)
                                smtp_gmail(username, password, message)
                            except smtplib.SMTPAuthenticationError:
                                print("Incorrect username or password for Gmail, or less secure apps must be turned off.")
                            
    except KeyboardInterrupt:
        print("Done watching")

def smtp_gmail(username, password, message):
    smtp_server = "smtp.gmail.com:587"
    email_body = message
    
    server = smtplib.SMTP(smtp_server)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, username, email_body)
    server.quit()
    

if __name__ == "__main__":
    keyList = []

    username = input("Please enter your gmail's username: ")
    password = input("Please enter your gmail's password: ")
    
    
    sub = input("Please enter a subreddit you would like to watch: ")
    key = input("Please enter a keyword you would like to watch for in {}: ".format(sub))
    keyList.append(key)
    
    while(key.lower() != 'no'):
        key = input('Would you like to watch for an additional keyword? If not, enter "no": ')
        if(key.lower()!='no'):
            keyList.append(key)

    watchSubforKey(sub, keyList)
