from datetime import datetime, timedelta
from typing import Union, Set


def process_str_date(start: str = None, end: str = None) -> Union[str, Set[datetime]]:
    start_date = None
    end_date = None

    if start == None and end == None:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

    if start != None and end == None:
        end_date = datetime.now()

    if start == None and end != None:
        return "start date not provided"

    if start_date == None:
        try:
            start_date =  datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f')
        except Exception as e:
            return "start date format is not correct"
    if end_date == None:
        try:
            end_date =  datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%f')
        except Exception as e:
            return "end date format is not correct"

    return start_date, end_date