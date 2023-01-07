import time
import pandas as pd
import numpy as np

# CITY_DATA dict (maps cities to csv files that store the bikeshare data)
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# WEEKDAYS dict (maps weekday names to weekday numbers that are used within the dataframe)
WEEKDAYS = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

# MONTHS dict (maps month names to month numbers that are used within the dataframe )
MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).

    while True:
        city = input("\nFor which city would you like to explore bikeshare data? \n\
Please enter Chicago, New York City or Washington. \n\
> ")
        if city.lower() in CITY_DATA.keys():
            break
        else:
            print("\nYour input was not valid.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month would you like to explore? \nPlease enter a month name \
(January, February, March, April, May or June) or enter all for all months. \n> ")
        if month.lower() in MONTHS.keys() or month.lower() == "all":
            break
        else:
            print("\nYour input was not valid.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich weekday would you like to explore? \nPlease enter a weekday name \
(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday) or enter all to look at all weekdays. \n> ")
        if day.lower() in WEEKDAYS.keys() or day.lower() == "all":
            break
        else:
            print("\nYour input was not valid.")

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time to datetime and extract month and day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filter df on month
    if month != 'all':
        month = MONTHS[month]
        df = df[df['month'] == month]

    # filter df on weekday
    if day != 'all':
        day = WEEKDAYS[day]
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    top_month = df['month'].mode()[0]
    print("The most frequent month is: {}".format(top_month))

    #TODO: Check if output should be name or index of weekday and check if filtering is correct
    # display the most common day of week
    top_weekday = df['day_of_week'].mode()[0]
    print("The most frequent weekday is: {}".format(top_weekday)) 

    # display the most common start hour
    top_start_hour = df['hour'].mode()[0]
    print("The most frequent start hour is: {}".format(top_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start_station = df['Start Station'].mode()[0]
    print("The most common Start Station is: {}".format(top_start_station)) 

    # display most commonly used end station
    top_end_station = df['End Station'].mode()[0]
    print("The most common End Station is: {}".format(top_end_station)) 

    # display most frequent combination of start station and end station trip
    df["Start-End Station"] = "(" + df['Start Station'] + ", " + df['End Station'] + ")"
    top_start_end_station = df['Start-End Station'].mode()[0]
    print("The most frequent combination of Start and End Station is: {}".format(top_start_end_station)) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is {} seconds".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is {} seconds".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types (also check if Gender is contained in dataframe)
    user_counts = df['User Type'].value_counts().to_string(name=False, dtype=False)
    print("These are the number of users per User Type: \n{}".format(user_counts))

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts().to_string(name=False, dtype=False)
        print("\nThese are the number of users per Gender: \n{}".format(gender_counts))
    else:
        print("Cannot provide statistics on Gender because this is not available for the chosen city.")

    # Display earliest, most recent, and most common year of birth (also check if Birth Year is contained in dataframe)
    if 'Birth Year' in df:
        earliest_YOB = int(df['Birth Year'].min())
        latest_YOB = int(df['Birth Year'].max())
        most_frequent_YOB = int(df['Birth Year'].mode()[0])
        print("The earliest year of birth is {}".format(earliest_YOB))
        print("The most recent year of birth is {}".format(latest_YOB))
        print("The most frequent year of birth is {}".format(most_frequent_YOB))
    else:
        print("Cannot provide statistics on Birth Year because this is not available for the chosen city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_display(df, num_rows_per_promt=5):
    """
    Displays raw data in df in chunks as longer as user chooses to view more data.

    Args:
        (str) df - data frame to view
        (int) num_rows_per_prompt - number of rows to show at once (default=5)
    """

    show_raw_data = input("Would you also like to see {} trips for your chosen filters (yes/no)?\n>".format(num_rows_per_promt))
    if show_raw_data.lower() == "yes":
        row_number = 0
        while show_raw_data == "yes":
            display_completed = False
            for i in range(num_rows_per_promt):
                 print(df.iloc[row_number].to_string()) # print each df row individually using to_string() method (looks ok in shell) 
                 print("\n")
                 if row_number >= df.shape[0] - 1: # if all rows have been shown, stop displaying data
                    display_completed = True
                    break
                 row_number += 1
            if display_completed:
                break
            show_raw_data = input("Would you like to see 5 more trips (yes/no)?\n>").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
