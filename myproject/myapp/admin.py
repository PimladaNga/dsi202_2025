from django.contrib import admin
from .models import Category, Event, Attendance, UserProfile ,Community,ButterflyType, Question, Choice, UserProfile
from django.utils.translation import gettext_lazy as _

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

# --- UserProfileAdmin (รวมเป็นอันเดียว) ---
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username_display', 'assigned_butterfly_type','is_pro_member', 'pro_membership_end_date', 'quiz_completed_at', 'bio_short')
    list_filter = ('assigned_butterfly_type', 'is_pro_member')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'bio')
    # readonly_fields ทำให้แก้ไขไม่ได้โดยตรงจากหน้าแก้ไข UserProfile ปกติ เหมาะกับ field ที่มาจาก User model หรือถูกจัดการโดยระบบ
    readonly_fields = ('quiz_completed_at',)
    # autocomplete_fields ช่วยให้การเลือก ForeignKey เช่น assigned_butterfly_type ทำได้ง่ายขึ้น
    autocomplete_fields = ['user', 'assigned_butterfly_type']
    fieldsets = (
        (None, {
            'fields': ('user', 'profile_image', 'bio')
        }),
        (_('Butterfly Quiz Information'), { # ใช้ gettext_lazy สำหรับ section title
            'fields': ('assigned_butterfly_type', 'quiz_completed_at'),
            'classes': ('collapse',), # ทำให้ section นี้ย่อได้
        }),
        (_('Pro Membership Information'), {
            'fields': ('is_pro_member', 'pro_membership_start_date', 'pro_membership_end_date'),
            'classes': ('collapse',), # ทำให้ section นี้ย่อได้
        }),
    )

    @admin.display(description=_('Username'))
    def get_username_display(self, obj):
        return obj.user.username
    get_username_display.admin_order_field = 'user__username' # ทำให้สามารถ sort ตาม username ได้

    @admin.display(description=_('Bio (Short)'))
    def bio_short(self, obj):
        return (obj.bio[:75] + '...') if obj.bio and len(obj.bio) > 75 else obj.bio

# --- Quiz Related Admin ---
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1 # จำนวนช่องตัวเลือกเริ่มต้นที่จะแสดง (ปรับตามต้องการ)
    autocomplete_fields = ['points_to_type'] # ทำให้การเลือก ButterflyType สำหรับ Choice ง่ายขึ้น

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'order')
    list_editable = ('order',)
    inlines = [ChoiceInline]
    search_fields = ['text']
    ordering = ['order']

    @admin.display(description=_('Question Text (Short)'))
    def text_short(self, obj):
        return (obj.text[:100] + '...') if len(obj.text) > 100 else obj.text

@admin.register(ButterflyType)
class ButterflyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'slug', 'theme_colors_description_short')
    # หากคุณเพิ่ม name_en ใน model เพื่อใช้สร้าง slug:
    prepopulated_fields = {'slug': ('name_en',)}
    # หากยังใช้ name (ภาษาไทย) สร้าง slug (อาจจะไม่สวยงามเท่า):
    # prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'name_en', 'description', 'long_description']

    @admin.display(description=_('Theme Colors (Short)'))
    def theme_colors_description_short(self, obj):
        if obj.theme_colors_description:
            return (obj.theme_colors_description[:75] + '...') if len(obj.theme_colors_description) > 75 else obj.theme_colors_description
        return "-"