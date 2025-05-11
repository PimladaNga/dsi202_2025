# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _ # สำหรับ verbose_name ที่เป็นภาษาไทย

class Community(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("ชื่อชุมชน"))
    image = models.ImageField(upload_to='communities/', blank=True, null=True, verbose_name=_("รูปภาพชุมชน"))
    description = models.TextField(blank=True, null=True, verbose_name=_("รายละเอียด"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("ชุมชน")
        verbose_name_plural = _("05. ชุมชน")
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("ชื่อหมวดหมู่"))
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name=_("รูปภาพหมวดหมู่"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("หมวดหมู่กิจกรรม")
        verbose_name_plural = _("06. หมวดหมู่กิจกรรม")
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
        on_delete=models.SET_NULL, # ถ้าลบ Category, Event จะยังมีอยู่แต่ไม่มี category
        null=True,
        blank=True, # อนุญาตให้ Event ไม่มี Category ได้
        related_name='events_in_category', # ชื่อสำหรับอ้างอิงจาก Category ไป Event
        verbose_name=_("หมวดหมู่")
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL, # ถ้าลบ Community, Event จะยังมีอยู่แต่ไม่มี community
        null=True,
        blank=True, # อนุญาตให้ Event ไม่มี Community ได้
        related_name='events_in_community', # ชื่อสำหรับอ้างอิงจาก Community ไป Event
        verbose_name=_("จัดโดยชุมชน (ถ้ามี)")
    )
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # ถ้าลบ User, Event ที่ User นี้จัดจะถูกลบไปด้วย
        related_name='organized_events', # ชื่อสำหรับอ้างอิงจาก User ไป Event ที่จัด
        verbose_name=_("ผู้จัดกิจกรรม")
    )
    max_attendees = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("จำนวนผู้เข้าร่วมสูงสุด (ถ้ามี)"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("วันที่สร้าง")) # วันที่สร้าง Event record

    def __str__(self):
        return self.title

    @property
    def attendee_count(self):
        # นับเฉพาะคนที่ 'attending' จริงๆ
        return self.attendees.filter(status='attending').count()
    # ทำให้แสดงใน Admin ได้สวยงาม
    attendee_count.fget.short_description = _("จำนวนผู้เข้าร่วม")


    class Meta:
        verbose_name = _("กิจกรรม")
        verbose_name_plural = _("07. กิจกรรม")
        ordering = ['-date', '-time'] # เรียงจากกิจกรรมล่าสุดไปเก่าสุด


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('attending', _('เข้าร่วม')),
        ('interested', _('สนใจ')),
        ('not_attending', _('ไม่เข้าร่วม')) # อาจจะเพิ่มสถานะนี้ถ้าต้องการให้ user ยกเลิกได้ชัดเจน
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees', verbose_name=_("กิจกรรม"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_attendances', verbose_name=_("ผู้ใช้"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='interested', verbose_name=_("สถานะ")) # อาจจะเริ่มที่ interested ก่อน
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("วันที่บันทึกสถานะ"))

    class Meta:
        unique_together = ('event', 'user') # ผู้ใช้คนหนึ่งสามารถมีสถานะต่อ Event หนึ่งได้เพียงสถานะเดียว
        verbose_name = _("การเข้าร่วมกิจกรรม")
        verbose_name_plural = _("08. การเข้าร่วมกิจกรรม")
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.event.title} - {self.get_status_display()}'


class ButterflyType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("ชื่อประเภทผีเสื้อ (ไทย)"))
    name_en = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name=_("ชื่อประเภท (อังกฤษสำหรับ Slug)"))
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text=_("สร้างอัตโนมัติจากชื่อภาษาอังกฤษ (ถ้ามี) หรือชื่อภาษาไทย"))
    description = models.TextField(verbose_name=_("คำอธิบายสั้นๆ (แสดงใน Quiz Result)"))
    long_description = models.TextField(blank=True, null=True, verbose_name=_("คำอธิบายแบบยาว (แสดงใน Quiz Result)"))
    strengths = models.TextField(blank=True, null=True, verbose_name=_("จุดแข็ง (แสดงใน Quiz Result)"))
    # weaknesses = models.TextField(blank=True, null=True, verbose_name=_("จุดที่ควรพัฒนา (ถ้ามี)"))

    icon_image = models.ImageField(upload_to='butterfly_type_icons/', blank=True, null=True, verbose_name=_("รูปไอคอน (แสดงทั่วไป)"))
    result_image = models.ImageField(upload_to='butterfly_results/', blank=True, null=True, verbose_name=_("รูปภาพผลลัพธ์หลัก (แสดงใน Quiz Result)"))

    theme_colors_description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("สี/ธีมที่สื่อถึง (คำอธิบาย)"))
    # สำหรับ Dynamic Theme ใน template (Optional, ถ้าจะใช้ต้อง uncomment และเพิ่มใน template ด้วย)
    theme_color_start = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Tailwind BG Gradient From (เช่น purple-50)"))
    theme_color_end = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Tailwind BG Gradient To (เช่น pink-50)"))
    text_color = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Tailwind Text Color (เช่น purple-700)"))


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # ถ้ามี name_en ให้ใช้ name_en เป็น source, ถ้าไม่มีให้ใช้ name (ไทย)
            source_for_slug = self.name_en if self.name_en else self.name
            # slugify จะจัดการภาษาไทยได้ระดับหนึ่ง แต่ถ้าต้องการ slug ที่เป็นภาษาอังกฤษล้วนๆ การมี name_en จะดีกว่า
            self.slug = slugify(source_for_slug, allow_unicode=True if not self.name_en else False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("ประเภทผีเสื้อ")
        verbose_name_plural = _("01. ประเภทผีเสื้อ (Quiz)") # ลำดับใน Admin
        ordering = ['name']


class Question(models.Model):
    text = models.TextField(verbose_name=_("ข้อความคำถาม"))
    order = models.PositiveIntegerField(default=0, help_text=_("ลำดับการแสดงผลของคำถาม (เลขน้อยแสดงก่อน)"), verbose_name=_("ลำดับ"))
    # image = models.ImageField(upload_to='quiz_question_images/', blank=True, null=True, verbose_name=_("รูปภาพประกอบคำถาม"))

    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}..."

    class Meta:
        ordering = ['order'] # สำคัญมากเพื่อให้คำถามเรียงตามลำดับใน Quiz
        verbose_name = _("คำถาม Quiz")
        verbose_name_plural = _("02. คำถาม Quiz")


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE, verbose_name=_("ของคำถาม"))
    text = models.CharField(max_length=255, verbose_name=_("ข้อความตัวเลือก"))
    points_to_type = models.ForeignKey(
        ButterflyType,
        on_delete=models.SET_NULL,
        null=True, # อนุญาตให้เป็น null ถ้า ButterflyType ถูกลบ
        blank=False, # **สำคัญ: บังคับให้ต้องเลือก ButterflyType ตอนสร้าง Choice ผ่าน Admin**
                     # ถ้าไม่เลือก จะไม่รู้ว่า Choice นี้ให้คะแนนแก่ Type ไหน
        related_name="defining_choices",
        verbose_name=_("ให้คะแนนแก่ประเภทผีเสื้อ")
    )
    # image = models.ImageField(upload_to='quiz_choice_images/', blank=True, null=True, verbose_name=_("รูปภาพประกอบตัวเลือก"))

    def __str__(self):
        type_name = self.points_to_type.name if self.points_to_type else _("ไม่ได้ระบุประเภท")
        return f"{self.text} (-> {type_name})"

    class Meta:
        verbose_name = _("ตัวเลือกคำตอบ Quiz")
        verbose_name_plural = _("03. ตัวเลือกคำตอบ Quiz")
        # อาจจะเพิ่ม ordering ตาม text หรือตาม question ถ้าต้องการ
        # ordering = ['question__order', 'text']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_("ผู้ใช้"))
    bio = models.TextField(blank=True, null=True, verbose_name=_("เกี่ยวกับฉัน"))
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default_avatar.png', blank=True, null=True, verbose_name=_("รูปโปรไฟล์"))

    assigned_butterfly_type = models.ForeignKey(
        ButterflyType,
        on_delete=models.SET_NULL, # ถ้า ButterflyType ถูกลบ, field นี้ใน UserProfile จะเป็น NULL
        null=True,
        blank=True, # อนุญาตให้ UserProfile ยังไม่มี assigned_butterfly_type (เช่น ยังไม่ได้ทำ quiz)
        related_name='users_of_this_type',
        verbose_name=_("ประเภทผีเสื้อที่ได้รับ")
    )
    quiz_completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("วันที่ทำ Quiz เสร็จสิ้น"))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("โปรไฟล์ผู้ใช้")
        verbose_name_plural = _("04. โปรไฟล์ผู้ใช้")


# Signal เพื่อสร้าง UserProfile อัตโนมัติเมื่อ User ถูกสร้าง
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created: # ตรวจสอบว่า User object นี้เพิ่งถูกสร้างขึ้นหรือไม่
        UserProfile.objects.create(user=instance)

# Signal เพื่อ save UserProfile เมื่อ User object ถูก save (อาจจะไม่จำเป็นเสมอไปถ้าไม่มีการอัปเดตที่เชื่อมโยง)
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#    try:
#        instance.profile.save()
#    except UserProfile.DoesNotExist:
        # กรณีที่ profile อาจจะยังไม่ได้ถูกสร้าง (เช่น ถ้าปิด signal create_user_profile ชั่วคราว)
#        UserProfile.objects.create(user=instance)