
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
DTYPE = dict(cnpj=np.str, cnpj_cpf=np.str, ano=np.int16, term=np.str)


# In[ ]:

t = pd.read_csv('../data/2017-03-15-reimbursements.xz', dtype=DTYPE, low_memory=False)
t.info(memory_usage='deep')


# In[ ]:

t.columns


# In[ ]:

t.installments.unique()


# In[ ]:

d = dict()
for c in t.columns:
    print(c, len(t[c].unique()))
    d[c] = len(t[c].unique())


# In[ ]:

s = pd.Series(d)
s.sort_values()


# In[2]:

DTYPE_low_memory = dict(cnpj_cpf=np.str,                        installment='category',                        term_id='category',                        term='category',                        document_type='category',                        subquota_group_id='category',                        subquota_group_description='category',                        #subquota_description='category',\
                        subquota_number='category',\
                        state='category',\
                        party='category')

reimbursements_low = pd.read_csv('../data/2017-03-15-reimbursements.xz', dtype=DTYPE_low_memory, low_memory=False, parse_dates=['issue_date'])
reimbursements_low.info(memory_usage='deep')


# In[ ]:

DTYPE_low_memory = dict(cnpj=np.str,                        ano=np.int16,                        subquota_description='category',                        subquota_number='category',                        subquota_group_description='category',                        subquota_group_id='category',                        party='category',                        document_type='category',                        congressperson_id='category',                        congressperson_name=np.str,                        congressperson_document=np.str,                        cnpj_cpf='category',                        term='category',                        term_id='category',                        state='category',                        reimbursement_numbers=np.str,                        document_number='category',                        batch_number='category',                        leg_of_the_trip='category',                        passenger=np.str,                        supplier=np.str)

reimbursements_low = pd.read_csv('../data/2017-03-15-reimbursements.xz', dtype=DTYPE_low_memory, low_memory=False, parse_dates=['issue_date'])
reimbursements_low.info(memory_usage='deep')


# In[ ]:

#len(reimbursements_low.issue_date.unique())


# In[ ]:

#reimbursements.columns


# In[ ]:

#reimbursements.party.unique()


# In[3]:

# Creates a DataFrame copy with fewer columns
rb = reimbursements_low[['year', 'month', 'total_net_value', 'party', 'state', 'term', 'issue_date',        'congressperson_name', 'subquota_description','supplier', 'cnpj_cpf']]
rb.head()


# ## 1. General description

# ### Consider only 2015 term from now on

# In[4]:

# Creates a DataFrame copy for the 2015 term
rb_2015_term = rb[rb.term == '2015.0']


# ### How many congressmen?

# In[5]:

congressmen_qty = len(rb_2015_term.congressperson_name.unique())
congressmen_qty


# ### Total reimbursed in 2015 term (in millions)

# In[6]:

total_reimbursements = rb_2015_term.total_net_value.sum()
total_reimbursements / 1e6


# ## 2. Questions & answers

# ### In which period of the year more reimbursements were issued?

# In[7]:

rb_2015_term.head()


# In[8]:

rb_2015_term.groupby('month')    .sum()    .total_net_value    .plot(kind='bar')
    
plt.title('Período do ano com mais pedidos')
plt.ylabel('Total reimbursements (R$ tens of millions)')


# ### Which party spends more, in average?

# In[9]:

rb_2015_term.groupby('party')    .mean()    .total_net_value    .sort_values(ascending=False)    .plot(kind='bar')


# ### Which party spends more, in average, in Santa Catarina?

# In[10]:

# Creates a DataFrame copy filtering only entries in the state (SC)
sc = rb_2015_term[rb_2015_term.state == 'SC']
sc.head()


# In[11]:

sc.groupby('party')    .mean()    .total_net_value    .sort_values(ascending=False)    .plot(kind='bar')


# ### Which congressmen spent more in 2015 term?

# In[12]:

rb_2015_term.groupby('congressperson_name')    .sum()    .total_net_value    .sort_values(ascending=False)    .head(10)


# In[13]:

rb_2015_term.groupby('congressperson_name')    .sum()    .total_net_value    .sort_values(ascending=False)    .plot(kind='bar')


# ### How much was spent with each supplier?

# In[14]:

rb_2015_term.groupby(['cnpj_cpf', 'supplier', 'subquota_description'])    .sum()    .sort_values(by='total_net_value', ascending=False)    .head(20)


# ### Services provided by most paid single supplier

# In[15]:

rb_2015_term.groupby(['supplier', 'cnpj_cpf', 'subquota_description', 'year', 'congressperson_name'])    .sum()    .sort_values(by='total_net_value', ascending=False)    .loc['DOUGLAS CUNHA DA SILVA ME']    .total_net_value


# ### Which is the most expensive individual reimbursement?

# In[16]:

rb = rb.sort_values(by='total_net_value', ascending=False)
rb.head()


# In[ ]:



