"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path
from consulta.views import listar_municipios, baixar_csv_filtrado, baixar_csv_completo, pagina_erro, download_page
from home.views import home_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home_view, name='home'),
    path('consulta/', listar_municipios, name='cities'),
    path('consulta/download/', download_page, name='download_page'),
    path('consulta/download/download-csv-1', baixar_csv_filtrado, name='download_csv_1'),
    path('consulta/download/download-csv-2', baixar_csv_completo, name='download_csv_2'),
    path('erro/', pagina_erro, name='error_page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
