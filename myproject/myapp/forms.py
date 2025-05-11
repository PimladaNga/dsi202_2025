from django import forms
from .models import Event, UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500'}),
            # Django จะจัดการ widget สำหรับ ImageField ให้เอง แต่สามารถ custom เพิ่มได้ถ้าต้องการ
        }
        labels = {
            'bio': 'เกี่ยวกับฉัน (Bio)',
            'profile_image': 'รูปโปรไฟล์ใหม่ (ถ้าต้องการเปลี่ยน)',
        }
        help_texts = {
            'profile_image': 'หากไม่เลือกไฟล์ใหม่ รูปเดิมจะยังคงอยู่',
        }

class EventForm(forms.ModelForm): # (ถ้าคุณใช้ ModelForm สำหรับ Event ด้วย)
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'time', 'image', 'category', 'community', 'max_attendees']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'your-tailwind-classes-for-date-input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'your-tailwind-classes-for-time-input'}),
            # เพิ่ม widgets และ styling สำหรับ field อื่นๆ ตามต้องการ
        }