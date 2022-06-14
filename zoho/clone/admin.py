from django.contrib import admin

from .models import (
   Department,
   EmpSelf,
   EmpPersonal,
   LeavesCreateModel,
   LeavesAndHolidays,
   LeaveType
)

admin.site.register(Department)
admin.site.register(EmpSelf)
admin.site.register(EmpPersonal)
admin.site.register(LeavesCreateModel)
admin.site.register(LeavesAndHolidays)
admin.site.register(LeaveType)