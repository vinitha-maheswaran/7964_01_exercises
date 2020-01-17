import pandas as pd
import numpy as np

# Create the required data frames by reading in the files
data_s = pd.read_excel('SaleData.xlsx')
data_i = pd.read_csv('imdb.csv',escapechar = "\\")
data_m = pd.read_csv('movie_metadata.csv',escapechar = "\\")
data_d = pd.read_csv('diamonds.csv')

from datetime import datetime
import math

# Q1 Find least sales amount for each item
# has been solved as an example
def least_sales(df):
    df = df.groupby(["Item"])["Sale_amt"].min().reset_index()
    return df

#print(least_sales(data_s))


# Q2 compute total sales at each year X region
def sales_year_region(df):
    df['year'] = df['OrderDate'].dt.year
    df = df.groupby(['year','Region'])['Sale_amt'].sum().reset_index()
    return df

#print(sales_year_region(data_s))


# Q3 append column with no of days difference from present date to each order date
def days_diff(df,ref_date):
    df['days_diff'] = pd.to_datetime(datetime.strptime(ref_date,'%d/%m/%Y').date()) - df['OrderDate']
    return df

#print(days_diff(data_s,"17/01/2020"))


# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(df):
    df = df.groupby('Manager')['SalesMan'].apply(lambda x: ','.join(set(x.dropna()))).rename('list_of_salesman').reset_index()
    return df

#print(mgr_slsmn(data_s))


# Q5 For all regions find number of salesman and number of units
def slsmn_units(df):
    df1 = df.groupby(['Region'])['SalesMan'].count().rename('salesmen_count')
    df2 = df.groupby(['Region'])['Sale_amt'].sum().rename('total_sales')
    df1 = pd.concat([df1,df2],axis=1)
    return df1

#print(slsmn_units(data_s))


# Q6 Find total sales as percentage for each manager
def sales_pct(df):
    total_sales = df.groupby(['Manager'])['Sale_amt'].sum().rename('total_sales')
    res = total_sales.sum()
    df3 = total_sales.apply(lambda x: x/res).rename('percent_sales').reset_index()
    return df3

#print(sales_pct(data_s))


# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(df):
    df4 = df.loc[4,'imdb_score']
    return df4

#print(fifth_movie(data_m))


# Q8 return titles of movies with shortest and longest run time
def movies(df):
    title = []
    df5 = df[df['duration']==df['duration'].min()]
    df6 = df[df['duration']==df['duration'].max()]
    title.append(df5['movie_title'])
    title.append(df6['movie_title'])
    return title

#print(movies(data_m))


# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(df):
    df = df.sort_values(['title_year', 'imdb_score'], ascending=[True, False])
    return df

#print(sort_df(data_m))


# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
def subset_df(df):
    data = df[(df['gross'] > 2000000) & (df['budget'] < 1000000) & (df['duration'] >= 30) & (df['duration'] <= 180)]
    return data

#print(subset_df(data_m))


# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(df):
    df1 = df.duplicated().sum()
    return df1

#print(dupl_rows(data_d))


# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(df):
    df2 = df.dropna(subset=['carat','cut'],how='any')
    return df2

#print(drop_row(data_d))


# Q13 subset only numeric columns
def sub_numeric(df):
    df3 = df.select_dtypes(include=np.number)
    return df3

#print(sub_numeric(data_d))


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

#print(vol_check(data_d))


# Q15 impute missing price values with mean
def impute(df):
    df5 = df['price'].fillna(value=df['price'].mean())
    return df5

#print(impute(data_d))


#Bonus Q1
#Generate a report that tracks the various Genere combinations for each type year on year. The result
#data frame should contain type, Genere_combo, year, avg_rating, min_rating, max_rating,
#total_run_time_mins

def bonus_q1(df):
    data = df[['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime','Documentary', 'Drama', 'Family',
              'Fantasy', 'FilmNoir', 'GameShow', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'RealityTV', 
              'Romance', 'SciFi', 'Short', 'Sport', 'TalkShow', 'Thriller', 'War', 'Western']]
    df['genre_combo'] = df[data.columns].apply(lambda x: ','.join(x.index[x==1]),axis=1)
    res = df.groupby(['type','year','genre_combo'],as_index=False).agg({'imdbRating':[np.mean, min, max],'duration':[np.sum]})
    return(res)

#bonus_q1(data_i)


#Bonus Q2
#Is there a realation between the length of a movie title and the ratings ? Generate a report that captures
#the trend of the number of letters in movies titles over years. We expect a cross tab between the year of
#the video release and the quantile that length fall under. The results should contain year, min_length,
#max_length, num_videos_less_than25Percentile, num_videos_25_50Percentile ,
#num_videos_50_75Percentile, num_videos_greaterthan75Precentile

def bonus_q2(df):
    df['Title_Length']=df['wordsInTitle'].str.len()
    df['Title_Length'].corr(df['imdbRating'])
    df['Quantile'] = pd.qcut(df['Title_Length'], q=4,labels=False)
    data = pd.crosstab(df['year'], df['Quantile'])
    data['Min_Len'] = df.groupby(["year"])["Title_Length"].min()
    data['Max_Len'] = df.groupby(["year"])["Title_Length"].max()
    data.columns = ['num_videos_less_than25Percentile', 'num_videos_25_50Percentile', 'num_videos_50_75Percentile', 'num_videos_greaterthan75Precentile', 'min_len', 'max_len']
    return data

#bonus_q2(data_i)


#Bonus Q3
#In diamonds data set Using the volumne calculated above, create bins that have equal population within
#them. Generate a report that contains cross tab between bins and cut. Represent the number under
#each cell as a percentage of total.

def bonus_q3(df):
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
    df['bins'] = pd.qcut(df['volume'], q=5,labels=False)
    df1 = pd.crosstab(df['bins'], df['cut'],normalize=True,margins=True)*100
    return df1

#bonus_q3(data_d)


#Bonus Q4
#Generate a report that tracks the Avg. imdb rating quarter on quarter, in the last 10 years, for movies
#that are top performing. You can take the top 10% grossing movies every quarter. Add the number of top
#performing movies under each genere in the report as well.

def bonus_q4(df):
    year = df['title_year'].unique()
    df['url'] = df['movie_imdb_link'].apply(lambda x: x.split('?')[0])
    b = pd.DataFrame()
    p = 0.1
    for j in year:
        new = df[df['title_year'] == j]
        g = new.sort_values('gross',ascending=False).apply(lambda x : x.head(math.ceil(len(x) * p)))
        b = b.append(g)
    new = pd.merge(b,data_i,on = 'url',how='left')
    genres = new.loc[:,'Action':'Western'].columns.tolist()
    result = new.groupby('title_year')[genres].sum()
    result['Avg_Imdb'] = new.groupby('title_year')['imdb_score'].mean()
    return result

#bonus_q4(data_m)


#Bonus Q5
#Bucket the movies into deciles using the duration. Generate the report that tracks various features like
#nomiations, wins, count, top 3 geners in each decile.

def bonus_q5(df):
    df['decile'] = pd.qcut(df['duration'], q=10,labels=False)
    data = df.groupby(['decile']).agg({'Action':[np.sum], 'Adult':[np.sum], 'Adventure':[np.sum], 'Animation':[np.sum],
    'Biography':[np.sum], 'Comedy':[np.sum], 'Crime':[np.sum],'Documentary':[np.sum], 'Drama':[np.sum], 'Family':[np.sum], 
    'Fantasy':[np.sum], 'FilmNoir':[np.sum], 'GameShow':[np.sum], 'History':[np.sum], 'Horror':[np.sum], 'Music':[np.sum], 
    'Musical':[np.sum], 'Mystery':[np.sum], 'News':[np.sum], 'RealityTV':[np.sum], 'Romance':[np.sum], 'SciFi':[np.sum], 
    'Short':[np.sum], 'Sport':[np.sum], 'TalkShow':[np.sum], 'Thriller':[np.sum], 'War':[np.sum], 'Western':[np.sum]})
    
    #renaming the columns
    data.columns = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime','Documentary', 'Drama', 'Family',
    'Fantasy', 'FilmNoir', 'GameShow', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'RealityTV', 
    'Romance', 'SciFi', 'Short', 'Sport', 'TalkShow', 'Thriller', 'War', 'Western']
    df1 = df.groupby(['decile'],as_index=False).agg({'nrOfNominations':[np.sum],'nrOfWins':[np.sum]})

    x=pd.DataFrame(data).T
    rslt = pd.DataFrame(np.zeros((0,3)), columns=['top1','top2','top3'])
    for i in x.columns:
        dfrow = pd.DataFrame(x.nlargest(3, i).index.tolist(), index=['top1','top2','top3']).T
        rslt = pd.concat([rslt, dfrow], axis=0)
    rslt = rslt.reset_index(drop=True)
    df1['top_3_genre'] = rslt.apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
    return df1

#bonus_q5(data_i)