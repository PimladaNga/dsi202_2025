# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _ # สำหรับ verbose_name ที่เป็นภาษาไทย

# --- Model เดิมของคุณ ---
class Community(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("ชื่อชุมชน"))
    image = models.ImageField(upload_to='communities/', blank=True, null=True, verbose_name=_("รูปภาพชุมชน"))
    description = models.TextField(blank=True, null=True, verbose_name=_("รายละเอียด"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("ชุมชน")
        verbose_name_plural = _("05. ชุมชน") # ปรับลำดับการแสดงใน Admin
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("ชื่อหมวดหมู่"))
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name=_("รูปภาพหมวดหมู่"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("หมวดหมู่กิจกรรม")
        verbose_name_plural = _("06. หมวดหมู่กิจกรรม") # ปรับลำดับ
        ordering = ['name']

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("ชื่อกิจกรรม"))
    description = models.TextField(verbose_name=_("รายละเอียดกิจกรรม"))
    location = models.CharField(max_length=200, verbose_name=_("สถานที่จัดกิจกรรม"))
    date = models.DateField(verbose_name=_("วันที่จัดกิจกรรม"))
    time = models.TimeField(verbose_name=_("เวลาเริ่มกิจกรรม"))
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name=_("รูปภาพกิจกรรม"))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events_in_category',
        verbose_name=_("หมวดหมู่")
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events_in_community',
        verbose_name=_("จัดโดยชุมชน (ถ้ามี)")
    )
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_events',
        verbose_name=_("ผู้จัดกิจกรรม")
    )
    max_attendees = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("จำนวนผู้เข้าร่วมสูงสุด (ถ้ามี)"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("วันที่สร้าง"))

    def __str__(self):
        return self.title

    @property
    def attendee_count(self):
        return self.attendees.filter(status='attending').count()
    attendee_count.fget.short_description = _("จำนวนผู้เข้าร่วม")


    class Meta:
        verbose_name = _("กิจกรรม")
        verbose_name_plural = _("07. กิจกรรม") # ปรับลำดับ
        ordering = ['-date', '-time']


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('attending', _('เข้าร่วม')),
        ('interested', _('สนใจ')),
        ('not_attending', _('ไม่เข้าร่วม'))
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees', verbose_name=_("กิจกรรม"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_attendances', verbose_name=_("ผู้ใช้"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='attending', verbose_name=_("สถานะ"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("วันที่บันทึกสถานะ"))

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = _("การเข้าร่วมกิจกรรม")
        verbose_name_plural = _("08. การเข้าร่วมกิจกรรม") # ปรับลำดับ
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.event.title} - {self.get_status_display()}'

# --- Model ใหม่/ปรับปรุงสำหรับโปรไฟล์ผีเสื้อ ---
class ButterflyType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("ชื่อประเภทผีเสื้อ"))
    name_en = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name=_("ชื่อประเภท (ภาษาอังกฤษสำหรับ Slug)"))
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text=_("สร้างอัตโนมัติจากชื่อภาษาอังกฤษ ถ้าเว้นว่าง"))
    description = models.TextField(verbose_name=_("คำอธิบายสั้นๆ (แสดงใน Quiz Result)"))
    long_description = models.TextField(blank=True, null=True, verbose_name=_("คำอธิบายแบบยาว (แสดงใน Quiz Result)"))
    strengths = models.TextField(blank=True, null=True, verbose_name=_("จุดแข็ง (แสดงใน Quiz Result)"))
    # weaknesses = models.TextField(blank=True, null=True, verbose_name=_("จุดที่ควรพัฒนา (ถ้ามี)")) # Optional

    icon_image = models.ImageField(upload_to='butterfly_type_icons/', blank=True, null=True, verbose_name=_("รูปไอคอน (แสดงทั่วไป)"))
    result_image = models.ImageField(upload_to='butterfly_results/', blank=True, null=True, verbose_name=_("รูปภาพผลลัพธ์หลัก (แสดงใน Quiz Result)"))

    theme_colors_description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("สี/ธีมที่สื่อถึง (คำอธิบาย)"))
    # สำหรับ Dynamic Theme ใน template (Optional)
    # theme_color_start = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Tailwind BG Gradient From (เช่น purple-50)"))
    # theme_color_end = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Tailwind BG Gradient To (เช่น pink-50)"))
    # text_color = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Tailwind Text Color (เช่น purple-700)"))


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            source_for_slug = self.name_en if self.name_en else self.name
            self.slug = slugify(source_for_slug)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("ประเภทผีเสื้อ")
        verbose_name_plural = _("01. ประเภทผีเสื้อ (Quiz)")
        ordering = ['name']


class Question(models.Model):
    text = models.TextField(verbose_name=_("ข้อความคำถาม"))
    order = models.PositiveIntegerField(default=0, help_text=_("ลำดับการแสดงผลของคำถาม (เลขน้อยแสดงก่อน)"), verbose_name=_("ลำดับ"))
    # image = models.ImageField(upload_to='quiz_question_images/', blank=True, null=True, verbose_name=_("รูปภาพประกอบคำถาม")) # Optional

    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}..."

    class Meta:
        ordering = ['order']
        verbose_name = _("คำถาม Quiz")
        verbose_name_plural = _("02. คำถาม Quiz")


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE, verbose_name=_("ของคำถาม"))
    text = models.CharField(max_length=255, verbose_name=_("ข้อความตัวเลือก"))
    points_to_type = models.ForeignKey(
        ButterflyType,
        on_delete=models.SET_NULL, # หรือ models.PROTECT ถ้าไม่ต้องการให้ลบ Type ที่มี Choice ผูกอยู่
        null=True,
        blank=False, # บังคับให้ต้องเลือกตอนสร้างผ่าน Admin
        related_name="defining_choices",
        verbose_name=_("ให้คะแนนแก่ประเภทผีเสื้อ")
    )
    # image = models.ImageField(upload_to='quiz_choice_images/', blank=True, null=True, verbose_name=_("รูปภาพประกอบตัวเลือก")) # Optional

    def __str__(self):
        type_name = self.points_to_type.name if self.points_to_type else "N/A"
        return f"{self.text} (-> {type_name})"

    class Meta:
        verbose_name = _("ตัวเลือกคำตอบ Quiz")
        verbose_name_plural = _("03. ตัวเลือกคำตอบ Quiz")


# UserProfile Model (ปรับปรุง)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_("ผู้ใช้"))
    bio = models.TextField(blank=True, null=True, verbose_name=_("เกี่ยวกับฉัน"))
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default_avatar.png', blank=True, null=True, verbose_name=_("รูปโปรไฟล์"))

    assigned_butterfly_type = models.ForeignKey(
        ButterflyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users_of_this_type',
        verbose_name=_("ประเภทผีเสื้อที่ได้รับ")
    )
    quiz_completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("วันที่ทำ Quiz เสร็จสิ้น"))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("โปรไฟล์ผู้ใช้")
        verbose_name_plural = _("04. โปรไฟล์ผู้ใช้")


# Signal เพื่อสร้าง UserProfile อัตโนมัติเมื่อ User ถูกสร้างหรืออัปเดต
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # ในกรณีที่ User ถูกอัปเดต อาจจะไม่จำเป็นต้อง save() profile ทุกครั้ง
        # เว้นแต่จะมีการเปลี่ยนแปลงข้อมูลใน User ที่ส่งผลต่อ Profile
        # แต่เพื่อความปลอดภัย (เผื่อ Profile อาจถูกลบไป) การใช้ get_or_create ก็เป็นทางเลือกที่ดี
        profile, profile_created = UserProfile.objects.get_or_create(user=instance)
        if not profile_created:
            # ถ้า profile มีอยู่แล้ว อาจจะไม่ต้องทำอะไร หรืออาจจะ save ถ้ามีการอัปเดตบางอย่างที่เชื่อมโยง
            pass # instance.profile.save() # อาจจะไม่จำเป็นเสมอไป