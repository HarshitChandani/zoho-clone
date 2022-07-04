# Standard Import
from datetime import datetime
import json
from typing import Any

# Django Import
from django.http import HttpResponse

# Local Import 
from clone.models import (
   Attendence as attendence ,
   DailyAttendenceRecords
)


class Attendence:
   
   # CHECK-IN
   def record_checkin(self,user:Any,data:dict,**kwargs:Any):
      self.attendence_date = data.get('date')
      self.checkin_time = (float(data.get('checkin'))/1000.0)
      self.action = data.get('action') # in / out

      self.attendence_date = datetime.strptime(self.attendence_date,'%Y-%m-%d')
      parse_time = datetime.fromtimestamp(self.checkin_time)
      get_parsed_in_time = f'{parse_time.hour}:{parse_time.minute}:{parse_time.second}'
      
      # check the record for the given date.
      if attendence.objects.filter(user=user,date=self.attendence_date).exists():
         get_attendence= attendence.objects.get(date=self.attendence_date,user=user)
         is_recorded_created = self.create_attendence_record(
            {
               'attendence_obj': get_attendence,
               'in_time':get_parsed_in_time,
               'status': True
            }
         )
         if is_recorded_created is not None:
            return HttpResponse(
               json.dumps({
                  'record_id':is_recorded_created,
                  'attendence_id':get_attendence.id,
                  'checked_in':True
               })
            ,content_type="application/json")
         else:
            return HttpResponse(
               json.dumps({
                  'record_id':None,
                  'attendence_id':None,
                  'checked_in':False
               })
            ,content_type='application/json')
      else:
         create_attendence = attendence.objects.create(
            user = user,
            date = self.attendence_date
         )
         is_recorded_created = self.create_attendence_record(
            {
               'attendence_obj':create_attendence,
               'in_time':get_parsed_in_time,
               'status': True
            }
         )
         if is_recorded_created is not None:
            return HttpResponse(
               json.dumps({
                  'record_id':is_recorded_created,
                  'attendence_id':create_attendence.id,
                  'checked_in':True
               })
            ,content_type='application/json')
         else:
            return HttpResponse(
               json.dumps({
                  'record_id':None,
                  'attendence_id':None,
                  'checked_in':False
               })
            ,content_type='application/json')

   # CHECK-OUT
   def record_checkout(self,data:dict,**kwargs:Any):
      self.checkout_time = (float(data.get('checkout'))/1000.0)
      self.action = data.get('action')
      self.record_id = data.get('record_id')
      self.attendence_id = data.get('attendence_id')
      self.ttl_work_hr = data.get('ttl_work_hrs')

      self.checkout_time = datetime.fromtimestamp(self.checkout_time)

      DailyAttendenceRecords.objects \
                                 .filter(id=self.record_id) \
                                 .update(
                                    check_out = self.checkout_time,
                                    total_hours = self.ttl_work_hr
                                 )
      return HttpResponse(
            json.dumps({
               'record_id':self.record_id,
               'success':True,
               'message':'successfully checkout'
            })
         ,content_type='application/json')

   def create_attendence_record(self,data:dict):
      create_attendence_record = DailyAttendenceRecords.objects.create(
         attendence = data.get('attendence_obj',None),
         check_in = data.get('in_time',None),
         status = data.get('status',False)
      )
      return (
         create_attendence_record.id 
         if create_attendence_record is not None
         else None
      ) 
   
   def get_attendence_by_weak(self,user,start_date,end_date) -> Any:
      """
         Function will return attendence data of a given week which is 
         specified by the given dates.
      """      
      parse_start_date = datetime.strptime(start_date,"%d-%m-%Y")
      parse_end_date = datetime.strptime(end_date,"%d-%m-%Y")
      
      attendence_data = DailyAttendenceRecords.objects \
                        .select_related('attendence') \
                        .filter(
                           attendence__user = user, 
                           attendence__date__range = [parse_start_date,parse_end_date]
                        ) \
                        .order_by('attendence__date') \
                        .all()

      return attendence_data
      
   def get_attendence_by_id(self,attendence_id) -> Any:
      attendence_data_by_id = DailyAttendenceRecords.objects \
                           .select_related('attendence') \
                           .filter(
                              attendence__id = attendence_id
                           ) 
      return attendence_data_by_id  
                                                
      