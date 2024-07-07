"""llm_post_processing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from RacialBias.views import ResultsView
from Hate_profanity.views import CommentViewSet
from PII.views import anonymizeView
from blacklisted.views import BlackListView
from django.conf import settings
from main.views import MainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('racialBias/', ResultsView.as_view(), name='result'),
    path('hateprofanity/', CommentViewSet.as_view(), name='tox'),
    path('anonymize_text/', anonymizeView.as_view(), name='anonymize_text'),
    path('blacklisted/', BlackListView.as_view(), name='blacklisted'),
    path('violenceDetection/', include('violenceDetection.urls')),
    path('postprocessing/', MainView.as_view(), name='postprocessing')
]
