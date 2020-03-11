import fitbit
from fitbit import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
from datetime import date,timedelta

# CLIENT_ID = '22BFSK'
# CLIENT_SECRET = '27d1af955e153fa8765fb3acb2ccabce'
CLIENT_ID = input("Enter the Client id: ")
CLIENT_SECRET = input("Enter the Client secret: ")

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

print("authorization successful")
time_list = []
val_list = []
date_list=[]

# yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
# yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
# today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
# for date in range(1,16):
#     yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=date)).strftime("%Y-%m-%d"))
#     today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
#     fit_statsHR = auth2_client.intraday_time_series('activities/steps',base_date=yesterday2, detail_level='1min')
#
#     for i in fit_statsHR['activities-steps-intraday']['dataset']:
#         val_list.append(i['value'])
#         time_list.append(i['time'])
#         date_list.append(yesterday2)
#     stepsdf = pd.DataFrame({'Step Count':val_list,'Time':time_list,'Date':date_list})
# print(stepsdf)
h_time_list = []
h_val_list = []
h_date_list=[]
time_list = []
val_list = []
date_list=[]
stime_list = []
sval_list = []
sdate_list=[]
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

#start date
start_year = input("Enter start_date year: ")
start_month = input("Enter start_date month: ")
start_day = input("Enter start_date day: ")
end_year = input("Enter end_date year: ")
end_month = input("Enter end_date month: ")
end_day = input("Enter end_date day: ")
start_date = date(int(start_year),int(start_month),int(start_day))
end_date = date(int(end_year),int(end_month),int(end_day)+1)
# start_date = date(2020,3,9)
# end_date = date(2020,3,11)
for single_date in daterange(start_date, end_date):
    date_new = single_date.strftime("%Y-%m-%d")
    #Heart Rate
    fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=date_new, detail_level='1min')
    for i in fit_statsHR['activities-heart-intraday']['dataset']:
        h_val_list.append(i['value'])
        h_time_list.append(i['time'])
        h_date_list.append(date_new)
    heartdf = pd.DataFrame({'Heart Rate':h_val_list,'Time':h_time_list,'Date':h_date_list})
    # heartdf['Time'] = pd.to_datetime(heartdf['Time'])
    # heartdf = heartdf.set_index('Time')
    # heartdf = heartdf.resample('5T').mean()
    # heartdf = heartdf.reset_index()

    fit_statsHR = auth2_client.intraday_time_series('activities/steps', base_date=date_new, detail_level='1min')
    for i in fit_statsHR['activities-steps-intraday']['dataset']:
        val_list.append(i['value'])
        time_list.append(i['time'])
        date_list.append(date_new)
    stepsdf = pd.DataFrame({'Time':time_list,'Date':date_list,'Step Count':val_list})
    # stepsdf['Time'] = pd.to_datetime(stepsdf['Time'])
    # stepsdf = stepsdf.set_index('Time')
    # stepsdf = stepsdf.resample('5T').sum()
    # stepsdf = stepsdf.reset_index()
    # date_list=[]
    # time_list=[]
    # for x in stepsdf['Time']:
    #     d=datetime.datetime.strptime(str(x),"%Y-%m-%d  %H:%M:%S")
    #     date_list.append(d.date())
    #     time_list.append(d.time())
    # stepsdf['Time_data'] = time_list
    # stepsdf['Date_data'] = date_list

    fitbit_stats3 = auth2_client.sleep(date=date_new)
    for i in fitbit_stats3['sleep'][0]['minuteData']:
        stime_list.append(i['dateTime'])
        sval_list.append(i['value'])
        sdate_list.append(date_new)
    sleepdf = pd.DataFrame({'Sleep State':sval_list,'Time':stime_list,'Date':sdate_list})
    # # """Sleep data on the night of ...."""
    # sleepdf['Time'] = pd.to_datetime(sleepdf['Time'])
    # sleepdf['Sleep State'] = pd.to_numeric(sleepdf['Sleep State'])
    # sleepdf = sleepdf.set_index('Time')
    # sleepdf = sleepdf.resample('5T').sum()
    # sleepdf = sleepdf.reset_index()
    # for x in range(0,len(sleepdf['Sleep State'])):
    #     if(sleepdf['Sleep State'][x]>=5):
    #         sleepdf['Sleep State'][x]=1
    #     # elif(sleepdf['Sleep State'][x]==0):
    #     #     sleepdf['Sleep State'][x]=0
    #     # elif(sleepdf['Sleep State'][x]>-5 and sleepdf['Sleep State'][x]<=0):
    #     #     sleepdf['Sleep State'][x]=0
    #     else:
    #         sleepdf['Sleep State'][x]=0
new_datetime_heart = []
for i in range(0,len(heartdf['Date'])):
    new_datetime_heart.append(datetime.datetime.strptime(heartdf['Date'][i]+" "+heartdf['Time'][i], '%Y-%m-%d %H:%M:%S'))
heartdf['Time'] = new_datetime_heart
heartdf = heartdf.set_index('Time')
heartdf = heartdf.resample('5T').mean()
heartdf = heartdf.reset_index()
# print(heartdf)

new_datetime_steps = []
for i in range(0,len(stepsdf['Date'])):
    new_datetime_steps.append(datetime.datetime.strptime(stepsdf['Date'][i]+" "+stepsdf['Time'][i], '%Y-%m-%d %H:%M:%S'))
stepsdf['Time'] = new_datetime_steps
stepsdf = stepsdf.set_index('Time')
stepsdf = stepsdf.resample('5T').sum()
stepsdf = stepsdf.reset_index()
date_list=[]
time_list=[]
for x in stepsdf['Time']:
    d=datetime.datetime.strptime(str(x),"%Y-%m-%d  %H:%M:%S")
    date_list.append(d.date())
    time_list.append(d.time())
stepsdf['Time_data'] = time_list
stepsdf['Date_data'] = date_list
# print(stepsdf)


# """Sleep data on the night of ...."""
new_datetime_sleep = []
for i in range(0,len(sleepdf['Date'])):
    new_datetime_sleep.append(datetime.datetime.strptime(sleepdf['Date'][i]+" "+sleepdf['Time'][i], '%Y-%m-%d %H:%M:%S'))
sleepdf['Time'] = new_datetime_sleep
sleepdf['Sleep State'] = pd.to_numeric(sleepdf['Sleep State'])
sleepdf = sleepdf.set_index('Time')
sleepdf = sleepdf.resample('5T').sum()
sleepdf = sleepdf.reset_index()
for x in range(0,len(sleepdf['Sleep State'])):
    if(sleepdf['Sleep State'][x]>=5):
        sleepdf['Sleep State'][x]=1
    # elif(sleepdf['Sleep State'][x]==0):
    #     sleepdf['Sleep State'][x]=0
    # elif(sleepdf['Sleep State'][x]>-5 and sleepdf['Sleep State'][x]<=0):
    #     sleepdf['Sleep State'][x]=0
    else:
        sleepdf['Sleep State'][x]=0

# print(sleepdf)
#
data=pd.concat([stepsdf.set_index('Time'),heartdf.set_index('Time'),sleepdf.set_index('Time')],axis=1)

data.reset_index(level='Time',col_level=1,col_fill='Time_data')
data['Heart Rate'].fillna(-1,inplace=True)
data['Step Count'].fillna(-99,inplace=True)
data['Sleep State'].fillna(-1,inplace=True)
data['Time_data'].fillna('no inputs yet',inplace=True)
data['Date_data'].fillna('no inputs yet',inplace=True)
data_new = data[data['Time_data']!='no inputs yet']
# print(data_new)



# new_data=pd.concat([data.set_index('Time'),sleepdf.set_index('Time')],axis=1)
# new_data['Sleep State'].fillna(1,inplace=True)
# print(new_data)
# sleepdf.to_csv('/Users/shsu/Downloads/python-fitbit-master/Sleep/sleep' + \
#               today+'.csv', \
#               columns = ['Time','State','Interpreted'],header=True,
#               index = False)


data.to_csv(path_or_buf='/Users/hp/Desktop/'+'fitbit_data'+CLIENT_ID+'.csv',columns=['Date_data','Time_data','Heart Rate','Step Count','Sleep State'], header=True, index = False)
print('The fitbit_data'+CLIENT_ID+'.csv file has been downloaded on your desktop')
