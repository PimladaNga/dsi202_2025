ไฟล์นี้ (myapp/urls.py) กำหนดรูปแบบ URL สำหรับแอปพลิเคชัน myapp โดยจับคู่ URL กับ view ต่างๆ

- หน้าหลัก:
    - /: แมปกับ views.home (ชื่อ: home)
- กิจกรรม (Events):
    - /events/: แมปกับ views.EventListView (ชื่อ: event_list)
    - /events/create/: แมปกับ views.EventCreateView (ชื่อ: event_create)
    - /events/<int:pk>/: แมปกับ views.EventDetailView (ชื่อ: event_detail)
    - /events/<int:pk>/update/: แมปกับ views.EventUpdateView (ชื่อ: event_update)
    - /events/<int:pk>/attend/: แมปกับ views.attend_event (ชื่อ: attend_event)
- โปรไฟล์ผู้ใช้ (User Profiles):
    - /profile/edit/: แมปกับ views.edit_profile (ชื่อ: edit_profile) (URL นี้อยู่ก่อน URL ที่รับ username เพื่อให้จับคู่ได้ถูกต้อง)
    - /profile/<str:username>/: แมปกับ views.user_profile (ชื่อ: view_profile) สำหรับดูโปรไฟล์ของผู้ใช้อื่น
    - /profile/: แมปกับ views.user_profile (ชื่อ: user_profile) สำหรับโปรไฟล์ของผู้ใช้ที่ล็อกอินอยู่
- การยืนยันตัวตน (Authentication):
    - /signup/: แมปกับ views.signup (ชื่อ: signup)
    - (การเข้าสู่ระบบ/ออกจากระบบ ถูกจัดการใน myproject/urls.py ระดับโปรเจกต์)
- ควิซ (Quiz):
    - /quiz/: แมปกับ views.butterfly_quiz_view (ชื่อ: butterfly_quiz)
    - /quiz/result/<slug:slug>/: แมปกับ views.butterfly_result_view (ชื่อ: butterfly_result_page_slug)
- แดชบอร์ด (Dashboard) (ถูกคอมเมนต์ไว้หรือรอการพัฒนา):
    # path('dashboard/', views.dashboard_page, name='dashboard')