from datetime import datetime
import re

timeformat = {
    "%d/%m/%Y" : r"\d{1,2}/\d{1,2}/\d{4}",  # "13/8/2024"
    "%b %d, %Y" : r"\w{3} \d{1,2}, \d{4}",  # "Sep 22, 2019"
    "%Y-%m-%d" : r"\d{4}-\d{2}-\d{2}"  # "2024-04-30"
    
}


def todatetime(time_string):
    temp_string = ""
    for key, value in timeformat.items():
        match = re.match(value, time_string)
        if match:
            temp_string = match.group(0)
            datetime_object = datetime.strptime(temp_string, key)
            return datetime_object
            
    return None


# Example usage:
time_string = "13/8/2024"
print(todatetime(time_string))

time_string = "Sep 22, 2019,23,5,44"
print(todatetime(time_string))

time_string = "2024-04-30T07:09:11+07:00"
print(todatetime(time_string))
