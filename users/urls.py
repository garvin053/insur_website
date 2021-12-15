from django.urls import include, path
from .views import UserViewset, PassengerViewset, AnalyseViewSet
from rest_framework import routers
from django.conf.urls import url, include

router = routers.DefaultRouter()

router.register(r'user', UserViewset)

router.register(r'passenger', PassengerViewset)

router.register(r'invoice', AnalyseViewSet)

# urlpatterns = [
#     # path('', UserListView.as_view()),
#     path('auth/login', include(UserViewset.login)),
#     path('auth/register/', include(UserViewset.register()))
# ]
urlpatterns = [
        url(r'^', include(router.urls)),
    ]