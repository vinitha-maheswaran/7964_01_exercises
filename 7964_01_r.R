library(readxl)
library(dplyr)
library(lubridate)

#Reading the required files
excel_sheets('SaleData.xlsx')
data_s <- read_excel('SaleData.xlsx',sheet = 'Sales Data')
data_m <- read.csv('movie_metadata.csv')
data_d<-read.csv("diamonds.csv")


# Q1 Find least sales amount for each item
least_sales <- function(df)
{
  df <- aggregate(df$Sale_amt, by=list(Item=df$Item), FUN=min)
  df <- rename(df,Min_Amt=x)
  return(df)
}
#print(least_sales(data_s))


# Q2 compute total sales at each year X region
sales_year_region <- function(df)
{
  df <- mutate(df, Year = as.numeric(format(OrderDate,'%Y')))
  df <- df %>% group_by(Year,Region) %>% summarise( TotalSales = sum(Sale_amt,na.rm = TRUE))
  return(df)
}
#print(sales_year_region(data_s))


# Q3 append column with no of days difference from present date to each order date
days_diff <- function(df,date)
{
  ref_date <- as.Date(date, format = "%d/%m/%y")
  #print(ref_date)
  df1 <- mutate(df,days_dif = abs(ref_date - as.Date(OrderDate)))
  return(df1)
}
#print(days_diff(data_s,"16/01/2020"))


# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
mgr_slsmn <- function(df)
{
  sel <- select(df,Manager,SalesMan)
  sel <- unique(sel)
  de <- aggregate(sel$SalesMan, by = list(manager = sel$Manager), paste, collapse=",")
  de <- rename(de, list_of_salesmen=x)
  return(de)
}
#print(mgr_slsmn(data_s))


# Q5 For all regions find number of salesman and total sales
slsmn_units <- function(df){
  df1 <- df %>% group_by(Region) %>% summarise(total_sales = sum(Sale_amt))
  df2 <- df %>% group_by(Region) %>% count(SalesMan) %>% summarise(salesmen_count = sum(n))
  df1 <- merge(df2,df1)
  return(df1)
}
#print(slsmn_units(data_s))


# Q6 Find total sales as percentage for each manager
sales_pct <- function(df){
  de <- df %>% group_by(Manager) %>% summarise(total_sales = sum(Sale_amt))
  de$percent_sales <- de$total_sales/sum(de$total_sales)
  de <- de %>% select(Manager,percent_sales)
  return(de)
}
#print(sales_pct(data_s))


# Q7 get imdb rating for fifth movie of dataframe
fifth_movie <- function(df)
{
  data <- df[5,] %>% select(imdb_score)
  return(data)
}
#print(fifth_movie(data_m))


# Q8 return titles of movies with shortest and longest run time
movies <- function(df)
{
  data2 <- df %>% filter(duration == min(as.numeric(as.character(df$duration)),na.rm = TRUE)) %>% select(movie_title)
  data3 <- df %>% filter(duration == max(as.numeric(as.character(df$duration)),na.rm = TRUE)) %>% select(movie_title)
  data2 <- rbind(data2,data3)
  return(data2)
}
#print(movies(data_m))


# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
sort_df <- function(df)
{
  data4 <- arrange(df,title_year,desc(imdb_score))
  return((data4))
}
#print(sort_df(data_m))


# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
subset_df <- function(df)
{
  data5 <- subset(df, gross > 2000000 & budget < 1000000 & duration >= 30 & duration <= 180)
  return(data5)
}
#print(subset_df(data_m))


#Q11 count the duplicate rows of diamonds DataFrame.
dupl_rows <- function(df)
{
  df1 <- sum(duplicated(df))
  return(df1)
}
#print(dupl_rows(data_d))


#Q12 droping those rows where any value in a row is missing in carat and cut columns
drop_row <- function(df)
{
  df2 <- na.omit(df, cols=c("carat", "cut"))
  return(df2)
}
#print(drop_row((data_d)))


# Q13 subset only numeric columns
sub_numeric <- function(df)
{
  df3 <- df[,sapply(df,is.numeric)]
  return(df3)
}
#print(sub_numeric(data_d))


# Q14 compute volume as (x*y*z) when depth > 60 else 8
volume <- function(df)
{
  df$volume <- ifelse(df$depth > 60,((as.numeric(as.character(df$x))) * (as.numeric(as.character(df$y))) * (as.numeric(as.character(df$z)))),8)
  return(df)
}
#print(volume(data_d))


#Q15 impute missing price values with mean
impute <- function(df)
{
  df$price <- ifelse(is.na(df$price),mean(df$price, na.rm = TRUE),df$price)
  return(df)
}
#print(impute(data_d))