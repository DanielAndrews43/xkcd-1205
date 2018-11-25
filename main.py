import sys
import math

# We are going to assume 8 hour days
# We are going to assume 21 day months
converter = {
    "s": 1,
    "m": 60,
    "h": 60*60,
    "d": 60*60*8,
    "M": 60*60*8*21,
    "y": 60*60*8*365,
}

# converter = {
#     "s": 1,
#     "m": 60,
#     "h": 60*60,
#     "d": 60*60*24,
#     "M": 60*60*24*30,
#     "y": 60*60*24*365,
# }

unit_order = ['seconds', 'minutes', 'hours', 'days', 'months', 'years']
unit_key = ['s', 'm', 'h', 'd', 'M', 'y']

def calculate_automation(f, t):
    """
    calculates the number of seconds that you save by automating over 5 years

    f: the number of times you do this per year
    t: the amount of time you save by automating in seconds

    returns number of seconds saved by automation
    """
    return round(5 * f * t)


def number_times_per_year(f, f_unit):
    """
    Calculates the number of times you engage in a task over a given year
    
    f: an int representing the frequency that you engage in a task
    f_unit: the unit of time used for frequency `f`

    return the number of times you complete a task over the course of a year
    """
    return round(f * converter['y'] / converter[f_unit])


def clean_unit(unit):
    """
    Cleans up the unit of value so that it can be used easily with our converter

    unit: a string representing a unit of measurement for time

    returns single letter representation of unit
    """
    return 'M' if unit.lower() == 'month' else unit[0].lower()


def clean_units(units):
    """
    Wrapper function for `clean_unit`. Cleans up the units to be used with our converter.

    units: a list of units to be cleaned

    returns the single letter representation of the unit
    """
    return [clean_unit(unit) for unit in units]

def usable_numbers(time):
    """
    Calculates the value and unit that is most easiy human readable for total time spent

    time: int representing total number of seconds

    returns
        value: the number representing time
        unit: the unit that value is represented in
    """
    curr_val = time
    index = 0

    while index+1 < len(unit_key):
        unit_test = converter[unit_key[index+1]]
        if time // unit_test < 1:
            break
        index += 1

    return time//converter[unit_key[index]], unit_order[index]

def automate_time(f, f_unit, t, t_unit):
    """
    This function will tell you how much time you should spend automating
    given that you do a task n times and it takes t time.

    f: an int representing the frequency that you engage in a task
    f_unit: the unit of time used for frequency `f`
    t: the amount of time it takes to complete a task
    t_unit: the unit of measurement for time for `t`

    returns the number of seconds you should spend to realize gains from automating over 5 years
    """
    f_unit, t_unit = clean_units([f_unit, t_unit])

    num_tasks = number_times_per_year(f, f_unit)

    time_seconds =  t * converter[t_unit]

    total_time = calculate_automation(num_tasks, time_seconds)

    value, unit = usable_numbers(total_time)
    print('You are spending %d %s every 5 years on this task' % (value, unit))
    
    # print("%d times per %s, I spend %d %s doing the task, which is %d seconds per 5 years" % (f, f_unit, t, t_unit, total_time))
    # print("num_tasks: %d, time_seconds: %d" % (num_tasks, time_seconds))
    # print(' ')


# "f times per f_unit, I spend t t_unit doing task"
# automate_time(1, 'year', 1, 'minute')

help_string = '''
This library tells you how long you spend on a repeating task so that you can
make a judgement call as to automate or not. Make sure to follow the correct pattern:

    f times per f_unit I spend t t_unit doing task

    f -> (int) frequency
    f_unit -> (string) frequency unit [second|minute|hour|day|month|year]
    t -> (int) time
    t_unit -> (string) time unit [second|minute|hour|day|month|year]
'''

def main():
    if sys.argv[1] == '-h':
        print(help_string)

    if len(sys.argv) != 9:
        return

    cmd, f, _, _, f_unit, _, _, t, t_unit = sys.argv
    automate_time(int(f), f_unit, int(t), t_unit)

if __name__ == '__main__':
   main()