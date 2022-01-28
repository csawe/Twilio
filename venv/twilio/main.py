import requests
import pandas as pd
import os
from dotenv import load_dotenv
import json
load_dotenv()

def load_data(sid, token, name):
    accountSID = os.getenv(sid)
    authToken =  os.getenv(token)
    accountName = os.getenv(name)
    url = f'https://api.twilio.com/2010-04-01/Accounts/{accountSID}/Usage/Records/Daily.json'
    response = requests.get(url, auth=(accountSID, authToken))
    data = response.json()
    for key, value in data.items():
        print(key, " : ", value)
    data = data['usage_records']
    print('Number of Messages: ', len(data))
    print(json.dumps(data, indent=2))
    data = pd.DataFrame(data)
    data['account_name'] = accountName
    return data    
    
number_of_accounts = 1
i=1
while (i<=number_of_accounts):
    sid = "SID"+str(i)
    token = "TOKEN"+str(i)
    name = "NAME"+str(i)
    if (i==1):
        dataframe = load_data(sid,token,name)
    else:
        tempframe = load_data(sid,token)
        dataframe = dataframe.append(tempframe)
    print(f"Done with account number {i}")
    i +=1


data = dataframe.groupby(['account_name','end_date'])['price'].sum().reset_index()
current_dir = os.getcwd()
data.to_csv(f'{current_dir}\data.csv')

def daily_table_add():
    daily_data = pd.read_csv(f'{current_dir}\data.csv')
    daily_data.drop(daily_data.columns[daily_data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    if os.path.isfile(f'{current_dir}\daily_data.csv'):
        prev =  pd.read_csv('daily_data.csv')
        prev.drop(prev.columns[prev.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        daily_data = prev.append(daily_data)
        daily_data.to_csv('daily_data.csv')
    else:
        daily_data.drop(daily_data.columns[daily_data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        daily_data.to_csv('daily_data.csv')

daily_table_add()
