from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("create-parts", views.create_parts, name="create-part"),
    path("list-parts", views.list_parts, name="list-part"), # öncelikli değil
    path("create-aircraft", views.create_aircrafts, name="create-aircraft"),
    path("list-aircraft", views.list_aircrafts, name="list-aircraft"),
    path("logout", views.logout_view, name="logout")
]
