# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # <--- ตรวจสอบว่ามี import นี้
from django.conf import settings
from django.conf.urls.static import static
# (ส่วน router ของ DRF ถ้าคุณมี ก็ปล่อยไว้เหมือนเดิม)

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Authentication URLs ---
    # Login
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'), # <--- เพิ่ม/แก้ไขบรรทัดนี้
    # template_name='myapp/login.html' คือให้ Django ใช้ template ที่คุณสร้างไว้สำหรับหน้า login
    # ถ้าคุณยังไม่มี template นี้ หรือใช้ชื่ออื่น ให้เปลี่ยนตามความเหมาะสม

    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # (URL สำหรับ DRF API ถ้ามี)
    # ...

    # URL สำหรับ myapp (หน้าเว็บหลัก)
    path('', include('myapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)