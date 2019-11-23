import time
import pandas as pd

# used to explicitly display the data frame when using df.head()
from IPython.display import display

# this is used to unlimit the number of raws and columns when printing Pandas data frames
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

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

    # list of cities to be used to ensure currect user input in the while loop
    cities = ['chicago', 'new york city', 'washington']

    # list of months to be used to ensure currect user input in the while loop
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    # list of months to be used to ensure currect user input in the while loop
    days = ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday']

    # get user input for city (chicago, new york city, washington)
    city = input("Please choose the city you want to explore its data\n").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("For which month do you want the data ?, or write 'all' for all months\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please choose the day of the week you desire, or write 'all' for all days\n").lower()

    # this loop is used to make sure the user input for city, month and day is correct, it's condition is True only if one of them is not correct
    while city not in cities or month not in months or day not in days:
        if city not in cities:
            city = input('Invalid city input, please make sure you choose one of the three following cities: chicago, new york city, washington and make sure the spelling is right\n').lower()
        if month not in months:
            month = input("Invalid month input, please make sure it's one of the following choices: all, january, february, march, april, may, june and make sure the spelling is right\n").lower()
        if day not in days:
            day = input("Invalid day input, please make sure it's one of the following choices: all, saturday, sunday, monday, theusday, wednesday, thursday and make sure the spelling is right\n").lower()



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

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

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


def time_stats(df, month, day):

    """
    Displays statistics on the most frequent times of travel.

    Args:
    (str) month - name of the month chosen by the user
    (str) day - name of the day of week chosen by the user
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if the user didn't choose a certain month

    if month == 'all':
        most_common_month = df['month'].mode()[0]
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        print('The most common month is {}'.format(months[most_common_month-1].title()))

    # display the most common month if the user chose a certain month
    else:
        print("The most common month couldn't be calculated, as the data is already filtered to show {} values only".format(month.title()))


    # display the most common day of week if the user didn't choose a certain day
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0]
        print('The most common day of week is {}'.format(most_common_day.title()))

    # display the most common day of week if the user didn't choose a certain day
    else:
        print("The most common day of week couldn't be calculated, as the data is already filtered to show {} values only".format(day.title()))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is {}\n' .format(most_common_hour))

    # printing the time it took to calculate most common month, day and hour
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station is: {}'. format(most_common_end_station))

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: {}' .format(most_common_start_station))

    # create a new column for start and end station combined, the hash symbol '#' is used to split the start and end station when needed
    Combined_Start_End_Station = df['Start Station'] +'#'+ df['End Station']

    # display most frequent combination of start station and end station trip
    most_frequent_combination_of_stations = Combined_Start_End_Station.mode()[0].split('#')
    print('The most frequent combination of start and end station is: \nStart Station: {}\nEnd Station: {}' .format(most_frequent_combination_of_stations[0],most_frequent_combination_of_stations[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total  travel  time is: {} seconds' .format(total_travel_time))

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print('The average trip duration is: {} seconds' .format(mean_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user types are:\n{}\n' .format(user_types))

    # to filter the city that doesn't have this column
    if 'Birth Year' in df.columns:
    # Display earliest, most recent, and most common year of birth
        birth_years = df['Birth Year'].dropna().astype('int64')
        print('The earliest birth year is: {}\nThe most resent birth year is: {}\nThe most common birth year is: {}' .format(birth_years.min(), birth_years.max(), birth_years.mode()[0]))
        print()

    # to filter the city that doesn't have this column
    if 'Gender' in df.columns:
    # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print(gender_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def df_printing_func(df):
    # n is the number of raws to be printed, by dafault it's 5
    n = 5
    while True:

        display(df.head(n))
        more_raws = input('\nDo you want to print more raws ? Enter yes or no.\n')
        if more_raws.lower() != 'yes':
            break
        #if the user types yes, number of raws increase by 5 to print 5 more raws
        n = n + 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        trip_duration_stats(df)
        station_stats(df)
        user_stats(df, city)

        df_printing_func(df)
        df.head()
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
