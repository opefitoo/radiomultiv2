from django.contrib import admin
from models import CareCode, Patient, Employee, JobPosition
from django_admin_bootstrapped.admin.models import SortableInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class CareCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'gross_amount', 'reimbursed')
admin.site.register(CareCode,CareCodeAdmin)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_name','phone_number')
admin.site.register(Patient,PatientAdmin)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(SortableInline, admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
admin.site.register(JobPosition, JobPositionAdmin)