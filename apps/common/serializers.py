from rest_framework import serializers
from .models import *
from django.db.models import Sum


class SponsorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponsor
        exclude = ('status','payment_type',)

    def validate(self, attrs):
        company_name = attrs.get('company_name')
        user_type = attrs.get('user_type')
        if user_type == '':############ tekshirish qilish kk 
            raise serializers.ValidationError({'company_name': 'This field is required.'})

        return super().validate(attrs)
    


class StudentSponsorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllocatedAmount
        fields = '__all__'


    def validate(self, attrs):
        print(attrs)
        sponsor = attrs['sponsor']
        student = attrs['student']
        amount = attrs['amount']
        result = sponsor.sponsor_amounts.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        sponsor_current_amount = sponsor.wallet - result
        student_current_amount = student.student_amounts.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        # print(student_current_amount)
        if amount > sponsor_current_amount:
            raise serializers.ValidationError({'msg': f"sponsor's current balance amount {sponsor_current_amount}.This amount is greater than your current balance."})
        if student.contract - student_current_amount < amount:
            raise serializers.ValidationError({'msg': f"student's current balance amount {student.contract-student_current_amount}.This amount is greater than your current balance."})
        return super().validate(attrs)
    
class AllocatedAmountSerializer(serializers.ModelSerializer):
    sponsor = serializers.StringRelatedField()
    class Meta:
        model = AllocatedAmount
        fields = ['sponsor', 'id', 'amount']

class StudentListSerializer(serializers.ModelSerializer):
    student_current_amount = serializers.IntegerField(source = 'allocated_amount')
    university = serializers.CharField(source = 'university.name')
    class Meta:
        model = Students
        fields = ['id', 'full_name', 'contract', 'phone','student_current_amount', 'type', 'university']

class SponsorListSerializer(serializers.ModelSerializer):
    sponsor_current_amount = serializers.IntegerField(source = 'allocated_amount')

    class Meta:
        model = Sponsor
        fields = ['id','full_name', 'company', 'status','sponsor_current_amount']
   




  
        


