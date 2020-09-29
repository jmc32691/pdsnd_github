import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        try:
            city = input("\nChoose a city to explore! (Chicago, New York City, Washington): \n").lower()
            if city in CITY_DATA.keys():
                break
            else:
                print('City is either not spelled properly, or not available in this data set. Please choose from one of the following: Chicago, New York City, Washington') 
        except KeyError as error:
            print('Unfortunately, you have input something wrong: {}'.format(error))

    # TO DO: get user input for month (all, january, february, ... , june)
    
    while True:
        try:
            month = input("\nChoose a month in the first half of the year if desired, or choose all: \n").lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                break
            else:
                print('You must choose a month between January and June, or choose all. Please spell out the month\'s full name, if selecting a month.')
        except KeyError as error:
            print('Unfortunately, you have input something wrong: {}'.format(error))
                
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("\nChoose a day of the week if you would like to focus on one; if not, input all: \n").lower()
            if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
                break
            else:
                print('Please spell out the weekday\'s full name if specifying a weekday. If not, choose \"all\".')
        except KeyError as error:
            print('Unfortunately, you have input something wrong: {}'.format(error))
            
    
    print('-'*40)
    return city, month, day

    


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print()
    print('Most Frequent Start Month:', popular_month)
    
    
    # TO DO: display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print()
    print('Most Frequent Start Day of Week:', popular_dow)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print()
    print('Most Frequent Start Hour:', popular_hour)
    print()
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print()
    print('Most Frequent Start Station:', popular_start)
    
    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print()
    print('Most Frequent End Station:', popular_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'].str.cat(df['End Station'], sep =" + ")
    popular_combo = df['Station Combo'].mode()[0]
    print()
    print('Most Frequent Combo of Start Station and End Station trip: ', popular_combo)
    print()
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    total_duration_min = (total_duration / 60).round(2)
    print()
    print('Total Travel Time: {} minutes'.format(f"{total_duration_min:,}"))


    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean()
    mean_duration_min = (mean_duration / 60).round(2)
    print()
    print('Average Travel Time: {} minutes'.format(mean_duration_min))
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df['User Type'].value_counts()
    print()
    print('User Counts: There are {} subscribers and {} customers.'.format(f"{user_counts['Subscriber']:,}", f"{user_counts['Customer']:,}"))


    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print()
        print('Gender Counts: There are {} males and {} females.'.format(f"{gender_counts['Male']:,}", f"{gender_counts['Female']:,}"))
    else:
        print()


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print()
        print('Birth Year Counts: The earliest birth year is {}. \n - The most recent birth year is {}. \n - The most common year of birth is {}.'.format(earliest_year, recent_year, common_year))
        print()
    else:
        print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        start = 0
        end = 5
        
        while True:
            raw_data = input('\nWould you like to see some of the raw data? Answer yes or no. \n')
            if raw_data.lower() == 'no':
                break
            else:
                print(df[start:end])
                start += 5
                end += 5
            
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
