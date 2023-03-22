#!/usr/bin/env python
# coding: utf-8

# ## Business Problem
# High Cancellation rates leading to less revenue

# ## Research Question
# 1. What are variables that affect hotel cancellation rates?
# 2. How can we reduce Hotel cancellation rates?
# 3. How will hotels be assisted in making pricing and promotional decisions?

# ## Hypothesis
# 
# 1. More cancellations occur when prices are higher
# 2. Longer waiting list- leads to more cancellations
# 3. Majority clients are coming from offline travel agents

# # Uploading libraries

# In[8]:


import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# # Loading Data set

# In[9]:


df = pd.read_csv('hotel_bookings_2.csv')


# # Data Cleaning

# In[10]:


df.head(10)


# In[11]:


df.tail(10)


# In[12]:


#finding shape of data set
df.shape


# In[13]:


#finding stats of numerical data 
df.describe()


# In[14]:


df.info()


# In[15]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])


# In[16]:


df.info()


# In[17]:


#plotting a box graph to confirm outliers

df['adr'].plot(kind = 'box')


# In[18]:


# re- creating a column that has the outlier removed- by showing the new column has less than 5000
df = df[df['adr'] < 5000]
df['adr'].plot(kind = 'box')


# In[19]:


df.describe()


# In[20]:


#getting stats data about obect type data- qualitative
df.describe(include = 'object')


# In[21]:


# finding unique value sof object data of all object columns
#using for loop to do it

for col in df.describe(include = 'object').columns:
    print(col);
    print(df[col].unique());
    print('-'*50);
    


# In[22]:


df.isnull().sum()


# In[23]:


df.drop(['agent', 'company'], axis = 1, inplace = True)


# In[24]:


df.isnull().sum()


# # Data Analysis & Visualisations

# In[25]:


#how much is cancellation percentage in total
# using value_counts to find % 

canc_perc = df['is_canceled'].value_counts(normalize = True)*100
canc_perc


# In[26]:


#plot a graph to visualise the cancellations

plt.figure(figsize = (5,4))
plt.title('Hotel Reservations')
plt.bar(['not canceled', 'canceled'], df['is_canceled'].value_counts(), edgecolor = 'k', width = 0.7)
plt.show()


# In[58]:


#Let's figure out how are cancellation rates across the 2 diff types of hotels

plt.figure(figsize = (6,4))
plt.title('Cancellation rates across hotels')
ax1 = sn.countplot(x= 'hotel', hue = 'is_canceled', data = df, palette = "Blues");
plt.xlabel('hotels')
plt.ylabel('no. of reservations')
legend_labels,_ = ax1.get_legend_handles_labels() #get clarity
ax1.legend(bbox_to_anchor = (1,1)) #get clarity
plt.legend(['canceled' , 'not canceled'])

plt.show()


# In[28]:


#finding cancellationn % of individual hotels

resort_hotel = df[df['hotel'] == 'Resort Hotel']
print(resort_hotel['is_canceled'].value_counts( normalize = True))

city_hotel = df[df['hotel'] == 'City Hotel']
print(city_hotel['is_canceled'].value_counts( normalize = True))


# In[29]:


#check if price affects the cancellation rate sin these 2 diff types of hotels
#grouping by reservation date - we will check 'average daily rate'
#WE ARE GROUPING BECAUSE ON ONE DAY THERE MIGH BE LOT OF RECORDS

resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[30]:


print(resort_hotel)
print(city_hotel)


# In[57]:


#we are testing our hypothesis: Lets check if pricing plays a role in cancellation

plt.figure(figsize= (16,8))
plt.title('Price distribution of hotels', fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel[['adr']], label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel[['adr']], label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show()


# In[32]:


#extracting month from reservation status date

df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize= (12,6))
plt.title('Reservation Status per month', size = 20)
ax1 = sn.countplot(x='month', hue = 'is_canceled', data = df, palette = 'bright')
plt.xlabel('Months')
plt.ylabel('No of registarations')
legend_labels,_ = ax1.get_legend_handles_labels() #get clarity
ax1.legend(bbox_to_anchor = (1,1))
plt.legend(['not canceled', 'canceled'])
plt.show()


# In[33]:


# figuring out the prices by looking at the adr when cancelleations were done
#using data which is specific from cancellation data
# plotting it by months vs adr

# What we are tryying to figure out- if cancellations are happening 


plt.figure(figsize = (12,6))
plt.title('Rates when cancellation occured')
sn.barplot('month', 'adr', data = df[df['is_canceled']== 1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# #### This shows January had high prices and hence might be contributing to higher cancellations

# In[34]:


#Creating data set of cancelled data 

canceled_data = df[df['is_canceled'] == 1]
top_10_countries = canceled_data['country'].value_counts()[:10]
sn.barplot('country', 'adr', data = df[df['is_canceled']== 1].groupby('country')[['adr']].sum().reset_index()[:10])
plt.figure(figsize = (12,6))
plt.pie(top_10_countries, autopct = '%.2f' , labels = top_10_countries.index)
plt.show()


# In[35]:


#finding via which medium is customer is coming to hotel
df['market_segment'].value_counts(normalize = True)


# In[36]:


canceled_data['market_segment'].value_counts(normalize = True)


# In[37]:


#check 


# In[38]:


get_ipython().run_line_magic('pinfo', 'reset_index')


# In[52]:


#finding the prices in cancelled reservations and not-cancelled reservations
#comparing the two - to figure out if cancellations  were becuase of the high prices

canceled_data = df[df['is_canceled'] == 1]
canceled_data_adr = canceled_data.groupby('reservation_status_date')[['adr']].mean()
canceled_data_adr.reset_index(inplace = True)
canceled_data_adr.sort_values('reservation_status_date', inplace = True)

not_canceled_data = df[df['is_canceled'] == 0]
not_canceled_data_adr = not_canceled_data.groupby('reservation_status_date')[['adr']].mean()
not_canceled_data_adr.reset_index(inplace = True)
not_canceled_data_adr.sort_values('reservation_status_date', inplace = True)

#plot

plt.figure(figsize= (12,6))
plt.title('Price Range: Cancelled VS Not-canceled reservations')
plt.plot(not_canceled_data_adr['reservation_status_date'],not_canceled_data_adr['adr'], label = 'not canceled')
plt.plot(canceled_data_adr['reservation_status_date'],canceled_data_adr['adr'], label = 'canceled')
plt.legend();


# ![download.png](attachment:download.png)

# In[55]:


## look at the inconsistency- before 2015 and after 2017- lets remove it

canceled_data_adr = canceled_data_adr[(canceled_data_adr['reservation_status_date']> '2016') & (canceled_data_adr['reservation_status_date'] < '2017')]
not_canceled_data_adr = not_canceled_data_adr[(not_canceled_data_adr['reservation_status_date']>'2016') & (not_canceled_data_adr['reservation_status_date']< '2017')]

plt.figure(figsize= (12,6))
plt.title('Price Range: Cancelled VS Not-canceled reservations')
plt.plot(not_canceled_data_adr['reservation_status_date'],not_canceled_data_adr['adr'], label = 'not canceled')
plt.plot(canceled_data_adr['reservation_status_date'],canceled_data_adr['adr'], label = 'canceled')
plt.legend();

