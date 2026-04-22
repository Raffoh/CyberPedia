from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_feed, name='home'),
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Attacchi
    path('attacchi/', views.attacchi_list, name='attacchi-list'),
    path('attacchi/nuovo/', views.attacco_create, name='attacco-create'),
    path('attacchi/<int:pk>/', views.attacco_detail, name='attacco-detail'),
    path('attacchi/<int:pk>/modifica/', views.attacco_edit, name='attacco-edit'),
    path('attacchi/<int:pk>/elimina/', views.attacco_delete, name='attacco-delete'),
    # Vulnerabilita
    path('vulnerabilita/', views.vulnerabilita_list, name='vulnerabilita-list'),
    path('vulnerabilita/nuova/', views.vulnerabilita_create, name='vulnerabilita-create'),
    path('vulnerabilita/<int:pk>/', views.vulnerabilita_detail, name='vulnerabilita-detail'),
    path('vulnerabilita/<int:pk>/modifica/', views.vulnerabilita_edit, name='vulnerabilita-edit'),
    # Contromisure
    path('contromisure/', views.contromisure_list, name='contromisure-list'),
    path('contromisure/nuova/', views.contromisura_create, name='contromisura-create'),
    path('contromisure/<int:pk>/', views.contromisura_detail, name='contromisura-detail'),
    path('contromisure/<int:pk>/modifica/', views.contromisura_edit, name='contromisura-edit'),
    # Casi Reali
    path('casi/', views.casi_list, name='casi-list'),
    path('casi/nuovo/', views.caso_create, name='caso-create'),
    path('casi/<int:pk>/', views.caso_detail, name='caso-detail'),
    path('casi/<int:pk>/modifica/', views.caso_edit, name='caso-edit'),
    # Articoli
    path('articoli/', views.articoli_list, name='articoli-list'),
    path('articoli/nuovo/', views.articolo_create, name='articolo-create'),
    path('articoli/<int:pk>/', views.articolo_detail, name='articolo-detail'),
    path('articoli/<int:pk>/modifica/', views.articolo_edit, name='articolo-edit'),
    path('articoli/<int:pk>/elimina/', views.articolo_delete, name='articolo-delete'),
    # Utenti
    path('profilo/<int:user_id>/', views.profilo_view, name='profilo'),
    path('profilo/modifica/', views.profilo_edit, name='profilo-edit'),
    # Social
    path('follow/<int:user_id>/', views.follow_toggle, name='follow-toggle'),
    path('interazione/attacco/<int:pk>/', views.interazione_attacco, name='interazione-attacco'),
    path('interazione/articolo/<int:pk>/', views.interazione_articolo, name='interazione-articolo'),
    path('interazione/caso/<int:pk>/', views.interazione_caso, name='interazione-caso'),
    # Statistiche
    path('statistiche/', views.statistiche_view, name='statistiche'),
]
