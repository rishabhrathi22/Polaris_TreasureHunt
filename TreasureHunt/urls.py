from django.contrib import admin
from django.urls import include, path

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('marvelrocks/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('quiz.urls'))
]