#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os


# ## Task 1: Merge the 12 months of sales data into a single csv file

# In[3]:


df=pd.read_csv("/Users/macbookair/Downloads/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_April_2019.csv")

files=[file for file in os.listdir("/Users/macbookair/Downloads/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data")]

all_months_data=pd.DataFrame()

for file in files:
       df = pd.read_csv("/Users/macbookair/Downloads/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/"+file)
       all_months_data=pd.concat([all_months_data,df])
    
all_months_data.to_csv("all_data.csv",index=False)


# #  Read in updated dataframe

# In[4]:


all_data=pd.read_csv("all_data.csv")
all_data.head()


# ## Clean up the data

# ### Drop rows of NAN

# In[5]:


nan_df=all_data[all_data.isna().any(axis=1)]
nan_df.head()
all_data=all_data.dropna(how="all")
all_data.head()


# ### Find "Or" and delete it

# In[6]:


all_data=all_data[all_data["Order Date"].str[0:2]!="Or"]


# ### Convert columns to the correct type

# In[7]:


all_data["Quantity Ordered"]=pd.to_numeric(all_data["Quantity Ordered"])
all_data["Price Each"]=all_data["Price Each"].astype("float")


# # Augment data with additional columns

# ### Task 2:Add Month Column

# In[8]:


all_data["Month"]=all_data["Order Date"].str[0:2]
all_data["Month"]=all_data["Month"].astype('int32')


# In[9]:


all_data.head()


# ### Task 3: Add Sales column

# In[10]:


all_data["Sales"]=all_data["Quantity Ordered"]*all_data["Price Each"]


# ### Task 4: Add a city column

# In[11]:


def get_City(address):
    return address.split(",")[1]

def get_State(address):
    return address.split(",")[2].split(' ')[1]

all_data["City"]=all_data["Purchase Address"].apply(lambda x:get_City(x)+" "+get_State(x))


# ## What was the best month for sales? How much was earned that month?

# In[12]:


results=all_data.groupby("Month").sum()


# In[13]:


import matplotlib.pyplot as plt 

months=range(1,13)

plt.bar(months,results["Sales"])
plt.xticks(months)
plt.ylabel("Sales in USD ($)")
plt.xlabel("Months number")
plt.show()


# #### Question 2: Which city had the highest number of sales?

# In[14]:


res=all_data.groupby("City").sum()


# In[16]:


res


# In[17]:


cities=[City for City,df in  all_data.groupby("City")]

plt.bar(cities,res["Sales"])
plt.xticks(cities,rotation="vertical",size=8)
plt.xlabel("City Name")
plt.ylabel("Sales in USD($)")
plt.show()


# ## Question 3: What time should we display advertisements to maximize likelihood of cutomer's buying product

# In[18]:


all_data["Order Date"]=pd.to_datetime(all_data["Order Date"])


# In[19]:


all_data["Hour"]=all_data["Order Date"].dt.hour
all_data['Minute']=all_data['Order Date'].dt.minute


# In[20]:


all_data


# In[33]:


hours=[df for hour,df in all_data.groupby("Hour")]


# In[27]:


plt.plot(hours,all_data.groupby(["Hour"]).count())
plt.xticks(hours)
plt.xlabel("Hours")
plt.ylabel("Number of orders")
plt.grid()
plt.show()


# ## Question 4: What Products are most often sold together?

# In[28]:


df=all_data[all_data["Order ID"].duplicated(keep=False)]

df["Grouped"]=df.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))

df=df[["Order ID","Grouped"]].drop_duplicates()

df.head()


# In[23]:


from itertools import combinations
from collections import Counter

count=Counter()

for row in df["Grouped"]:
    row_list=row.split(",")
    count.update(Counter(combinations(row_list,2)))
    
for key,value in count.most_common(10):
    print(key,value)


# ## Question 5: What product sold the most? Why do you think it sold the most?

# In[35]:


all_data["Order Date"]=all_data["Order Date"].astype("str")
product_group=all_data.groupby("Product")
quantity_ordered=product_group.sum()["Quantity Ordered"]

products=[product for product,df in product_group]
plt.bar(products,quantity_ordered)
plt.xticks(products,rotation="vertical",size=8)
plt.xlabel("Products")
plt.ylabel("Quantity Ordered")
plt.show()

