
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Heroes of Pymoli Data Analysis by Vijay Saxena
# * Male player spent significantly higher then Female players.
# * Although 'Total Revenue' for Male player ($1967) is significantly higher then Female players ($361), but 'Average Purchase' made by both is almost same i.e. ~ 4%
# * Most Popular items ('Oathbreaker, Last Hope of the Breaking Storm', 'Nirvana', 'Fiery Glass Crusader') are also in the list of Most popular item as evident in 'Most Poular Item' and 'Most Profitable Item' analysis
# * Most Popular and Most Profitable items 'Oathbreaker, Last Hope of the Breaking Storm' isnt the most expensive item or least expensive item.
# * Significant drop in players after the Age Group of 25-29 , it drops by more then 2/3 (from 365 to 101)
# 

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# Raw data file
file_to_load = "Resources/purchase_data.csv"

# Read purchasing file and store into pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data


# ## Player Count

# * Display the total number of players
# 

# In[3]:


player_count=purchase_data["SN"].nunique()
print(f"### Player Count(Unqiue): {player_count}")


# In[4]:


#Format all float values as currency
pd.options.display.float_format = '${:,.2f}'.format


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[5]:


print("### Purchasing Analysis (Total)")
unique_items=purchase_data["Item Name"].nunique()
avg_price=purchase_data['Price'].mean()
purchase_count=purchase_data["Price"].count()
total_rev = purchase_data['Price'].sum()
#purchase_analysis =pd.DataFrame[()]
purchase_analysis_df=pd.DataFrame({"Number of Unique Items" : [unique_items],
              "Average Price": [round(avg_price,2)],
             "Number of Purchases":[purchase_count],
             "Total Revenue":[round(total_rev,2)]})
#purchase_analysis_df=pd.DataFrame(purchase_analysis_data)
#purchase_analysis_df['Average Price']=purchase_analysis_df["Average Price"].map("${0:,.2f}".format)
#purchase_analysis_df['Total Revenue']=purchase_analysis_df["Total Revenue"].map("${0:,.2f}".format)
purchase_analysis_df[['Number of Unique Items','Average Price','Number of Purchases','Total Revenue']]       


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[6]:


print ("### Gender Demographics-v1 (With Calculations based on Non-Unique player count)")
gender_demg_df=purchase_data.groupby(['Gender'])
gender_demg_df=gender_demg_df['SN'].count().reset_index()
gender_demg_df.columns=['Gender','Total']
gender_demg_df['Percentage']= round((gender_demg_df['Total'] / gender_demg_df['Total'].sum())*100,2)

gender_demg_df['Percentage']=gender_demg_df["Percentage"].map("{0:,.2f}%".format)
gender_demg_df = gender_demg_df[['Gender', 'Percentage','Total']]
gender_demg_df.sort_values(by=['Total'], ascending=False).set_index('Gender')


# In[7]:


print ("### Gender Demographics-v2 (With Calculations based on Unique player count)")
gender_demg_df=purchase_data.groupby(['Gender'])
gender_demg_df=gender_demg_df['SN'].nunique().reset_index()
gender_demg_df.columns=['Gender','Total']
gender_demg_df['Percentage']= round((gender_demg_df['Total'] / gender_demg_df['Total'].sum())*100,2)

gender_demg_df['Percentage']=gender_demg_df["Percentage"].map("{0:,.2f}%".format)
gender_demg_df = gender_demg_df[['Gender', 'Percentage','Total']]
gender_demg_df.sort_values(by=['Total'], ascending=False).set_index('Gender')


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[8]:


print("### Purchasing Analysis (Gender)-v1")
gender_grp=purchase_data.groupby(['Gender'])
gender_list=[]
purchase_count=[]
avg_list=[]
total_list=[]
avg_total_person_list=[]
for g,g_df in gender_grp:
    #print(f"{g}  {g_df['SN'].nunique()} {g_df['Purchase ID'].count()}  {round(g_df['Price'].mean(),2)}  {round(g_df['Price'].sum(),2)}")
    gender_list.append(g)
    purchase_count.append(g_df['Purchase ID'].count())
    avg_list.append(round(g_df['Price'].mean(),2))
    total_list.append(round(g_df['Price'].sum(),2))
    avg_total_person_list.append(round(g_df['Price'].sum()/g_df['SN'].nunique(),2))
    
    
gender_purchase_data={"Gender":gender_list,
            "Purchase Count":purchase_count,
            "Average Purchase Price":avg_list,
            "Total Revenue":total_list,
            "Average Purchase Total per Person":avg_total_person_list}
gender_purchase_df=pd.DataFrame(gender_purchase_data)
#gender_purchase_df
gender_purchase_df=gender_purchase_df[["Gender","Purchase Count","Average Purchase Price", "Total Revenue","Average Purchase Total per Person"]].sort_values(by=['Purchase Count'], ascending=False)
#gender_purchase_df['Average Purchase Price']=gender_purchase_df["Average Purchase Price"].map("${0:,.2f}".format)
#gender_purchase_df['Total Revenue']=gender_purchase_df["Total Revenue"].map("${0:,.2f}".format)
#gender_purchase_df['Average Purchase Total per Person']=gender_purchase_df["Average Purchase Total per Person"].map("${0:,.2f}".format)

gender_purchase_df.set_index('Gender')


# In[ ]:


######testing


# In[9]:


print("### Purchasing Analysis (Gender)-v2")
gender_list=[]
player_count=[]
purchase_count=[]
avg_list=[]
total_list=[]
avg_total_person_list=[]
for gender in purchase_data["Gender"].unique():
    g_df=purchase_data[purchase_data["Gender"]==gender]
    g_avg_price=round(g_df['Price'].mean(),2)
    g_purchase_count=g_df["Price"].count()
    g_total_rev = round(g_df['Price'].sum(),2)
    g_avg_total_person = round(g_df['Price'].sum()/g_df['SN'].nunique(),2)

    gender_list.append(gender)
    player_count.append(g_df['SN'].nunique())
    purchase_count.append(g_purchase_count)
    avg_list.append(g_avg_price)
    total_list.append(g_total_rev)
    avg_total_person_list.append(g_avg_total_person)

gender_purchase_data={"Gender":gender_list,
            "Purchase Count":purchase_count,
            "No of Players(Unique)":player_count,
            "Average Purchase Price":avg_list,
            "Total Revenue":total_list,
            "Average Purchase Total per Person":avg_total_person_list}
gender_purchase_df=pd.DataFrame(gender_purchase_data)

gender_purchase_df=gender_purchase_df[["Gender","Purchase Count","No of Players(Unique)","Average Purchase Price", "Total Revenue","Average Purchase Total per Person"]].sort_values(by=['Purchase Count'], ascending=False)

#gender_purchase_df['Average Purchase Price']=gender_purchase_df["Average Purchase Price"].map("${0:,.2f}".format)
#gender_purchase_df['Total Revenue']=gender_purchase_df["Total Revenue"].map("${0:,.2f}".format)
#gender_purchase_df['Average Purchase Total per Person']=gender_purchase_df["Average Purchase Total per Person"].map("${0:,.2f}".format)

gender_purchase_df.set_index('Gender')  


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[15]:


print("### Age Demographics")
# Establish bins for ages
pd.options.display.float_format = '{:,.2f}%'.format
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

purchase_data['Age Group']=pd.cut(purchase_data["Age"], age_bins,labels=group_names)
age_analysis_df=purchase_data[["SN","Age Group"]]

age_analysis_df=age_analysis_df.groupby("Age Group")["SN"].count().reset_index()
age_analysis_df.columns=[["Age Group","Total"]]
age_analysis_df['Percentage']=round((age_analysis_df['Total']/age_analysis_df['Total'].sum())*100,2)
age_analysis_df = age_analysis_df[['Age Group', 'Percentage','Total']]
age_analysis_df.set_index('Age Group')
#age_analysis_df['Percentage']=age_analysis_df["Percentage"].map("%{0:,.2f}".format)


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[18]:


pd.options.display.float_format = '${:,.2f}'.format
age_df=purchase_data.groupby("Age Group")
pcount=age_df["Purchase ID"].count().reset_index()
ucount=age_df["SN"].nunique().reset_index()
avgprice=round(age_df["Price"].mean(),2).reset_index()
sumprice=age_df["Price"].sum().reset_index()
avgtotalpp=round(age_df["Price"].sum()/age_df["SN"].nunique(),2).reset_index()

age_df=pcount.merge (ucount, on='Age Group').merge(avgprice, on='Age Group').merge(sumprice, on='Age Group').merge(avgtotalpp, on='Age Group')
age_df.columns=["Age Group","Purchase Count","Unique count","Average Purchase Price","Total Purchase Value","Average Purchase Total per Person"]
age_df.set_index('Age Group', inplace=True)
#age_df['Average Purchase Price']=age_df["Average Purchase Price"].map("${0:,.2f}".format)
#age_df['Average Purchase Total per Person']=age_df["Average Purchase Total per Person"].map("${0:,.2f}".format)
#age_df['Total Purchase Value']=age_df["Total Purchase Value"].map("${0:,.2f}".format)
age_df


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[19]:


pd.options.display.float_format = '${:,.2f}'.format
topspender_df=purchase_data.groupby("SN")
#sn_df

pcount=topspender_df["Purchase ID"].count().reset_index()
avgprice=round(topspender_df["Price"].mean(),2).reset_index()
sumprice=topspender_df["Price"].sum().reset_index()
topspender_df=pcount.merge (avgprice, on='SN').merge(sumprice, on='SN')
topspender_df.columns=["SN","Purchase Count","Average Purchase Price","Total Purchase Value"]

#sn_df.set_index("SN",inplace=True)
topspender_df.sort_values(by=["Total Purchase Value"], ascending=False).head(5).set_index('SN')


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[20]:


popular_item_df=purchase_data.groupby(["Item ID","Item Name"])
pcount=popular_item_df["Purchase ID"].count().reset_index()
avgprice=round(popular_item_df["Price"].mean(),2).reset_index()
sumprice=popular_item_df["Price"].sum().reset_index()
popular_item_df=pcount.merge (avgprice, on=['Item ID','Item Name']).merge(sumprice, on=['Item ID','Item Name'])
popular_item_df.columns=["SN","Item Name", "Purchase Count","Item Price","Total Purchase Value"]

popular_item_df.sort_values(by=["Purchase Count"], ascending=False).head(5).set_index(['SN','Item Name'])


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[21]:


popular_item_df.sort_values(by=["Total Purchase Value"], ascending=False).head(5).set_index(['SN','Item Name'])

