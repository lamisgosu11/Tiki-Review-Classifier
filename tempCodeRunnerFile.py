#!/usr/bin/env python
# coding: utf-8

# Library

# In[8]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# In[3]:


df = pd.read_csv("D:/University/2022-2023\HK2/thuThapVaTienXuLyDuLieu/fat_preprocessing/comment_final.csv", encoding="utf-8", index_col=0)


# Check NAN
# 

# In[4]:


print('Data shape:', df.shape)
missing_val_num = df.isnull().sum()
missing_percent = (missing_val_num / df.shape[0]) * 100
missing_info = {'missing_values': missing_val_num,
                'missing_percent': round(missing_percent,3)}
missing_df = pd.DataFrame(missing_info)
missing_df


# In[5]:


df.dropna(inplace=True)
print(df.shape)
print(df.isnull().sum())


# Duplicate Data
# 

# In[6]:


df[df.duplicated()]


# In[7]:


# Drop all duplicate rows
df.drop_duplicates(inplace=True)
print('Duplicate data:', df.duplicated().sum())
print(df.shape)
# Reset index
df.reset_index(drop=True, inplace=True)


# In[9]:


#train the naive bayes model
X = df['comment']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
cv = CountVectorizer()
X_train = cv.fit_transform(X_train)
X_test = cv.transform(X_test)
clf = MultinomialNB()
clf.fit(X_train, y_train)
clf.score(X_test, y_test)


