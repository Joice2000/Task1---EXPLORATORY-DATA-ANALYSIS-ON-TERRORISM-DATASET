#!/usr/bin/env python
# coding: utf-8

# # TASK -1

# # EXPLORATORY DATA ANALYSIS ON GLOBAL TERRORISM DATASET

# ## STEP 1: IMPORTING DATASETS AND DATA CLEANING

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *
import warnings
warnings.filterwarnings('ignore')


# In[2]:


df= pd.read_csv(r'globalterrorismdb_0718dist.csv',encoding='ISO-8859-1')


# In[3]:


print(df.columns)


# In[4]:


df.head()


# In[5]:


col_list= list(df) 
print(col_list)


# ## there are more columns .so I am filtering the columns using excel
# 

# In[6]:


df_ter= pd.read_csv(r'C:\Users\joice mary\Downloads\Global Terrorism - START data\globalterrorismdb_0718dist.csv')


# In[7]:


df_ter.head()


# In[8]:


df_ter.columns


# In[9]:


df_ter.drop(columns={'eventid','country','iday','target1','natlty1_txt','guncertain1','property','weapdetail','dbsource','nwoundus','nwoundte','nkillus','nkillter','propextent_txt'},inplace=True)



df_ter.head()


# In[10]:


df_ter.rename(columns={'iyear':'Year','imonth':'Month','city':'City','country_txt':'Country','attacktype1_txt':'AttackType','nkill':'Killed','nwound':'Wounded','gname':'Group','targtype1_txt':'Target_type','weaptype1_txt':'Weapon_type','provstate':'State','weapsubtype1_txt':'WeaponSub_type','region_txt':'Region'},inplace=True)




# ## These are the columns that are required for analysis

# In[11]:


df_ter.columns


# In[12]:


df_ter.shape


# In[13]:


df_ter.dtypes


# In[14]:


df_ter.nunique()


# In[15]:


df_ter.isnull().sum()


# ## It can be seen that there are null values present in the given dataset. So it is important to remove or replace it

# In[16]:


df_ter['Wounded'] = df_ter['Wounded'].fillna(0)
df_ter['Killed'] = df_ter['Killed'].fillna(0)
df_ter['latitude'] =df_ter ['latitude'].fillna(0)
df_ter['longitude'] =df_ter ['longitude'].fillna(0)


# In[17]:


df_ter.isnull().sum()


# In[18]:


df_ter= df_ter.fillna({'State':'unknown','City':'unknown','WeaponSub_type': 'unknown'})


# ## Dataset without null values

# In[19]:


df_ter.isnull().sum()


# ## Checking for duplicated values

# In[20]:


df_ter.duplicated().sum()


# In[21]:


df_ter.drop_duplicates()


# ## Checking for outliers using some statistical Analysis

# In[22]:


df_ter.describe()


# In[23]:


hist=df_ter.hist(bins=5)


# ## There are no outliers present in the given dataset

# ## STEP 2: FINDING CORRELATIONS AND DATA VISUALIZATION

# In[24]:


correlation= df_ter.corr()
sns.heatmap(correlation,xticklabels= correlation.columns,yticklabels= correlation.columns,annot= True)


# In[25]:


plt.figure(figsize=(20,10))
sns.lineplot('Year','Killed',data=df_ter,color='y',label='Year')
plt.legend()
plt.show()


# ## This is the lineplot between Year and number of people killed. And it can be seen that there are more people killed it between the year's 1995 and 2005

# In[29]:


people_damage = df_ter[["Year","Killed"]].groupby('Year').sum()
list_year =  df_ter["Year"].unique().tolist()

#draw bar chart
fig, ax1 = plt.subplots(figsize = (20,6))
ax1.bar(people_damage.index, [i[0] for i in people_damage.values], color= '#0063B1' )

ax1.set_xticklabels(np.arange(1970, 2018, step=1), rotation=90)
ax1.set_ylabel('Number Of Dead/Injured People', size = 12)
ax1.set_xlabel('Year', size = 12)
ax1.set_title('Number of Terrorist Attacks vs Number of Dead/Injured people From 1970 to 2017', fontsize= 15, pad= 10, weight ='bold', 
                    color = sns.cubehelix_palette(8, start=.5, rot=-.75)[-3])
ax2 = ax1.twinx()

#Filter & get a number of attacked in the world from 1970 to 2017 
number_attack = []
for year in list_year:
    number_attack.append(len(df_ter[df_ter['Year'] == year][["Year"]]))
number_attack.insert(23, 0)

#draw plot chart
ax2.set_ylabel('Number Of Terrorist Attacks', size = 12,rotation=-90)
ax2.plot(range(1970, 2018), number_attack, 'r--o', mfc='k', label='Number Of Terrorist Attacks')

plt.xticks(np.arange(1970, 2018, step=1))
plt.legend(loc='upper left')
plt.show()


# In[47]:


plt.subplots(figsize=(15,6))
country_attacks = df_ter.Country.value_counts()[:15].reset_index()
country_attacks.columns = ['Country', 'Total Attacks']
sns.barplot(x=country_attacks.Country, y=country_attacks['Total Attacks'], palette= 'OrRd_r',edgecolor=sns.color_palette('dark',10))
plt.xticks(rotation=30)
plt.title('Number Of Total Attacks in Each Country')
plt.show()


# ## from these plot it can be clearly seen that Iraq, Pakistan, India, Afghanistan had faced the more number of attacks

# In[28]:


country_wound = df_ter[df_ter['Year'] > 1970][["Country", "Killed"]].groupby('Country',as_index=False).sum()
data_paint = country_wound.sort_values(by='Killed', ascending = False).tail(10)

#Paint the bar chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(data_paint["Country"][::-1], data_paint["Killed"][::-1], color = 'blue')
plt.xticks(rotation=-45)
ax.set_ylabel('Countries', size=16)
ax.set_xlabel('Number Of People Killed', size=16)
plt.title(" Countries Which had faced less or no Attacks", fontsize= 20, pad= 10, weight ='bold', 
             color = sns.cubehelix_palette(8, start=.5, rot=-.75)[-3])
plt.show()


# ## FROM THESE PLOTS WE CAN Say that these countries are Terrorist free countries 

# In[32]:


region_attacks = df_ter.Region.value_counts().to_frame().reset_index()
region_attacks.columns = ['Region', 'Total Attacks']
plt.subplots(figsize=(15,6))
sns.barplot(x=region_attacks.Region, y=region_attacks['Total Attacks'], palette='OrRd_r', edgecolor=sns.color_palette('dark',10))
plt.xticks(rotation=90)
plt.title('Number Of Total Attacks in Each Region')
plt.show()


# In[49]:


group_attacks = df_ter.Group.value_counts().to_frame().drop('Unknown').reset_index()[:16]
group_attacks.columns = ['Terrorist Group', 'Total Attacks']
group_attacks


# In[50]:


group_attacks = df_ter.Group.value_counts().to_frame().drop('Unknown').reset_index()[:16]
group_attacks.columns = ['Terrorist Group', 'Total Attacks']
plt.subplots(figsize=(10,8))
sns.barplot(y=group_attacks['Terrorist Group'], x=group_attacks['Total Attacks'], palette='YlOrRd_r',
            edgecolor=sns.color_palette('dark', 10))
# plt.xticks()
plt.title('Number Of Total Attacks by Terrorist Group')
plt.show()


# In[30]:


attack_plot=(ggplot(df_ter , aes(x='AttackType',y='Killed',fill='AttackType'))+ geom_col() + coord_flip()
  + scale_fill_brewer(type='div',palette="Spectral")+ theme_classic() + ggtitle('Attack types '))
display(attack_plot)
    


# In[67]:


weap_attacks = df_ter.Weapon_type.value_counts().to_frame().drop('Unknown').reset_index()[:16]
weap_attacks.columns = ['Weapon Type', 'Total Attacks']
plt.subplots(figsize=(10,8))
sns.barplot(y=weap_attacks['Weapon Type'], x=group_attacks['Total Attacks'], palette='YlOrRd_r',
            edgecolor=sns.color_palette('dark', 10))
# plt.xticks()
plt.title('Weapon Type in various attacks')
plt.show()


# In[31]:


attack_plot=(ggplot(df_ter , aes(x='Target_type',y='Killed',fill='Target_type'))+ geom_col() + coord_flip()
  + scale_fill_brewer(type='div',palette="Spectral")+ theme_classic() + ggtitle('Target types '))
display(attack_plot)
    


# In[26]:


df_ter.head()


# # ANALYSIS ON TERRORISM ATTACKS IN INDIA

# In[51]:


def change_case(text):
    text = text.lower()
    return text[0].upper()+text[1:]


# In[53]:


india_attacks = df_ter[df_ter.Country=='India'].reset_index()
india_attacks.City = india_attacks.City.apply(change_case)
india_attacks.head()


# In[56]:


plt.subplots(figsize=(15,6))
city_attacks_india = india_attacks.City.value_counts()[:15].reset_index()
city_attacks_india.columns = ['City', 'Total Attacks']
city_attacks_india.drop(1, inplace=True)
sns.barplot(x=city_attacks_india.City, y=city_attacks_india['Total Attacks'], palette='OrRd_r',
            edgecolor=sns.color_palette('dark',10))
plt.xticks(rotation=30)
plt.title('Total Number Of Attacks in Each Indian City')
plt.show()


# ## these are the cities from India that has facing more terrorist attacks

# In[58]:


plt.subplots(figsize=(15,6))
year_cas_ind = india_attacks.groupby('Year').Killed.sum().to_frame().reset_index()
year_cas_ind.columns = ['Year','Killed']
sns.barplot(x=year_cas_ind.Year, y=year_cas_ind.Killed, palette='RdYlGn_r',
            edgecolor=sns.color_palette('dark',10))
plt.xticks(rotation=90)
plt.title('Number Of Casualities in India Each Year')
plt.show()


# In[57]:


ind_attack_type = india_attacks.AttackType.value_counts().to_frame().reset_index()
ind_attack_type.columns = ['Attack Type', 'Total Number of people Killed']
plt.subplots(figsize=(15,6))
sns.barplot(x=ind_attack_type['Attack Type'], y=ind_attack_type['Total Number of people Killed'], palette='YlOrRd_r',
            edgecolor=sns.color_palette('dark', 10))
plt.xticks(rotation=90)
plt.title('Total Number of Attacks in India by Attack type')
plt.show()


# In[59]:


ind_group_attacks = india_attacks.Group.value_counts().to_frame().drop('Unknown').reset_index()[:8]
ind_group_attacks.columns = ['Terrorist Group', 'Total Attacks']
ind_group_attacks


# In[60]:


plt.subplots(figsize=(10,8))
sns.barplot(y=ind_group_attacks['Terrorist Group'], x=ind_group_attacks['Total Attacks'], palette='YlOrRd_r',
            edgecolor=sns.color_palette('dark', 10))
plt.xticks(range(0,110,10))
plt.title('Number Of Total Attacks by Terrorist Group in India')
plt.show()


# In[63]:


ind_groups_10 = india_attacks[india_attacks.Group.isin(india_attacks.Group.value_counts()[1:9].index)]
pd.crosstab(ind_groups_10.Year, ind_groups_10.Group).plot(color=sns.color_palette('Paired', 10))
fig=plt.gcf()
fig.set_size_inches(18,6)
plt.xticks(range(1985, 2017, 5))
plt.ylabel('Total Attacks')
plt.title('Top Terrorist Groups Activities in India from 1985 to 2017')
plt.show()


# # INFERENCES FROM ANALYZING THE ABOVE DATASET :
#   
#   ## a. Countries that are facing or faced more terrorist attacks are :
# ##               1) Iraq
# ##               2) Pakistan
# ##               3) Afghanistan
# ##               4) India
# 
# 
# 
# ##   b. More terrorist attacks happened in the year between 1995 and 2005
# 
# 
# 
# ##   c.  Most attacks are targeted on 
# ##                1) Private citizens
# ##                2) Police
# ##                3) Military
# 
# 
# ##   d. More commonly used weapon type in terrorism attacks 
# ##               1) Explosives
# ##               2) Firearms
# ##               3) Incendiary
# 
# 
# 
# ##   e. Highly used attack types are Armed Assault and Bombing Explosion
# 
# 
# 
# ##   f. Groups that had caused more disasters in the world :
# ##             1) Taliban
# ##             2) Islamic State of Iraq
# ##             3) Shining Path
# 
# 
#               

# # INFERENCES FROM ANALYZING TERRORISM ACTIVITIES IN INDIA
# 
# 
# ##   a. CITIES THAT ARE FACING MORE  TERRORIST ATTACKS :
# ##   1. Srinagar
# ##   2. Imphal
# ##   3. New Delhi
# 
# 
# ##   b. GROUPS THAT HAD DONE MORE ATTACKS IN iNDIA :
# ##   1. Communist Party Of India
# ##   2.  Maoists
# ##   3. Sikh Extremist
# 
# 
# ##  c.  ALOT NUMBER OF CASUALTIES HAD HAPPENED IN THE YEAR BETWEEN 1982 TO 2010
# 
# ##   d. MOSTLY USED ATTACK TYPES ARE ARMED ASSAULT AND BOMBINGS

# In[ ]:




