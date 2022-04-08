from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *
import time, datetime
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from .forms import *
# Register your models here.
admin.site.site_header = 'ગુજરાત મત્સ્યઉધોગ'                    # default: "Django Administration"
admin.site.index_title = 'ગુજરાત મત્સ્યઉધોગ'  



class BoatAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser == False:
            queryset = BoatManager.get_queryset(self, request)
            return queryset
        return Boat_Details.objects.all()

    def changelist_view(self, request, **kwargs):
        user = request.user
        if user.is_superuser == False:
                self.list_display = (
            'boat_name','boat_number','lisence_number','port_name','boat_material','dimension_length','dimension_breadth','dimension_depth','engine_name','engine_number','engine_manufacture_date','engine_horsepower','owner_details'
                )
            # make_log('non-super user')
        else:
            self.list_display = (
               'boat_name','boat_number','lisence_number','port_name','boat_material','dimension_length','dimension_breadth','dimension_depth','engine_name','engine_number','engine_manufacture_date','engine_horsepower','owner_details'
            )
            # make_log('superuser')
        return super(BoatAdmin, self).changelist_view(request, **kwargs)

    fieldsets = [
        (None,{'fields':('boat_name','boat_number','lisence_number','port_name','boat_material','dimension_length','dimension_breadth','dimension_depth','engine_name','engine_number','engine_manufacture_date','engine_horsepower','owner_details')}),
        ]
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_at', None) is None:
            obj.created_by = request.user
            obj.created_at = int(time.time())
        obj.updated_by = request.user
        obj.updated_at = int(time.time())
        obj.save()

    def created_At(self, obj):
        query = Boat_Details.objects.filter(id=obj.pk).get()
        date = datetime.datetime.fromtimestamp(query.updated_at)
        return f"{date:%d-%b-%Y}"
    
    def updated_At(self, obj):
        query = Boat_Details.objects.filter(id=obj.pk).get()
        date = datetime.datetime.fromtimestamp(query.updated_at)
        return f"{date:%d-%b-%Y}"


from django.contrib.auth.decorators import permission_required

class TokenAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields':('fishing_lisence_number','location_of_operation','date_depature','tentative_date','quantity_water','quantity_fuel','owner')}),
    ]
    def get_queryset(self, request):
        if request.user.is_superuser == False:
            queryset = BlogManager.get_queryset(self, request)
            return queryset
        return Token_Book.objects.all()

    def changelist_view(self, request, **kwargs):
        user = request.user
        if user.is_superuser == False:
                self.list_display = (
            'fishing_lisence_number','location_of_operation','token_number','date_depature','tentative_date','quantity_water','quantity_fuel','owner','number_of_crew','approved',
                )
            # make_log('non-super user')
        else:
            self.list_display = (
                'fishing_lisence_number','location_of_operation','token_number','date_depature','tentative_date','quantity_water','quantity_fuel','owner','number_of_crew','result'
            )
            # make_log('superuser')
        return super(TokenAdmin, self).changelist_view(request, **kwargs)


    def save_model(self, request, obj, form, change):
        user_id = request.user
        query = Boat_Details.objects.filter(owner_details=request.user).get()
        query2 = Crew.objects.filter(boat=query.id).count()
        obj.number_of_crew = query2
        if getattr(obj, 'created_at', None) is None:
            obj.created_by = request.user
            obj.created_at = int(time.time())
            
        query = Boat_Details.objects.filter()
        obj.updated_by = request.user
        obj.updated_at = int(time.time())
        obj.save()


    def created_At(self, obj):
        query = Token_Book.objects.filter(id=obj.pk).get()
        date = datetime.datetime.fromtimestamp(query.updated_at)
        return f"{date:%d-%b-%Y}"
    
    def updated_At(self, obj):
        print('ob',obj)
        query = Token_Book.objects.filter(id=obj.pk).get()
        date = datetime.datetime.fromtimestamp(query.updated_at)
        return f"{date:%d-%b-%Y}"
        

    def result(self, obj):
        obj = Token_Book.objects.get(id = obj.id)

        if(obj.approved == 0):
            return mark_safe('<div class="btn-group" role="group" aria-label="Basic example"><a type="button" class="btn btn-sm btn-success" id="myButton%s" onclick="myFunction(%s)">Approve</a> <a type="button" onclick="myFunctions(%s)" class="btn btn-sm btn-danger" id="myButton2%s">Rejected</a></div>'%(obj.pk, obj.pk, obj.pk, obj.pk))
        else:
            return mark_safe('<div class="btn-group" role="group" aria-label="Basic example"><a type="button" class="btn btn-sm btn-success" id="myButton%s" onclick="myFunction(%s)">Approved</a><a type="button" onclick="myFunctions(%s)" class="btn btn-sm btn-danger" id="myButton2%s">Reject</a></div>'%(obj.pk, obj.pk, obj.pk, obj.pk))
    

    # def get_ordering(self, request):
    
        # else:
        #     return ['fishing_lisence_number','location_of_operation','token_number','date_depature','tentative_date','quantity_water','quantity_fuel','owner','number_of_crew']

class CrewAdmin(admin.ModelAdmin):
    list_display = ['first_name','middle_name','last_name','aadhar_number','phone_number','alternate_number','email','address','boat','created_by','updated_by','created_At','updated_At']
    fieldsets = [
        (None, {'fields':('first_name','middle_name','last_name','aadhar_number','phone_number','alternate_number','email','address','boat')}),
        ]
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_at', None) is None:
            obj.created_by = request.user
            obj.created_at = int(time.time())
        obj.updated_by = request.user
        obj.updated_at = int(time.time())
        obj.save()

    def created_At(self, obj):
        query = Crew.objects.filter(id=obj.pk).get()
        date = datetime.datetime.fromtimestamp(query.created_at)
        return f"{date:%d-%b-%Y}"
    
    def updated_At(self, obj):
        query = Crew.objects.filter(id=obj.pk).get()
        date = datetime.datetime.fromtimestamp(query.updated_at)
        return f"{date:%d-%b-%Y}"

class BoatdetailAdmin(admin.ModelAdmin):
    list_display = ['fishing_lisence_number','token_number','location_of_operation','date_depature','tentative_date','quantity_fuel','owner','number_of_crew']

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','phone_number','alternate_number','address','email','aadhar_number','username', 'password1', 'password2','is_active','is_staff', 'is_superuser',
                                        'groups', 'user_permissions'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Boat_Details,BoatAdmin)
admin.site.register(Token_Book,TokenAdmin)
admin.site.register(Crew,CrewAdmin)