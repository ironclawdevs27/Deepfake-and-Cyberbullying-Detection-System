from django.urls import path, include
from . import views
from .views import about, home, index, cyberbullying_index, cyberbullying_detect, predict_page, cuda_full

app_name = 'ml_app'
handler404 = views.handler404

urlpatterns = [
    path('home/', home, name='home'),
    path('', index, name='index'),
    path('cyberbullying/', cyberbullying_index, name='cyberbullying_index'),
    path('detect/', cyberbullying_detect,
         name='cyberbullying_detect'),
    path('about/', about, name='about'),
    path('predict/', predict_page, name='predict'),
    path('cuda_full/', cuda_full, name='cuda_full'),
]
