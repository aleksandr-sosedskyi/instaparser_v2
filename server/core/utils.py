import re

from django.utils import timezone


def parse_user_data(s):
    # Initializate variables
    arr = []
    colon_counter = 0
    last_split_index = 0
    user = {}

    # Patterns for id:username:subscribers:subscriptions
    patterns = {
        0: re.compile(r"\d{7,13}"),
        1: re.compile(r"[\w.]*"),
        2: re.compile(r"\d{1,11}"),
        3: re.compile(r"\d{1,11}"),
    }

    # Iterate by data-string
    for index, value in enumerate(s):
        if index < last_split_index:
            continue 
        if value == ":":
            # Collect id, username, subscribers
            if colon_counter in (0,1,2):
                string = s[last_split_index:index]
                if not patterns[colon_counter].fullmatch(string):
                    end_of_string_pattern = r" \d{7,13}:[\w.]*:\d{1,12}:\d{1,12}.+"
                    string = re.search(end_of_string_pattern, s[index+1:])
                    if not string:
                        print(index)
                        break
                    else:
                        last_split_index = index + 2 + string.start()
                        user = {}
                        colon_counter = 0
                        continue
                user[colon_counter] = string
                colon_counter += 1
                last_split_index = index + 1
                continue

            # Collect subscriptions, name, phone, email, city
            if colon_counter == 3:

                # Check for subscriptions
                string = s[last_split_index:index]
                if not patterns[colon_counter].fullmatch(string):
                    end_of_string_pattern = r" \d{7,13}:[\w.]*:\d{1,12}:\d{1,12}.+"
                    string = re.search(end_of_string_pattern, s[index+1:])
                    if not string:
                        break
                    else:
                        last_split_index = index + 2 + string.start()
                        user = {}
                        colon_counter = 0
                        continue
                user[colon_counter] = string

                # Check if it the last user
                last_element = False
                end_of_string_pattern = r" \d{7,13}:[\w.]*:\d{1,12}:\d{1,12}.+"
                string = re.search(end_of_string_pattern, s[index+1:])
                if not string:
                    last_element = True 
                
                # If user is the last split by last 3 colons 
                # The -1 colon is city
                # The -2 colon is email 
                # The -3 colon is phone 
                # All from phone to subscriptions is the name doesn't matter what it includes
                if last_element:
                    string = s[index+1:]
                    if string.count(':') == 3:
                        user[4], user[5], user[6], user[7] = string.split(':')
                    elif string.count(':') < 3:
                        break
                    elif string.count(':') > 3:
                        string_arr = string.split(':')
                        user[7] = string_arr.pop()
                        user[6] = string_arr.pop()
                        user[5] = string_arr.pop()
                        user[4] = ':'.join(string_arr)
                        
                # Find the space-delimiter between users 
                # Do the same as for the last element
                else:
                    string = re.search(end_of_string_pattern, s[index+1:])
                    found_string = s[index+1:index+1+string.start()]
                    if found_string.count(':') == 3:
                        user[4], user[5], user[6], user[7] = found_string.split(':')
                    elif found_string.count(':') < 3:
                        last_split_index = index + 2 + string.start()
                        user = {}
                        colon_counter = 0
                        continue
                    elif found_string.count(':') > 3:
                        string_arr = found_string.split(':')
                        user[7] = string_arr.pop()
                        user[6] = string_arr.pop()
                        user[5] = string_arr.pop()
                        user[4] = ':'.join(string_arr)

                arr.append(user)
                user = {}
                if last_element:
                    break
                colon_counter = 0
                last_split_index = index + 2 + string.start()
    return arr


def format_date_from_seconds(total_seconds):
    seconds_in_day = 60 * 60 * 24
    seconds_in_hour = 60 * 60
    seconds_in_minute = 60

    days = total_seconds // seconds_in_day
    hours = (total_seconds - (days * seconds_in_day)) // seconds_in_hour
    minutes = (total_seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
    
    formated_date = f"{minutes}m ago"
    if hours:
        formated_date = f"{hours}h " + formated_date
    if days:
        formated_date = f"{days}d " + formated_date

    return formated_date

