#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
warnings.filterwarnings('ignore')


# In[2]:


data = pd.read_csv (r'C:\Users\HP\Downloads\Copy of HINDALCO_1D.csv')   
df = pd.DataFrame(data, columns= ['datetime','close','high','low','open','volume','instrument'])


# In[3]:


from pathlib import Path
Path('my_data.db').touch()


# In[4]:


import sqlite3
conn = sqlite3.connect('my_data.db')
c = conn.cursor()


# In[5]:


users = pd.read_csv(r'C:\Users\HP\Downloads\Copy of HINDALCO_1D.csv')
# write the data to a sqlite table
users.to_sql('users', conn, if_exists='append', index = False)


# In[6]:


c.execute('''SELECT * FROM users''').fetchall()


# In[7]:


pd.read_sql('''SELECT * FROM users''', conn)


# In[8]:


from datetime import datetime
df["new_date"] = df["datetime"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))


# In[9]:


df=df.set_index(df['new_date'].values)


# In[10]:


plt.figure(figsize=(13.2, 5.5))
plt.title('Close Price', fontsize=18)
plt.plot(df['close'], label='close price')
plt.xlabel('Date', fontsize = 18)
plt.ylabel('close price (INR)', fontsize=18)
plt.legend(df.columns.values, loc='upper left')
plt.show()


# In[11]:


typical_price = (df['close'] + df['high'] + df['low']) / 3
typical_price


# In[12]:


#Get the period
period = 14


# # MONEYFLOW

# In[14]:


money_flow = typical_price * df['volume']
money_flow


# # positive and negative money flow

# In[17]:


negative_flow= []
positive_flow= []

for i in range(1, len(typical_price)):
    if typical_price[i] > typical_price[i-1]:
        positive_flow.append(money_flow[i-1])
        negative_flow.append(0)
    elif typical_price[i] < typical_price[i-1]:
        negative_flow.append(money_flow[i-1])
        positive_flow.append(0)
    else:
        positive_flow.append(0)
        negative_flow.append(0)
        
        


# In[18]:


positive_mf = []
negative_mf = []

for i in range(period-1, len(positive_flow)):
    positive_mf.append(sum(positive_flow[i+1- period : i+1]) )
for i in range(period-1, len(negative_flow)):
    negative_mf.append(sum(negative_flow[i+1-period : i+1]) )
    
    


# # MONEY FLOW INDEX 

# In[19]:


mfi = 100* (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))
mfi


# In[21]:


df2 = pd.DataFrame()
df2['MFI'] =mfi
#create the plot
plt.figure(figsize=(13.2, 5.5))
plt.title('MFI', fontsize=18)
plt.plot(df2['MFI'], label='MFI')
plt.axhline(10, linestyle='--',color='orange')
plt.axhline(20, linestyle='--',color='blue')
plt.axhline(80,linestyle='--',color='blue')
plt.axhline(90, linestyle='--',color='orange')
plt.ylabel('MFI values')
plt.legend(df.columns.values, loc='upper left')
plt.show()


# In[22]:


new_df = pd.DataFrame()
new_df = df[period:]
new_df['MFI'] = mfi
new_df


# # BUY AND SELL SIGNALS

# In[23]:


def get_signal(data, high, low):
    buy_signal = []
    sell_signal = []
    
    for i in range(len(data['MFI'])):
        if data['MFI'][i] > high:
            buy_signal.append(np.nan)
            sell_signal.append(data['close'][i])
        elif data['MFI'][i] < low:
            buy_signal.append(data['close'][i])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)
            
    return (buy_signal, sell_signal)    
    


# In[24]:


new_df['Buy'] = get_signal(new_df, 80, 20)[0]
new_df['Sell'] = get_signal(new_df, 80, 20)[1]
new_df


# In[27]:


plt.figure(figsize=(13.2, 5.5))
plt.title('Close Price')
plt.plot(df['close'], label='close price', alpha = 0.5)
plt.scatter(new_df.index, new_df['Buy'], color='green', label='Buy Signal', marker='^', alpha=1)
plt.scatter(new_df.index, new_df['Sell'], color='red', label='Sell Signal', marker='v', alpha=1)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('close price (INR)', fontsize=18)
plt.legend(loc='upper left')
plt.show()
#plot
plt.figure(figsize=(13.2, 5.5))
plt.title('MFI', fontsize=18)
plt.plot(new_df['MFI'], label='MFI')
plt.axhline(10, linestyle='--',color='orange')
plt.axhline(20, linestyle='--',color='blue')
plt.axhline(80,linestyle='--',color='blue')
plt.axhline(90, linestyle='--',color='orange')
plt.ylabel('MFI values')
plt.legend(df.columns.values, loc='upper left')
plt.show()


# In[ ]:





# In[ ]:




