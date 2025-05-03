# นำเข้าคลาส AppConfig จาก django.apps ซึ่งเป็นคลาสพื้นฐานสำหรับการตั้งค่าแอปพลิเคชัน
from django.apps import AppConfig
# กำหนดคลาสการตั้งค่าสำหรับแอปพลิเคชัน 'myapp' โดยสืบทอด (inherit) มาจาก AppConfig
# Django จะใช้คลาสนี้เพื่อจัดการกับแอปพลิเคชันนี้โดยเฉพาะ
class MyappConfig(AppConfig):
    # ตั้งค่าชนิดข้อมูลเริ่มต้นสำหรับ primary key ที่สร้างอัตโนมัติ (auto-generated primary key)
    # ในโมเดล (models) ของแอปนี้ให้เป็น BigAutoField (เลขจำนวนเต็ม 64 บิต)
    default_auto_field = 'django.db.models.BigAutoField'

    # ระบุชื่อของแอปพลิเคชันนี้ (Python dotted path)
    # Django ใช้ชื่อนี้ในการค้นหาและโหลดแอปพลิเคชัน
    name = 'myapp'
