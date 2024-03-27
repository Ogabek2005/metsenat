from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from apps.common.views import *

from .schema import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/',include('apps.users.urls')),
    path('sponsor-create/' , SponsorCreateAPIView.as_view()),
    path('sponsor-add/', StudentSponsorCreateAPIView.as_view()),
    path('student/sponsors/<int:student_id>', StudentSponsorListAPIView.as_view()),
    path('student-list/', StudentListAPIView.as_view()),
    path('sponsor-list/', SponsorListAPIView.as_view()),
    path('total-amount-statistics', TotalAmountStatisticsAPIView.as_view()),
    path('monthly-statistics', MonthlyStatisticsAPIView.as_view()),
    path('student-sponsor-update/<int:pk>', StudentSponsorUpdateAPIView.as_view()),
    path('student-updated/<int:pk>', StudentUpdateAPIView.as_view()),
    path('sponsor-updated/<int:pk>', SponsorUpdateAPIView.as_view()),
    

]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
