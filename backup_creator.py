# Simply run to create an instant backup of code @ that time.


from datetime import datetime

gf = open('botbackup.txt', 'a', encoding='utf-8')

time = datetime.now()
t = time.strftime("%A, %B %d, 20%y - %X")

gf.write("\n" "--------------------------------------------" + "\n" + str(t) + "\nTWEEPY_STREAMER BACKUP" + "\n\n")
with open("tweepy_streamer.py", 'r') as tp:
    for line in tp:
        gf.write(line)

gf.write("\n\nTXT_ANALYSIS" + "\n" "--------------------------------------------" + "\n\n")
with open("txt_analysis.py", 'r') as ta:
    for line in ta:
        gf.write(line)

