from datetime import (
   datetime,
   timedelta
)
from typing import Any


def convert_to_dict_format(data:Any) -> dict:
   data_dict,d = dict() , dict()
   
   for data in data:
      attendence_date = datetime.strftime(data.attendence.date,"%Y-%m-%d")
      if attendence_date in data_dict.keys():
            d = data_dict[attendence_date]
            d[len(d.keys())+1] = [data.check_in,data.check_out,data.total_hours]
      else:
         d = {1:[data.check_in,data.check_out,data.total_hours]}
      data_dict[attendence_date] = d
   return data_dict

def get_dates_ranges(startWeekDate):
   if isinstance(startWeekDate,str):
      startWeekDate = datetime.strptime(startWeekDate,"%d-%m-%Y")
      
   date_ranges = (
      startWeekDate + timedelta(days = d) 
      for d in range(7)  
   )
   return date_ranges