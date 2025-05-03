from django.contrib import admin
from .models import Category, Event, Attendance, UserProfile ,Community

# Register โมเดล Community เข้ากับ Django admin interface
@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    # กำหนดฟิลด์ที่จะแสดงในหน้า List View ของออบเจ็กต์ Community
    list_display = ('name',)
    # กำหนดฟิลด์ที่สามารถใช้ค้นหาออบเจ็กต์ Community ในหน้า admin interface
    search_fields = ('name',)

# Register โมเดล Category เข้ากับ Django admin interface
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # กำหนดฟิลด์ที่จะแสดงในหน้า List View ของออบเจ็กต์ Category
    list_display = ('name',)
    # กำหนดฟิลด์ที่สามารถใช้ค้นหาออบเจ็กต์ Category ในหน้า admin interface
    search_fields = ('name',)

# Register โมเดล Event เข้ากับ Django admin interface
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # กำหนดฟิลด์ที่จะแสดงในหน้า List View ของออบเจ็กต์ Event
    list_display = ('title', 'date', 'time', 'location', 'category', 'community', 'organizer', 'attendee_count')
    # กำหนดฟิลด์ที่สามารถใช้ Filter ออบเจ็กต์ Event ในหน้า admin interface
    list_filter = ('date', 'category', 'community')
    # กำหนดฟิลด์ที่สามารถใช้ค้นหาออบเจ็กต์ Event ในหน้า admin interface
    search_fields = ('title', 'description', 'location')
    # เปิดใช้งานการนำทางตามลำดับวันที่สำหรับออบเจ็กต์ Event
    date_hierarchy = 'date'

# Register โมเดล Attendance เข้ากับ Django admin interface
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # กำหนดฟิลด์ที่จะแสดงในหน้า List View ของออบเจ็กต์ Attendance
    list_display = ('user', 'event', 'status', 'created_at')
    # กำหนดฟิลด์ที่สามารถใช้ Filter ออบเจ็กต์ Attendance ในหน้า admin interface
    list_filter = ('status', 'created_at')
    # กำหนดฟิลด์ที่สามารถใช้ค้นหาออบเจ็กต์ Attendance ในหน้า admin interface
    search_fields = ('user__username', 'event__title')

# Register โมเดล UserProfile เข้ากับ Django admin interface
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # กำหนดฟิลด์ที่จะแสดงในหน้า List View ของออบเจ็กต์ UserProfile
    list_display = ('user', 'bio')
    # กำหนดฟิลด์ที่สามารถใช้ค้นหาออบเจ็กต์ UserProfile ในหน้า admin interface
    search_fields = ('user__username', 'bio')