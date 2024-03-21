from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from django.db.models import Sum


JISMONIY , YURIDIK = 'jismoniy','yuridik'
NEW , ACTIVE , CANSELED , MODERATION = 'new','active','canseled','moderation'
BACHELOUR , MAGISTR = 'bachelour','magistr'
BY_CARD , CASH = 'Karta_orqali' , 'Naqd_pul'

phone_validator = RegexValidator(regex=r"^\+998\d{9}$", message='phone number is wrong',
                                 code="invalid_phone")



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Sponsor(BaseModel):
    TYPE_CHOICES =(
        (JISMONIY,'jismoniy shaxs'),
         (YURIDIK, 'yuridik shaxs',)
    )

    STATUS_CHOICES = (
        (NEW, 'new'),
        (ACTIVE, 'active'),
        (CANSELED, 'canseled'),
        (MODERATION,'moderation'),
    )

    PAYMENT_CHOICES = (
        (BY_CARD,'card'),
         (CASH , 'Naqd pul'),
    )

    full_name = models.CharField(max_length=250)
    wallet = models.DecimalField(max_digits=12, decimal_places=2)
    phone = models.CharField(max_length=13,validators =[phone_validator])
    type = models.CharField(max_length=250,
                            choices=TYPE_CHOICES,
                            default=JISMONIY,
                            verbose_name = "Type")
    status = models.CharField(max_length=250,
                             choices=STATUS_CHOICES,
                             default=NEW,
                             verbose_name = "Status")
    company = models.CharField(max_length=250,blank=True, null=True)
    payment_type = models.CharField(max_length=250,
                                    choices = PAYMENT_CHOICES,
                                    default = CASH
                                    )
    @property
    def allocated_amount(self):
        return self.sponsor_amounts.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    
    

    def __str__(self):
        return self.full_name
    
class Students(BaseModel):

    TYPE_CHOICES =(
        (BACHELOUR, 'bachelor'),
        (MAGISTR,'magistr'),
    )

    full_name = models.CharField(max_length=250, verbose_name="Full Name")
    contract = models.DecimalField(max_digits=12 , decimal_places=2, verbose_name="Contract")
    phone = models.CharField(max_length=25,
                            validators =[phone_validator],
                            default = BACHELOUR,
                            verbose_name="Phone")
    type = models.CharField(max_length=250,
                            choices=TYPE_CHOICES,
                            default=BACHELOUR,
                            verbose_name = "Type")
    university = models.ForeignKey('University',on_delete=models.CASCADE,verbose_name='University')
    @property
    def allocated_amount(self):
        return self.student_amounts.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    

    def __str__(self):
        return self.full_name
    

class University(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name
    

class AllocatedAmount(BaseModel):

    sponsor = models.ForeignKey(
                                Sponsor,
                                on_delete=models.PROTECT,
                                verbose_name="Sponsor",
                                related_name="sponsor_amounts"
                                )
    student = models.ForeignKey(
                                Students,
                                on_delete=models.PROTECT,
                                verbose_name="Student",
                                related_name="student_amounts"
                                )
    amount = models.DecimalField(max_digits=12,
                                 decimal_places=2,
                                #  verbose_name="Amount"
                                 )


    def __str__(self):
        return f"{self.sponsor}-{self.student}"




