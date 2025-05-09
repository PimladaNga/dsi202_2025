# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- Model เดิมของคุณ ---
class Community(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='communities/', blank=True, null=True) # ถูกต้องตามโครงสร้าง media ของคุณ
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Communities'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True) # เพิ่ม unique=True ถ้าชื่อ Category ไม่ควรซ้ำ
    image = models.ImageField(upload_to='categories/', blank=True, null=True) # ถูกต้อง

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(upload_to='events/') # ถูกต้อง
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_in_category') # เปลี่ยน related_name เล็กน้อย
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_in_community') # เปลี่ยน related_name เล็กน้อย
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def attendee_count(self):
        return self.attendees.filter(status='attending').count()

    class Meta:
        ordering = ['-date', '-time']


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('attending', 'เข้าร่วม'),
        ('interested', 'สนใจ'),
        ('not_attending', 'ไม่เข้าร่วม')
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_attendances') # เปลี่ยน related_name
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='attending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.event.title} - {self.get_status_display()}'

# --- Model ใหม่สำหรับโปรไฟล์ผีเสื้อ ---
class ButterflyType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="ชื่อประเภทผีเสื้อ")
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text="สร้างอัตโนมัติจากชื่อ (ภาษาอังกฤษ) ถ้าเว้นว่าง")
    description = models.TextField(verbose_name="คำอธิบายลักษณะ")
    icon_image = models.ImageField(upload_to='butterfly_type_icons/', blank=True, null=True, verbose_name="รูปไอคอนประจำประเภท") # ถูกต้อง
    theme_colors_description = models.CharField(max_length=255, blank=True, null=True, verbose_name="สี/ธีมที่สื่อถึง")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) # แนะนำให้ชื่อ name เป็นภาษาอังกฤษเพื่อให้ slug สวยงาม
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "ประเภทผีเสื้อ"
        verbose_name_plural = "01. ประเภทผีเสื้อ"
        ordering = ['name']


class Question(models.Model):
    text = models.TextField(verbose_name="ข้อความคำถาม")
    order = models.PositiveIntegerField(default=0, help_text="ลำดับการแสดงผลของคำถาม (เลขน้อยแสดงก่อน)", verbose_name="ลำดับ")

    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}..."

    class Meta:
        ordering = ['order']
        verbose_name = "คำถาม Quiz"
        verbose_name_plural = "02. คำถาม Quiz"


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE, verbose_name="ของคำถาม")
    text = models.CharField(max_length=255, verbose_name="ข้อความตัวเลือก")
    points_to_type = models.ForeignKey(
        ButterflyType,
        on_delete=models.SET_NULL,
        null=True, # สามารถเป็น Null ได้ถ้า Type นั้นถูกลบ แต่ควรมีค่าเสมอเมื่อสร้าง
        blank=False, # บังคับให้ต้องเลือกตอนสร้างผ่าน Admin
        related_name="defining_choices", # เปลี่ยน related_name
        verbose_name="ให้คะแนนแก่ประเภทผีเสื้อ"
    )

    def __str__(self):
        type_name = self.points_to_type.name if self.points_to_type else "N/A"
        return f"{self.text} (-> {type_name})"

    class Meta:
        verbose_name = "ตัวเลือกคำตอบ Quiz"
        verbose_name_plural = "03. ตัวเลือกคำตอบ Quiz"


# UserProfile Model (ปรับปรุง)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, verbose_name="เกี่ยวกับฉัน")
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="รูปโปรไฟล์") # ถูกต้อง

    assigned_butterfly_type = models.ForeignKey(
        ButterflyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users_of_this_type', # เปลี่ยน related_name
        verbose_name="ประเภทผีเสื้อที่ได้รับ"
    )
    quiz_completed_at = models.DateTimeField(null=True, blank=True, verbose_name="วันที่ทำ Quiz เสร็จสิ้น")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "โปรไฟล์ผู้ใช้"
        verbose_name_plural = "04. โปรไฟล์ผู้ใช้"


# Signal เพื่อสร้าง UserProfile อัตโนมัติเมื่อ User ถูกสร้าง
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance) # ใช้ get_or_create เพื่อความปลอดภัย
    else:
        
        try:
            instance.profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance) # สร้าง profile ถ้ายังไม่มีจริงๆ