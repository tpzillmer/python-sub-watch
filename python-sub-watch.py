import praw
import smtplib
import threading
import sys

reddit = praw.Reddit(client_id='KxlxBCK7CFy1TQ', client_secret=None, user_agent='email_notification')

def watch_sub(sub, key_list):
    "Retrieves most recent postings in a subreddit and checks if they contain key "
    
    current_title = ''
    while (1):
        subreddit = reddit.subreddit(sub).new(limit=1)
        for entry in subreddit:
            title = entry.title
            if title != current_title:
                current_title = title
                for keyword in key_list:
                    if keyword.lower() in title.lower():
                        message = "'{}' has been posted in /r/{}.".format(title, sub)
                        smtp_gmail(email, message)
                            
def get_key_list(sub):
    "Obtains a list of keys from the user"
    key_list = []

    key = input("Enter a keyword or phrase you would like to be notified "
                "about in {}. If you would like to be notified for each post, enter "
                "'all': ".format(sub))

    while(len(key) == 0):
        print("Please do not enter nothing.")
        key = input("Enter a keyword or phrase you would like to be notified "
                        "about in {}. If you would like to be notified for each post, enter "
                        "'all': ".format(sub))
        
    if(key == 'all'):
        key_list.append('')
        print("reached")
        return key_list
    else: key_list.append(key)

    key = ''
    while(key.lower() != 'stop'):
        key = input("Enter an additional keyword or phrase you would like to notified "
                    "about in {}, otherwise enter 'stop': ".format(sub))
        while(len(key) == 0):
            print("Please do not enter nothing.")
            key = input("Enter an additional keyword or phrase you would like to notified "
                        "about in {}, otherwise enter 'stop': ".format(sub))
            
        if(key.lower()!='stop'): key_list.append(key)

    return key_list

def smtp_gmail(email, message):
    "Sends notification email using Gmail"
    
    smtp_server = "smtp.gmail.com:587"
    server = smtplib.SMTP(smtp_server)
    server.starttls()
    server.login("redditpythontest@gmail.com", "***PASSWORD***")
    server.sendmail("redditpythontest@gmail.com", email, message)
    server.quit()

def get_sub():
    "Obtains initial subreddit user wants to watch"
    do = 1
    while(do):
        sub = input("Enter a subreddit you would like to watch: ")
        subreddit = reddit.subreddit(sub).new(limit=1)
        try:
            for i in subreddit: do = 0
        except: print("You entered an invalid subreddit.")
    return sub

def get_additional_sub():
    "Obtains additional subreddits user wants to watch"
    do = 1
    while(do):
        sub = input("Enter an additional subreddit you would like to watch, "
                    "otherwise enter 'stop': ")
        if sub == 'stop': return 0
        subreddit = reddit.subreddit(sub).new(limit=1)
        try:
            for i in subreddit: do = 0
        except: print("You entered an invalid subreddit.")
    return sub

def get_email():
    "Obtain email the user wants to be notified by"
    while(1):
        email = input("Please enter an email you would like to be notified by: ")
        if('.com' not in email and '@' not in email):
            print("Please enter a valid email.")
        else:
            return email
    
if __name__ == "__main__":
    print("It is reccomended to make a dummy Gmail account for to log in and send in " 
            "this application. You can use your official email to receive notifications. "
            "Remember to turn on the 'Use for less secure apps' functionality in the Gmail "
            "account you want to send the notifications in.\n")
    
    email = get_email()
    
    init_sub = get_sub()
    init_key_list = get_key_list(init_sub)
    threading.Thread(target=watch_sub, args=[init_sub, init_key_list]).start()

    while(1):
        additional_sub = get_additional_sub()
        if(additional_sub):
            additional_key_list = get_key_list(additional_sub)
            threading.Thread(target=watch_sub, args=[additional_sub, additional_key_list]).start()
        else: sys.exit()

