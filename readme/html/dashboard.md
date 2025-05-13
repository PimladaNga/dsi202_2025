ไฟล์ HTML นี้เป็นหน้าแดชบอร์ดแบบง่าย มีแนวโน้มว่าจะใช้สำหรับมุมมองการดูแลระบบหรือสรุปข้อมูล ไม่ได้สืบทอดจาก base.html และดูเหมือนจะเป็นหน้าเดี่ยวหรือใช้ base อื่น

- หัวเรื่อง (Title): "Dashboard"
- การจัดรูปแบบ (Styling): ใช้ Tailwind CSS (ผ่าน CDN)
- เนื้อหา (Content):
    - หัวข้อหลัก "Dashboard Summary"
    - เลย์เอาต์แบบตารางแสดงสถิติสรุปสี่รายการในการ์ดที่จัดรูปแบบ:
        - "Users": แสดง {{ user_count }}
        - "Events": แสดง {{ event_count }}
        - "Communities": แสดง {{ community_count }}
        - "Attendances": แสดง {{ attendance_count }}