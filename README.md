# attenix-update-hours
A scraper for the Attenix system that's in charge of updating hours to employees
It is written for python 2.7.8 and currently checked to be working on Mac (El Capitan - 10.11.5) but no real reason it shouldn't work on other versions

Installing
1. install chromedriver at ~/Documents using these references: https://sites.google.com/a/chromium.org/chromedriver/getting-started, https://sites.google.com/a/chromium.org/chromedriver/downloads
2. pip install requirements.txt

Running
1. import the Attenix_Api from attenix-scraper.py 
2. init the Attenix_Api
3. run the update_hours() method

f.e.
Attenix_Api(general_schedule_option_id='1111', user_credentials=[{'user':'bla.bla', 'password':'blabla', 'user_display_name':'164'}])
Where general_schedule_option_id is your company's code and user_credentials is a list of credentials for each user needed to update hours, the user_display_name could be anything that holds a unique value for searching for your user. it's best to supply the Attenix ID for that


