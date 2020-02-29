import fitbit
from fitbit import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
CLIENT_ID = '22BFSK'
CLIENT_SECRET = '27d1af955e153fa8765fb3acb2ccabce'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

print("authorization successful")

yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))
print(today)
fit_statsHR = auth2_client.intraday_time_series('activities/steps', detail_level='15min')
print(fit_statsHR['activities-steps'])
time_list = []
val_list = []
for i in fit_statsHR['activities-steps-intraday']['dataset']:
    val_list.append(i['value'])
    time_list.append(i['time'])
heartdf = pd.DataFrame({'Step Count':val_list,'Time':time_list})
print(heartdf)

