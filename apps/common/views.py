from django.shortcuts import render
from .serializers import *
from rest_framework.generics import *
from rest_framework.views import *
from . import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class SponsorCreateAPIView(CreateAPIView):
    queryset = models.Sponsor.objects.all()
    serializer_class = SponsorCreateSerializer



class StudentSponsorCreateAPIView(CreateAPIView):
    queryset = models.AllocatedAmount.objects.all()
    serializer_class = StudentSponsorCreateSerializer





class StudentSponsorListAPIView(ListAPIView):
    serializer_class = AllocatedAmountSerializer

    def get_queryset(self):
        # Birinchi, so'rov tizimidan studentni identifikatorini olish
        student_id = self.kwargs.get('student_id')
        # Keyin, berilgan student uchun sponsorlar ro'yxatini topish
        return AllocatedAmount.objects.filter(student_id=student_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class StudentListAPIView(ListAPIView):
    queryset = models.Students.objects.all()
    serializer_class = StudentListSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['university','type']
    search_fields = ['full_name',]

class SponsorListAPIView(ListAPIView):
    queryset = models.Sponsor.objects.all()
    serializer_class = SponsorListSerializer
    filter_backends = [DjangoFilterBackend],SearchFilter
    filterset_fields = []
    search_fields = ['full_name',]


class TotalAmountStatisticsAPIView(APIView):
     def get(self,request):
         total_required_amount = Students.objects.aggregate(total=Sum('contract'))['total'] or 0
         total_paid_amount = AllocatedAmount.objects.aggregate(total=Sum('amount'))['total'] or 0
         return Response({
             'total_required_amount':total_required_amount,
             'total_paid_amount':total_paid_amount,
             'total_remain_amount':total_required_amount - total_paid_amount

         })
         

class MonthlyStatisticsAPIView(APIView):


    def get(self,request):
        from datetime import date
        this_year = date.today().year

        students = Students.objects.all()
        sponsors = Sponsor.objects.all()

        result = []
        for i in range(1,13):
            result.append({
                'year':this_year,
                'students':students.filter(created_at__month=i , created_at__year=this_year).count(),
                'sponsors':sponsors.filter(created_at__month=i , created_at__year=this_year).count(),
            })
        return Response(result)

    def get_month(self,month_in_number):
        l={
            1:'Yanvar',
            2:'Fevral',
            3:'Mart',
            4:'Aprel',
            5:'May',
            6:'Iyun',
            7:'iyul',
            8:'Avgust',
            9:'Sentabr',
            10:'Octabar',
            11:'Noyabr',
            12:'Dekabr'
        }

        return l[month_in_number]
         

class StudentSponsorUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.AllocatedAmount.objects.all()
    serializer_class = StudentSponsorUpdateSerializer



class StudentUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Students.objects.all()
    serializer_class =  StudentUpdateSerializer
    

class SponsorUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class =  SponsorUpdateSerializer
