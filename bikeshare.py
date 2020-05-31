    """Displays statistics of the bike sharing data"""
import time
import sys
import calendar
import pandas as pd
import numpy as np
    """Copyrights are belonging to me!"""
global CITY_DATA

CITY_DATA = { 'chicago': 'chicago.csv',
              'newyork': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_day():
    """
    asks user to specify day of the week
    Returns:
        (int) day - day of the week as an integer number
    """
    day = -1
    while day < 0 or day > 6:
          day = int(input("Which day ? Please type your response as an integer (e.g., Monday=0)\n"))
          if day < 0 or day > 6:
              print("Monday=0, Tuesday=1, Wednesday=2...")

    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global CITY_DATA

    city = ""
    while not city in CITY_DATA.keys():
           city = input('Would you like to see data for Chicago, NewYork, or Washington ?\n').lower()
           if not city in CITY_DATA.keys():
               print("please choose [Chicago, NewYork, or Washington] ;)")

    times = ["day","month","both","none"]
    timefil = ""
    while not timefil in times:
           timefil = input('Would you like to filter data by month, day, both, or not at all? Type "none" for no time filter.\n').lower()
           if not timefil in times:
               print("please choose [month, day, both, or none] ;)")


    allmonths = list(calendar.month_name[1:])

    month = 0
    day = -1
    if timefil == "month" or timefil == "both":
        while month < 1 or month > 6:
           month = int(input("Which month ? Please type your response as an integer max.6 (e.g., January=1, February=2...)\n"))
           if month < 1 or month > 6:
               print("January=1, February=2, March=3, April=4...max.6 because no data after June :))")

        if timefil == "both":
            day = get_day()

    if timefil == "day":
        day = get_day()

    if timefil == "none":
        month = 0
        day = -1

    print('Hello! Let\'s explore some US bikeshare data!')

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
    global CITY_DATA

    data_file = CITY_DATA[city]
    df = pd.read_csv(data_file)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday

    if month != 0:
        df = df[df['month'] == month]

    if day != -1:
        df = df[df['weekday'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', calendar.month_name[popular_month])

    # TO DO: display the most common day of week
    popular_day = df['weekday'].mode()[0]
    #print('Most Popular Day of Week:', WEEK_DAYS[popular_day])
    print('Most Popular Day of Week:', calendar.day_name[popular_day])

    # TO DO: display the most common start hour
    number_of_hours = df.hour.value_counts()[df['hour'].mode()[0]]

    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour,'Count:',number_of_hours)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly end start station:', end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combin_station = (df['Start Station'] + df['End Station']).mode()[0]
    print('Most frequent combination of start-end station:', combin_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time: ',total_travel)

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Mean travel time: ',mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if city != "washington":
        user_gender = df['Gender'].value_counts()
        print(user_gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    if city != "washington":
        print('Earliest birth year: ',df['Birth Year'].min())
        print('Recent birth year: ',df['Birth Year'].max())
        print('Most common birth year: ',df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_user_data(df):
    """
    this function display data to the user if they want to see
    """
    rows, columns = df.shape
    columns_name = list(df.columns)
    rows_number = list(df.index)

    turn = 0
    print("================================================================")
    while True:
        ask = input('Would you like to view individual trip data ? [Enter yes or no ] ').lower().strip()
        if ask != "yes":
            break

        turn += 1
        start = (turn * 5) - 5
        stop = start + 5

        if start > len(rows_number):
            print(".end of data.")
            break

        if stop > len(rows_number):
            stop = len(rows_number)

        for wi in range(start, stop):
            index = rows_number[wi]
            for rowi in columns_name:
                if 'Unnamed: 0' == rowi:
                    print("{'': "+str(df[rowi][index]))
                else:
                    print("'"+rowi+"': "+str(df[rowi][index]))
            print("}")


def main():

    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        display_user_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
