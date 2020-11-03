from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACe8c7d80243dcb6af6d499504d2752671"
# Your Auth Token from twilio.com/console
auth_token  = "be6525b180c6b39f24497564910fad1d"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+16236282738", 
    from_="+12166165289",
    body=
    "Hey dude, thanks again for watching our house! " 
    "Friendly reminder: make sure the front, back and bedroom doors are locked before you go to bed. "
    "Make sure the cats have their one serving of food for the day and water, you know the drill. "
    "Mostly I just did this to see if I could get it work and to be annoying. "
    "This is a bot btw, created by Robert Raya. No need to reply to this number. Message scheduled to be sent October 9th through 10th. Go Suns!")

print(message.sid)