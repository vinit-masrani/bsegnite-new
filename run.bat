cd ..\Anaconda3\Scripts
call activate.bat
call activate bsegnite
cd ..\..\project\getann-postgresql
scrapy crawl announcement
cd ..\
cd compup-postgresql
scrapy crawl newlisting