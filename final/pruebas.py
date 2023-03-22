import datetime, re

er = r'[A-J][0-9]$'
while True:
    msg1 = input()
    if re.match(er, msg1.upper()):
        print("BIEN")
    else:
        print("MAL")
        