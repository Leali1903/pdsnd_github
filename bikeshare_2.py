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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ' '
    while city not in ('chicago', 'new york city', 'washington'):
       city = input("\nWhich city do you wanna explore? Choose one of the cities: Chicago, New York City or Washington\n").lower()
       if city not in ('chicago', 'new york city', 'washington'):
           print("\nPlease enter a valid city out of the cities mentioned.")
    # get user input for month (all, january, february, ... , june)
    month = ' '
    while month not in ('all', 'january', 'february','march', 'april', 'may', 'june'):
       month = input("\nWhich month do you want to take a look at? Choose a month or all.\n").lower()
       if month not in ('all', 'january', 'february','march', 'april', 'may', 'june'):
           print("\nPlease enter a valid month between january and june or select all.")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ' '
    while day not in ('all', 'monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
       day = input("\nWhich day of the week do you want to take a look at? Choose a day (e.g. monday) or all.\n").lower()
       if day not in ('all', 'monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
           print("\nPlease enter a valid weekday or select all.")

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

    # display the most common month
    # as this only makes sense if the month are set to all: 
    if df['month'].nunique() > 1:
        popular_month = df['month'].mode()[0]
        print("\nThe most common month of travel is {}.\n".format(popular_month))
    else: 
        print("\nThere is only one month that you selected. Hence that month is the most common month of travel. This month and the most common month of travel is {}.".format(df['month'].nunique()))

    # display the most common day of week
    # as this only makes sense if the month are set to all: 
    if df['day_of_week'].nunique() > 1:
        popular_day = df['day_of_week'].mode()[0]
        print("\nThe most common day of travel is {}.\n".format(popular_day))
    else: 
        print("\nThere is only one weekday that you selected. Hence, that is the most common day of travel. The day you chose and most common day of travel is {}.".format(df['day_of_week'].nunique()))     

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe most common hour of the day to start the travel is {}.\n".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("\nThe most common start station for the travel is {}.\n".format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("\nThe most common end station for the travel is {}.\n".format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("\nThe most common trip (i.e. combination of start and end station) for the travel is {}.\n".format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()/60/60
    print("\nThe total travel time in the timeframe is {} hours.\n".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print("\nThe average travel time in the timeframe is {} minutes.\n".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nThe counts of the different user types are: {}.\n".format(user_types))
    
    # Display counts of gender
    # catch that gender is in dataset
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print("\nThe user had the following the gender: {}.\n".format(gender))
    else: 
        print("\nNo gender data available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year_early = df['Birth Year'].min().astype(int)
        birth_year_recent = df['Birth Year'].max().astype(int)
        birth_year_common = df['Birth Year'].mode()[0].astype(int)
        print("\nThe oldest user(s) were born in {}, the youngest in {} and the most common year of birth is {}.\n".format(birth_year_early, birth_year_recent, birth_year_common))
    else: 
        print("\nNo birth year data available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(dataframe, lines):
    """ Provides the user with "lines" amount rows of data as long as he requests to see (more) data 
    or until no more data is there to display.
    
    Args:
    (dataframe) dataframe - data that should be displayed chunkwise
    (int) lines - amount of lines that should be displayed at a time
    """
    start_val = 0
    total_len = len(dataframe)

    while start_val < total_len:
        # Ask user if they want to see more data
        raw_data = input("\nWould you like to see some (more) lines of raw data? Enter yes or no.\n"
        ).strip().lower()

        if raw_data == "yes":
            # Print next chunk (even if fewer `lines` remain)
            end_val = min(start_val + lines, total_len)
            print(dataframe.iloc[start_val:end_val])
            start_val = end_val
        elif raw_data == "no":
            print("\nOkay, stopping data display.")
            break
        else:
            print("\nInvalid input. Please answer with 'yes' or 'no'.")
            # make sure to reprompt
            continue

    if start_val >= total_len:
        print("\nNo more data to display.")
    

def main():
    """Runs all above functions in the right order starting with the user input. """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df, 5)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('That\'s okay, see you next time you wanna explore some more bikesharing stats.')
            break


if __name__ == "__main__":
	main()
