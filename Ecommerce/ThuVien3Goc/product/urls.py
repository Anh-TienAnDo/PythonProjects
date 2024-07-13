from django.urls import path, include

urlpatterns = [
    path('loudspeakers/', include('product.paths.loudspeaker')),
    path('memorysticks/', include('product.paths.memory_stick')),
    path('usbs/', include('product.paths.usb')),
]