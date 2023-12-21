from django.contrib import admin
from film.views import *
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aktyorlar/', AktyorlarApi.as_view()),
    path('aktyor/<int:pk>', AktyorApi.as_view()),
    path('tariflar/', TariflarApi.as_view()),
    path('tarif/<int:pk>', TarifApi.as_view()),
    path('kinolar/', KinolarApi.as_view()),
    path('kino/<int:pk>', KinoApi.as_view()),
    path('izoh/', IzohApi.as_view()),
    path('izoh/<int:pk>', IzohDestroyRetireveUpdate.as_view())
]
