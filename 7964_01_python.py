
import pandas as pd
import numpy as np

# Create the required data frames by reading in the files

de = pd.read_excel('SaleData.xlsx')
#data = pd.read_csv('imdb.csv',escapechar = "\\")
data = pd.read_csv('movie_metadata.csv')
df = pd.read_csv('diamonds.csv')


# Q1 Find least sales amount for each item
# has been solved as an example
def least_sales(de1):
    de1 = de1.groupby(["Item"])["Sale_amt"].min().reset_index()
    return de1
#print(least_sales(de))


# Q2 compute total sales at each year X region
def sales_year_region(de2):
    de2['year'] = de2['OrderDate'].dt.year
    de2 = de2.groupby(['year','Region'])['Sale_amt'].sum().reset_index()
    return de2
#print(sales_year_region(de))


# Q3 append column with no of days difference from present date to each order date
from datetime import date
def days_diff(de3):
    de3['days_diff'] = pd.to_datetime(date.today()) - de3['OrderDate']
    return de3
#print(days_diff(de))


# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(de4):
    de4 = de4.groupby('Manager')['SalesMan'].apply(lambda x: ','.join(set(x.dropna()))).rename('list_of_salesman').reset_index()
    return de4
#print(mgr_slsmn(de))


# Q5 For all regions find number of salesman and number of units
def slsmn_units(de):
    de5 = de.groupby(['Region'])['SalesMan'].count().rename('salesmen_count')
    de6 = de.groupby(['Region'])['Sale_amt'].sum().rename('total_sales')
    de5 = pd.concat([de5,de6],axis=1)
    return de5
#print(slsmn_units(de))


# Q6 Find total sales as percentage for each manager
def sales_pct(de):
    total_sales = de.groupby(['Manager'])['Sale_amt'].sum().rename('total_sales')
    res = total_sales.sum()
    de7 = total_sales.apply(lambda x: x/res).rename('percent_sales').reset_index()
    return de7
#print(sales_pct(de))


# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(data):
    data1 = data.loc[4,'imdb_score']
    return data1
#print(fifth_movie(data))


# Q8 return titles of movies with shortest and longest run time
def movies(data):
    title = []
    data2 = data[data['duration']==data['duration'].min()]
    data3 = data[data['duration']==data['duration'].max()]
    title.append(data2['movie_title'])
    title.append(data3['movie_title'])
    return title
#print(movies(data))


# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(data):
    data4 = data.sort_values(['title_year', 'imdb_score'], ascending=[True, False])
    return data4
#print(sort_df(data))


# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
def subset_df(data):
    data5 = data[(data['gross'] > 2000000) & (data['budget'] < 1000000) & (data['duration'] >= 30) & (data['duration'] <= 180)]
    return data5
#print(subset_df(data))


# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(df):
    df1 = df.duplicated().sum()
    return df1
#print(dupl_rows(df))


# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(df):
    df2 = df.dropna(subset=['carat','cut'],how='any')
    return df2
#print(drop_row(df))


# Q13 subset only numeric columns
def sub_numeric(df):
    df3 = df.select_dtypes(include=np.number)
    return df3
#print(sub_numeric(df))


# Q14 compute volume as (x*y*z) when depth > 60 else 8
def vol_check(df):
    volume = []
    for i in range(len(df)):
        if(df['depth'][i] > 60):
            if(df['z'][i] == 'None'):
                volume.append(np.nan)
            else:
                volume.append(float(df['x'][i])*float(df['y'][i])*float(df['z'][i]))
        else:
            volume.append(8)
    df['volume'] = volume
    return df
#print(vol_check(df))


# Q15 impute missing price values with mean
def impute(df):
    df5 = df['price'].fillna(value=df['price'].mean())
    return df5
#print(impute(df))