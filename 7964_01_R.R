library(readxl)
library(dplyr)
library(lubridate)

excel_sheets('SaleData.xlsx')
de <- read_excel('SaleData.xlsx',sheet = 'Sales Data')

# Q1 Find least sales amount for each item
least_sales <- function(de)
{
  de1 <- aggregate(de$Sale_amt, by=list(Item=de$Item), FUN=min)
  de1 <- rename(de1,Min_Amt=x)
  return(de1)
}
#print(least_sales(de))

# Q2 compute total sales at each year X region
sales_year_region <- function(de)
{
  de2 <- mutate(de, Year = as.numeric(format(OrderDate,'%Y')))
  de2 <- de2 %>% group_by(Year,Region) %>% summarise( TotalSales = sum(Sale_amt,na.rm = TRUE))
  return(de2)
}
#print(sales_year_region(de))

# Q3 append column with no of days difference from present date to each order date
days_diff <- function(de)
{
  de3 <- mutate(de, days_diff = Sys.Date() - as.Date(OrderDate))
  return(de3)
}
#print(days_diff(de))

# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
mgr_slsmn <- function(de)
{
  sel <- select(de,Manager,SalesMan)
  sel <- unique(sel)
  de4 <- aggregate(sel$SalesMan, by = list(manager = sel$Manager), paste, collapse=",")
  de4 <- rename(de4, list_of_salesmen=x)
  return(de4)
}
#print(mgr_slsmn(de))

# Q5 For all regions find number of salesman and total sales
slsmn_units <- function(df){
  de5 <- df %>% group_by(Region) %>% summarise(total_sales = sum(Sale_amt))
  de6 <- df %>% group_by(Region) %>% count(SalesMan) %>% summarise(salesmen_count = sum(n))
  de5 <- merge(de5,de6)
  return(de5)
}
#print(slsmn_units(de))

# Q6 Find total sales as percentage for each manager
sales_pct <- function(de){
  de7 <- de %>% group_by(Manager) %>% summarise(total_sales = sum(Sale_amt))
  de7$percent_sales <- de7$total_sales/sum(de7$total_sales)
  de7 <- de7 %>% select(Manager,percent_sales)
  return(de7)
}
#print(sales_pct(de))

data <- read.csv('movie_metadata.csv')

# Q7 get imdb rating for fifth movie of dataframe
fifth_movie <- function(data)
{
  data1 <- data[5,] %>% select(imdb_score)
  return(data1)
}
#print(fifth_movie(data))

# Q8 return titles of movies with shortest and longest run time
movies <- function(data)
{
  data2 <- data %>% filter(duration == min(as.numeric(as.character(data$duration)),na.rm = TRUE)) %>% select(movie_title)
  data3 <- data %>% filter(duration == max(as.numeric(as.character(data$duration)),na.rm = TRUE)) %>% select(movie_title)
  data2 <- rbind(data2,data3)
  return(data2)
}
#print(movies(data))

# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
sort_df <- function(data)
{
  data4 <- arrange(data,title_year,desc(imdb_score))
  return((data4))
}
#print(sort_df(data))

# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
subset_df <- function(data)
{
  data5 <- subset(data, gross > 2000000 & budget < 1000000 & duration >= 30 & duration <= 180)
  return(data5)
}
#print(subset_df(data))

df<-read.csv("diamonds.csv")

#Q11 count the duplicate rows of diamonds DataFrame.
dupl_rows <- function(df)
{
  df1 <- sum(duplicated(df))
  return(df1)
}
#print(dupl_rows(df))

#Q12 droping those rows where any value in a row is missing in carat and cut columns
drop_row <- function(df)
{
  df2 <- na.omit(df, cols=c("carat", "cut"))
  return(df2)
}
#print(drop_row((df)))

# Q13 subset only numeric columns
sub_numeric <- function(df)
{
  df3 <- df[,sapply(df,is.numeric)]
  return(df3)
}
#print(sub_numeric(df))

# Q14 compute volume as (x*y*z) when depth > 60 else 8
volume <- function(df)
{
  df$volume <- ifelse(df$depth > 60,((as.numeric(as.character(df$x))) * (as.numeric(as.character(df$y))) * (as.numeric(as.character(df$z)))),8)
  return(df)
}
#print(volume(df))

#Q15 impute missing price values with mean
impute <- function(df)
{
  df$price <- ifelse(is.na(df$price),mean(df$price, na.rm = TRUE),df$price)
  return(df)
}
#print(impute(df))
