# Standard Import
from datetime import datetime
import json

# Django Import
from django.http import JsonResponse
from django.http import HttpResponse

# Local Import 
from ..models import Attendence


def record_attendence(request,**kwargs):
   in_time = float(request.POST.get('checkin_time'))
   out_time = float(request.POST.get('checkout_time'))
   work_time = request.POST.get('ttl_work_time')
   checkin_date = request.POST.get('checkin_date')
   parse_in_time = datetime.fromtimestamp(in_time)
   parse_out_time = datetime.fromtimestamp(out_time)
   get_parsed_in_time = f'{parse_in_time.hour}:{parse_in_time.minute}:{parse_in_time.second}'
   get_parsed_out_time = f'{parse_out_time.hour}:{parse_out_time.minute}:{parse_out_time.second}'
   create_record = Attendence.objects.create(
      user = request.user,
      date = checkin_date,
      checkin_time = get_parsed_in_time,
      checkout_time = get_parsed_out_time,
      ttl_work_time = work_time  
   )
   return HttpResponse(
         json.dumps({
            'attendence_recorded':True,}),
            content_type="application/json")
 
def day_checkin_available(request,date):
   """
      Function will check if the attendence is already made for the day.
      Executes when a user click's a check-in button for the second time in a day.

   """
   filter_record = Attendence.objects.filter(user=request.user,date=date)
   if filter_record.exists():
      get_record = filter_record.get('id','checkout_time','ttl_work_time')
      return HttpResponse({
         json.dumps({
            'attendence_available':True,
            'message':get_record.id,
            'response_data':{
               'checkout_time':get_record.checkout_time,
               'ttl_work_hr':get_record.ttl_work_time
            }     
         })
      })
   else:
      return HttpResponse({
         json.dumps({
            'attendence_available':False,
            'message':None,
            'response_data':None
         })
      })
   