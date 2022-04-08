from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    phone_message = 'Phone number must start with either 9, 8, 7 or 6 and should enter in this format: 9999955555'
    phone_regex = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message=phone_message
    )
    ten_digit = '''-> Phone number should be of 10 digits <br/> 
    -> Phone number must starts with either 9, 8, 7 or 6 <br/>
    -> Should enter in this format: 9999955555
    '''
    aadhar_number = models.CharField(max_length=16, unique=True)
    phone_number =  models.CharField(max_length=12,null=False,unique=True, validators=[phone_regex],help_text=ten_digit)
    alternate_number = models.CharField(max_length=12,null=False, unique=True, validators=[phone_regex],help_text=ten_digit)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name_plural = "Owner Details"

from django.contrib.auth.models import  UserManager
class StaffManager(UserManager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_staff=True)


class StaffProxyModel(User):
    objects = StaffManager()
    class Meta:
        proxy = True
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'


class Boat_Details(models.Model):
    MATERIAL_WOOD = 'W'
    MATERIAL_IRON = 'I'
    MATERIAL_FIBER = 'F'

    MATERIAL_CHOISES = [
        (MATERIAL_WOOD,'Wood'),
        (MATERIAL_IRON, 'Iron'),
        (MATERIAL_FIBER, 'Fiber'),
    ]

    boat_name = models.CharField(max_length=255)
    boat_number = models.IntegerField()
    lisence_number = models.CharField(max_length=255)
    port_name = models.CharField(max_length=255) 
    boat_material = models.CharField(max_length=255, choices=MATERIAL_CHOISES)  # remain to add choices
    dimension_length = models.DecimalField(max_digits=6,decimal_places=4,verbose_name='length')
    dimension_breadth = models.DecimalField(max_digits=6, decimal_places=4, verbose_name='breadth')
    dimension_depth = models.DecimalField(max_digits=6, decimal_places=4, verbose_name='depth')
    engine_name = models.CharField(max_length=255)
    engine_number = models.IntegerField()
    engine_manufacture_date = models.DateField(null=True, blank=True,verbose_name='Engine MFD')
    engine_horsepower = models.IntegerField()
    owner_details = models.ForeignKey(User,verbose_name='Owner', on_delete=models.CASCADE, related_name='owner')      
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    created_by = models.ForeignKey(User,related_name='boatcreatedby', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(User, related_name='boatupdatedby', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.boat_name 
    
    class Meta:
        verbose_name_plural = "Boat Details"
class BoatManager(models.Manager):
    def get_queryset(self, request):
        query = Boat_Details.objects.filter(owner_details=request.user)
        if request.user.is_superuser:
            query = User.objects.all()
        return query

status=(
(0, "Rejected"),
(1, "Approved"),
(2, "Pending"),
)
class Token_Book(models.Model):
    fishing_lisence_number = models.CharField(max_length=255,verbose_name='license No.')
    location_of_operation = models.CharField(max_length=255)
    token_number = models.CharField(max_length=255,unique=True,null=True)
    date_depature = models.DateField(null=True,blank=True)
    tentative_date = models.DateField(null=True,blank=True)
    quantity_fuel = models.DecimalField(max_digits=6,decimal_places=2)
    quantity_water = models.DecimalField(max_digits=6, decimal_places=2)
    owner = models.ForeignKey(Boat_Details,related_name='Owner1', on_delete=models.CASCADE) 
    number_of_crew = models.IntegerField()
    approved = models.PositiveIntegerField(default=2,choices=status,verbose_name='Status')
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    created_by = models.ForeignKey(User, related_name='tokencreated_by', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(User, related_name='tokenupdated_by', on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.fishing_lisence_number 
    
    class Meta:
        verbose_name_plural = "Token Book"

class BlogManager(models.Manager):
    def get_queryset(self, request):
        query = Token_Book.objects.filter(created_by=request.user)
        if request.user.is_superuser:
            query = User.objects.all()
        return query

# class Admin_Token_Book(models.Model):
#     token_book = models.OneToOneField(Token_Book, on_delete=models.CASCADE)

class Crew(models.Model):
    phone_message = 'Phone number must start with either 9, 8, 7 or 6 and should enter in this format: 9999955555'
    phone_regex = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message=phone_message
    )
    ten_digit = '''-> Phone number should be of 10 digits <br/> 
    -> Phone number must starts with either 9, 8, 7 or 6 <br/>
    -> Should enter in this format: 9999955555
    '''
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    aadhar_number = models.CharField(max_length=16, unique=True)
    phone_number =  models.CharField(max_length=12,null=False,unique=True, validators=[phone_regex],help_text=ten_digit)
    alternate_number = models.CharField(max_length=12,null=False, unique=True, validators=[phone_regex],help_text=ten_digit)
    boat = models.ForeignKey(Boat_Details, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    address = models.TextField()
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    created_by = models.ForeignKey(User,related_name='crewcreated_by', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(User, related_name='crewupdated_by' ,on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Crew"