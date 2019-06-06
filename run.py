import subprocess
import os

cmd2="scrapy crawl announcement"
cmd5="scrapy crawl newlisting"
os.chdir("getann/")
val2=subprocess.call(cmd2,shell=True)
os.chdir("../")
os.chdir("compup/")
val5=subprocess.call(cmd5,shell=True)