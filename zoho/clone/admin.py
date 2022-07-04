from django.contrib import admin

from .models import (
   Department,
   EmpSelf,
   EmpPersonal,
   LeavesAndHolidays,
   LeavesCreateModel,
   LeaveType,
   TimeTracker,
   Attendence,
   DailyAttendenceRecords
)

class AttendenceAdmin(admin.ModelAdmin):
   list_display =  [
      'id', 
      'date', 
      'user'
   ]

class AttendenceRecordsAdmin(admin.ModelAdmin):
   list_display = [
      'id',
      'attendence', 
      'check_in',
      'check_out', 
      'total_hours'
   ]
admin.site.register(Department)
admin.site.register(EmpSelf)
admin.site.register(EmpPersonal)
admin.site.register(LeavesCreateModel)
admin.site.register(LeavesAndHolidays)
admin.site.register(LeaveType)
admin.site.register(TimeTracker)
admin.site.register(Attendence,AttendenceAdmin)
admin.site.register(DailyAttendenceRecords,AttendenceRecordsAdmin)