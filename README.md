# spec-cal
### Calendar app for monitoring historical rainfall using the Weather Underground API.

Unfortunately The Weather Company / Wunderground sucks and got rid of their APIs on 9/30/2018. I’d have to rebuild this using some other data source but I am simultaneously busy and lazy.

Should probably also update all the libraries used in requirements.txt and make sure this is Python3 compliant. Again, busy and lazy.

TO RUN THIS:
Run it using gunicorn, or install the requirements using PIP and then run:

`python SpecWeather.py`

I also ran a CRON job a few times a day to update the latest data by running:
 `python weatherUpdate.py` 

Good luck and keep slapping.
