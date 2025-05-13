ไฟล์นี้มีการกำหนดค่าแอปพลิเคชันสำหรับแอป Django ชื่อ myapp

- MyappConfig: คลาสย่อยของ AppConfig
    - ตั้งค่า default_auto_field เป็น django.db.models.BigAutoField ซึ่งระบุประเภทของ primary key ที่สร้างขึ้นอัตโนมัติ
    - ตั้งค่า name เป็น 'myapp' ซึ่งเป็น Python dotted path ไปยังแอปพลิเคชัน Django ใช้ชื่อนี้เพื่อค้นหาและโหลดแอปพลิเคชัน