# myproject/urls.py (ไฟล์หลักของโปรเจกต์)

from django.contrib import admin
from django.urls import path, include # include จำเป็นสำหรับการเรียก myapp.urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')), # <--- Include URL patterns จาก myapp.urls
    # ถ้าคุณต้องการให้ URL ของ myapp มี prefix เช่น 'app/' ก็จะเป็น path('app/', include('myapp.urls'))
]

# เพิ่มส่วนนี้เพื่อให้ Serve media files และ static files (ถ้าจำเป็น) ตอน DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # ปกติ Django dev server จะ serve static files จาก STATICFILES_DIRS และ app's static/ ให้อัตโนมัติ
    # แต่ถ้าต้องการความแน่นอน หรือมี STATIC_ROOT ที่ใช้ตอน collectstatic ก็อาจจะเพิ่ม:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)