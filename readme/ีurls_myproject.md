ไฟล์นี้ (myproject/urls.py) กำหนดการตั้งค่า URL หลักสำหรับโปรเจกต์ Django

- ส่วนติดต่อผู้ดูแลระบบ (Admin Interface):
    - admin/: รวม URL สำหรับไซต์การดูแลระบบของ Django
- URL การยืนยันตัวตน (Authentication URLs):
    - login/: แมปไปยัง LoginView ที่มีใน Django โดยใช้เทมเพลตที่กำหนดเอง myapp/login.html
    - logout/: แมปไปยัง LogoutView ที่มีใน Django โดยจะเปลี่ยนเส้นทางไปยังหน้า home หลังจากออกจากระบบ
- URL ของแอปพลิเคชัน (Application URLs):
    - พาธว่าง '' จะรวมรูปแบบ URL ทั้งหมดที่กำหนดใน myapp.urls (ไฟล์ urls.py ระดับแอปที่อธิบายไว้ก่อนหน้านี้)
- ไฟล์สถิตและไฟล์มีเดีย (Static and Media Files):
    ในโหมด DEBUG จะกำหนดค่ารูปแบบ URL เพื่อให้บริการไฟล์มีเดีย (จาก MEDIA_ROOT) และไฟล์สถิต (จาก STATIC_ROOT) โดยทั่วไปจะใช้เพื่อวัตถุประสงค์ในการพัฒนา