
# coding: utf-8

# # Intro to reimbursements: overview with visualization
# 
# This notebook provides an overview of the `2017-03-15-reimbursements.xz` dataset, which contains broad data regarding CEAP usage in all terms since 2007. It aims to provide an example of basic analyses and visualization by answering questions such as:
# 
# - In which period of the year more reimbursements were issued?
# - Which party spends more, in average, overall?
#     - And in Santa Catarina?
# - Which congressman spent more in 2015 term?
# - Which are the top service suppliers?
# - Which is the most expensive single reimbursement?
# 
# ---
# 
# The notebook is divided as follows:
# 
# ** 1. General description **
# 
# Sections containing basic information for readers get the dataset context.
# 
# ** 2. Questions & answers **
# 
# Data manipulation to answer questions as those listed above.
# 
# ---

# In[1]:

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pylab import rcParams

get_ipython().magic('matplotlib inline')

# Charts styling
plt.style.use('ggplot')
rcParams['figure.figsize'] = 15, 8
matplotlib.rcParams.update({'font.size': 14})
#rcParams['font.family'] = 'Georgia'

# Type setting for specific columns
#DTYPE = dict(cnpj=np.str, cnpj_cpf=np.str, ano=np.int16, term=np.str)

# Experimenting with 'category' type to reduce df size
DTYPE =dict(cnpj_cpf=np.str,            year=np.int16,            month=np.int16,            installment='category',            term_id='category',            term='category',            document_type='category',            subquota_group_id='category',            subquota_group_description='category',            #subquota_description='category',\
            subquota_number='category',\
            state='category',\
            party='category')


# In[2]:

reimbursements = pd.read_csv('../data/2017-03-15-reimbursements.xz',                              dtype=DTYPE, low_memory=False, parse_dates=['issue_date'])


# In[3]:

# Creates a DataFrame copy with fewer columns
rb = reimbursements[['year', 'month', 'total_net_value', 'party', 'state', 'term', 'issue_date',        'congressperson_name', 'subquota_description','supplier', 'cnpj_cpf']]
rb.head()


# ## 1. General description

# ### Consider only given year (e.g. 2016

# In[23]:

# Creates a DataFrame copy with data only for given year
YEAR = 2016
r = rb[rb.year == YEAR]


# ### How many congressmen?

# In[24]:

congressmen_qty = len(r.congressperson_name.unique())
congressmen_qty


# ### Total reimbursed in the year (in millions)

# In[25]:

total_reimbursements = r.total_net_value.sum()
total_reimbursements / 1e6


# ## 2. Questions & answers

# ### In which period of the year more reimbursements were issued?

# In[26]:

r.head()


# In[39]:

r.groupby('month')    .sum()    .total_net_value    .sort_index()    .plot(kind='bar')
    
plt.title('Fluctuation of reimbursements issued by months in ' + str(YEAR))
plt.ylabel('Total reimbursements (R$ tens of millions)')


# ### Which party has the most spending congressmen?

# ##### How many congressmen in each party?

# In[28]:

parties = r.party.unique()
parties


# In[29]:

d = dict()
for p in parties:
    d[p] = len(r[r.party == p].congressperson_name.unique())

s = pd.Series(d)
s


# #### How much did congressmen from each party spend in the year, in average? 

# In[50]:

t = r.groupby('party').sum()
t = t.drop(['year', 'month'], 1)  # Removes useless columns

t['congressmen_per_party'] = s
# Divides total amount of each party for how many members and 
t['monthly_value_per_congressperson'] = t['total_net_value'] / t['congressmen_per_party'] / 12
t.head()


# In[51]:

t.monthly_value_per_congressperson    .sort_values(ascending=False)    .plot(kind='bar')

plt.title('Average monthly reimbursements per congressperson in each party in ' + str(YEAR))
plt.ylabel('Total reimbursements (R$)')


# ### Which party spends more, in average, in Santa Catarina?

# In[ ]:

# Creates a DataFrame copy filtering only entries in the state (SC)
sc = rb_2016[rb_2016.state == 'SC']
sc.head()


# In[ ]:

sc.groupby('party')    .mean()    .total_net_value    .sort_values(ascending=False)    .plot(kind='bar')


# ### Which congressmen spent more in 2015 term?

# In[ ]:

rb_2016.groupby('congressperson_name')    .sum()    .total_net_value    .sort_values(ascending=False)    .head(10)


# In[ ]:

rb_2016.groupby('congressperson_name')    .sum()    .total_net_value    .sort_values(ascending=False)    .head(20)    .plot(kind='bar')


# ### How much was spent with each supplier?

# In[ ]:

rb_2016.groupby(['cnpj_cpf', 'supplier', 'subquota_description'])    .sum()    .sort_values(by='total_net_value', ascending=False)    .head(20)


# ### Services provided by most paid single supplier

# In[ ]:

rb_2016.groupby(['supplier', 'cnpj_cpf', 'subquota_description', 'year', 'congressperson_name'])    .sum()    .sort_values(by='total_net_value', ascending=False)    .loc['DOUGLAS CUNHA DA SILVA ME']    .total_net_value


# ### Which is the most expensive individual reimbursement?

# In[ ]:

rb = rb.sort_values(by='total_net_value', ascending=False)
rb.head()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:

rb.term.unique()


# In[ ]:



