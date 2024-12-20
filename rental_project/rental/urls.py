from django.urls import path
from . import views

from .views import PartDetailAPIView, PartListCreateAPIView, AircraftAPIView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("create-parts", views.create_parts, name="create-part"),
    path("create-aircraft", views.assemble_aircraft, name="assemble-aircraft"),
    path("list-aircraft", views.list_aircrafts, name="list-aircraft"),
    path("logout", views.logout_view, name="logout"),
    path('api/parts/', PartListCreateAPIView.as_view(), name='part_list_create'),
    path('api/parts/<int:pk>/', PartDetailAPIView.as_view(), name='part_detail'),
    path("api/assemble-aircraft/", AircraftAPIView.as_view(), name="assemble_aircraft"),
]
