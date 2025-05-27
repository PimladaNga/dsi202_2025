from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from functools import wraps
from .models import Event, Community, Attendance
from django.utils import timezone # สำหรับ pro_membership_end_date
from datetime import timedelta # สำหรับ pro_membership_end_date
from django.core.exceptions import PermissionDenied
from .promptpay_utils import generate_promptpay_qr_payload, generate_qr_code_image_base64, InvalidInputError
import base64

from .models import (
    Event, Category, Attendance, UserProfile, Community,
    ButterflyType, Question, Choice
)
from .forms import EventForm, UserProfileForm

# --- หน้าหลัก ---
def index(request):
    return HttpResponse("Hello from myapp!")

def home(request):
    featured_events = Event.objects.all().order_by('-created_at')[:4]
    categories = Category.objects.all()
    communities = Community.objects.all()
    context = {
        'featured_events': featured_events,
        'categories': categories,
        'communities': communities,
    }
    return render(request, 'myapp/home.html', context)

# --- Event views ---
class EventListView(ListView):
    model = Event
    template_name = 'myapp/event_list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        queryset = Event.objects.all().order_by('date', 'time')
        category_id = self.request.GET.get('category')
        community_id = self.request.GET.get('community')
        search_query = self.request.GET.get('search')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if community_id:
            queryset = queryset.filter(community_id=community_id)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['communities'] = Community.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['selected_community'] = self.request.GET.get('community')
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'myapp/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['attendance'] = Attendance.objects.get(
                    event=self.object, user=self.request.user
                )
            except Attendance.DoesNotExist:
                context['attendance'] = None
        context['attendees'] = self.object.attendees.filter(status='attending')
        context['interested'] = self.object.attendees.filter(status='interested')
        context['related_events'] = (
            Event.objects.filter(category=self.object.category)
            .exclude(id=self.object.id)[:4]
            if self.object.category else Event.objects.none()
        )
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'myapp/event_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'myapp/event_form.html'

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.organizer != request.user:
            return redirect('event_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

@login_required
def attend_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    status = request.POST.get('status', 'attending')
    Attendance.objects.update_or_create(
        event=event,
        user=request.user,
        defaults={'status': status}
    )
    return redirect('event_detail', pk=pk)

# --- User Profile ---
@login_required
def user_profile(request, username=None):
    if username:
        # ดูโปรไฟล์ของคนอื่น
        target_user = get_object_or_404(User, username=username)
    else:
        # ดูโปรไฟล์ของตัวเอง (เมื่อเข้า /profile/ โดยไม่มี username)
        target_user = request.user

    # ดึง UserProfile (จะถูกสร้างอัตโนมัติโดย signal ถ้ายังไม่มี)
    profile, created = UserProfile.objects.get_or_create(user=target_user)
    is_own_profile = (request.user == target_user)

    # ดึงข้อมูลกิจกรรมที่เกี่ยวข้อง (สามารถเพิ่ม .order_by() เพื่อจัดเรียงได้)
    organized_events = Event.objects.filter(organizer=target_user).order_by('-created_at')
    attending_events = Event.objects.filter(
        attendees__user=target_user,
        attendees__status='attending'
    ).order_by('-date', '-time') # เรียงจากกิจกรรมล่าสุด

    context = {
        'profile_user': target_user,        # User object ของเจ้าของโปรไฟล์ที่กำลังดู
        'profile': profile,                 # UserProfile object ของเจ้าของโปรไฟล์
        'organized_events': organized_events,
        'attending_events': attending_events,
        'is_own_profile': is_own_profile    # Boolean เพื่อตรวจสอบใน template
    }
    return render(request, 'myapp/user_profile.html', context)

def pro_member_required(view_func):
    @wraps(view_func) # ควร import wraps จาก functools
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'profile', None) or not request.user.profile.is_pro_member:
            # อาจจะ redirect ไปหน้า pro_membership หรือแสดง error
            # raise PermissionDenied 
            return redirect('pro_membership') # หรือแสดงหน้าว่าต้องเป็นโปร
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# การใช้งานใน view
# from .decorators import pro_member_required # ถ้าสร้างไฟล์แยก

@login_required
@pro_member_required # <--- เพิ่ม decorator นี้
def my_pro_feature_view(request):
    # ... logic สำหรับ pro feature ...
    return render(request, 'myapp/pro_feature_template.html')

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    # --- ตรวจสอบว่าคุณมี UserProfileForm ใน forms.py หรือยัง ---
    # ถ้ายังไม่มี อาจจะต้องสร้าง form นี้ก่อน หรือใช้ Django's ModelForm
    # from .forms import UserProfileForm # (ถ้ายังไม่ได้ import)

    # สมมติว่าคุณมี UserProfileForm ที่รับ instance ของ UserProfile
    # และสามารถจัดการ field 'bio' และ 'profile_image' ได้
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # หลังจาก save ควรจะ redirect ไปยังหน้า profile ของตัวเอง
            return redirect('user_profile') # หรือ redirect('view_profile', username=request.user.username) ก็ได้
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'myapp/edit_profile.html', {'form': form})

# --- Butterfly Quiz ---
@login_required
def butterfly_quiz_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    questions = Question.objects.prefetch_related('choices').order_by('order').all()
    page_title = "แบบทดสอบค้นหาผีเสื้อของคุณ"
    error_message = None # กำหนดค่าเริ่มต้น error_message

    if request.method == 'POST':
        type_scores = {bt.id: 0 for bt in ButterflyType.objects.all()}
        all_questions_answered = True
        answered_question_ids = set() # เก็บ ID ของคำถามที่ตอบแล้ว

        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id: # ตรวจสอบว่ามีการส่งค่า choice_id มาหรือไม่
                answered_question_ids.add(question.id)
                try:
                    selected_choice = Choice.objects.get(id=choice_id, question=question)
                    if selected_choice.points_to_type:
                        type_scores[selected_choice.points_to_type.id] += 1
                except Choice.DoesNotExist:
                    # กรณีนี้ไม่ควรเกิดขึ้นถ้า choice_id ถูกต้อง แต่ใส่ไว้เพื่อความปลอดภัย
                    all_questions_answered = False # หรือจะตั้ง error_message ก็ได้
                    error_message = "มีข้อผิดพลาดในการเลือกคำตอบ กรุณาลองใหม่อีกครั้ง"
                    break
            # ไม่จำเป็นต้อง break ถ้าคำถามไม่ได้ถูกตอบทั้งหมดในครั้งเดียว
            # การตรวจสอบจะทำหลังจาก loop

        # ตรวจสอบว่าตอบครบทุกคำถามหรือไม่
        if len(answered_question_ids) != questions.count():
            all_questions_answered = False
            error_message = "กรุณาตอบคำถามให้ครบทุกข้อ"

        if not all_questions_answered:
            context = {
                'questions': questions,
                'page_title': page_title,
                'error_message': error_message,
            }
            return render(request, 'myapp/butterfly_quiz_form.html', context) # <--- แก้ไขชื่อ template

        # ตรวจสอบว่ามีคะแนนเกิดขึ้นหรือไม่ (ป้องกันกรณีที่ไม่มีการเลือก choice ใดๆ ที่ให้คะแนน)
        if any(score > 0 for score in type_scores.values()):
            highest_score = -1
            winning_type_ids = []
            for type_id, score in type_scores.items():
                if score > highest_score:
                    highest_score = score
                    winning_type_ids = [type_id]
                elif score == highest_score:
                    winning_type_ids.append(type_id)

            if winning_type_ids:
                # เลือก type แรกถ้ามีคะแนนเท่ากันหลายตัว (หรือจะสุ่มก็ได้ถ้าต้องการ)
                final_winning_type_id = sorted(winning_type_ids)[0]
                assigned_type = ButterflyType.objects.get(id=final_winning_type_id)
                user_profile.assigned_butterfly_type = assigned_type
                user_profile.quiz_completed_at = timezone.now()
                user_profile.save()
                return redirect(reverse('butterfly_result_page_slug', kwargs={'slug': assigned_type.slug}))
            else: # กรณีที่วน loop แล้วไม่เจอ winning_type_ids (ไม่ควรเกิดขึ้นถ้า logic ถูกต้อง)
                error_message = "ไม่สามารถคำนวณผลลัพธ์ได้ กรุณาลองใหม่อีกครั้ง"
        else: # กรณีที่ไม่มีคะแนนใดๆ เลย (เช่น ตอบแต่ choice ที่ไม่มี points_to_type หรือไม่ได้ตอบเลย)
             error_message = "กรุณาเลือกคำตอบ หรือเกิดข้อผิดพลาดในการประมวลผล"


        # ถ้ามาถึงตรงนี้ แสดงว่ามีปัญหาบางอย่างในการประมวลผล หรือไม่มีคะแนน
        context = {
            'questions': questions,
            'page_title': page_title,
            'error_message': error_message if error_message else "เกิดข้อผิดพลาดบางอย่าง กรุณาลองใหม่",
        }
        return render(request, 'myapp/butterfly_quiz_form.html', context) # <--- แก้ไขชื่อ template

    # สำหรับ GET request หรือถ้ายังไม่ได้ submit form
    context = {
        'questions': questions,
        'page_title': page_title,
    }
    return render(request, 'myapp/butterfly_quiz_form.html', context) # <--- แก้ไขชื่อ template


@login_required
def butterfly_result_view(request, slug):
    butterfly_type = get_object_or_404(ButterflyType, slug=slug)
    user_profile = get_object_or_404(UserProfile, user=request.user) # ดึงโปรไฟล์ของผู้ใช้ปัจจุบัน

    # (Optional) ตรวจสอบว่าผู้ใช้ที่เข้ามาดูผลลัพธ์ เป็นเจ้าของผลลัพธ์นั้นจริงๆ
    # หรือเป็นประเภทผีเสื้อที่ถูก assign ให้กับ user คนนั้น
    if user_profile.assigned_butterfly_type != butterfly_type:
        # ถ้าผลลัพธ์ที่ขอดูไม่ตรงกับที่ assign ไว้ อาจจะ redirect ไปที่ผลลัพธ์ของ user เอง
        if user_profile.assigned_butterfly_type:
            return redirect(reverse('butterfly_result_page_slug', kwargs={'slug': user_profile.assigned_butterfly_type.slug}))
        else:
            # ถ้า user ยังไม่เคยทำ quiz เลย ก็ให้กลับไปทำ quiz
            return redirect(reverse('butterfly_quiz'))

    context = {
        'butterfly_type': butterfly_type,
        # page_title สามารถตั้งใน template butterfly_result.html ได้เลย หรือส่งจาก view นี้ก็ได้
        # 'page_title': f"ผลลัพธ์ของคุณ: {butterfly_type.name}"
    }
    return render(request, 'myapp/butterfly_result.html', context)

# ใน views.py
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    # ดึงค่า next จาก POST (ถ้าฟอร์มถูก submit) หรือ GET (ถ้ามาจากลิงก์)
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # ตรวจสอบว่า redirect_to มีค่าและเป็น local URL หรือไม่
            # (การตรวจสอบนี้เป็นแบบง่ายๆ อาจจะต้องใช้ฟังก์ชันที่ซับซ้อนกว่านี้ถ้าต้องการความปลอดภัยสูงสุด)
            if redirect_to and redirect_to.startswith('/'):
                return redirect(redirect_to)
            else:
                # ถ้าไม่มี next หรือ next ไม่ปลอดภัย ให้ redirect ไปที่หน้า Quiz ตามปกติ
                return redirect(reverse('butterfly_quiz'))
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'next': redirect_to # ส่ง next ไปยัง template signup.html (สำหรับ hidden input)
    }
    return render(request, 'myapp/signup.html', context)

@login_required
def pro_membership_view(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        # สมมติว่าการ "สมัคร" คือการตั้งค่า is_pro_member = True
        # และกำหนดวันหมดอายุ (เช่น 30 วันนับจากนี้)
        user_profile.is_pro_member = True
        user_profile.pro_membership_start_date = timezone.now()
        user_profile.pro_membership_end_date = timezone.now() + timedelta(days=30) # ตัวอย่าง: ให้สิทธิ์ 30 วัน
        user_profile.save()
        # อาจจะเพิ่ม message บอกว่าสมัครสำเร็จ
        return redirect('user_profile') # กลับไปหน้าโปรไฟล์

    context = {
        'page_title': 'สมัครสมาชิกแบบโปร',
    }
    return render(request, 'myapp/pro_membership.html', context)

# --- REST Framework API ViewSets ---
from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer

# User API
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# UserProfile API
class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# --- กำหนดค่าสำหรับ PromptPay ของคุณ ---
# !!! 중요: เปลี่ยนเป็นเบอร์ PromptPay หรือเลข NID/Tax ID ของผู้รับเงินจริง !!!
# เพื่อการทดสอบ คุณอาจจะใช้เบอร์/เลขสมมติไปก่อนได้
YOUR_PROMPTPAY_ID_TYPE = "mobile"  # หรือ "nid"
YOUR_PROMPTPAY_ID = "0812345678"   # เบอร์มือถือ 10 หลัก หรือ เลข NID/Tax ID 13 หลัก
PRO_MEMBERSHIP_PRICE = 50.00       # ราคาสมาชิกโปร (ตัวอย่าง)

@login_required
def pro_membership_view(request):
    user_profile = request.user.profile
    qr_image_base64 = None
    error_message = None
    promptpay_payload = None

    if request.method == 'POST':
        # ในขั้นตอนนี้ เรายังคง "เชื่อ" ว่าผู้ใช้จ่ายเงินแล้วเมื่อเขากดยืนยัน
        # ในระบบจริง คุณจะต้องมีวิธีตรวจสอบการชำระเงินที่ซับซ้อนกว่านี้
        user_profile.is_pro_member = True
        user_profile.pro_membership_start_date = timezone.now()
        user_profile.pro_membership_end_date = timezone.now() + timedelta(days=30) # ตัวอย่าง: 30 วัน
        user_profile.save()
        # messages.success(request, "คุณได้อัปเกรดเป็นสมาชิกโปรสำเร็จแล้ว!") # Optional
        return redirect('user_profile')
    else:
        # GET request: สร้าง QR code
        if not user_profile.is_pro_member:
            try:
                if YOUR_PROMPTPAY_ID_TYPE == "mobile":
                    promptpay_payload = generate_promptpay_qr_payload(
                        mobile=YOUR_PROMPTPAY_ID,
                        amount=PRO_MEMBERSHIP_PRICE,
                        one_time=True # เหมาะสำหรับจ่ายครั้งเดียว
                    )
                elif YOUR_PROMPTPAY_ID_TYPE == "nid":
                    promptpay_payload = generate_promptpay_qr_payload(
                        nid=YOUR_PROMPTPAY_ID,
                        amount=PRO_MEMBERSHIP_PRICE,
                        one_time=True
                    )
                # else: # เพิ่ม ewallet_id ที่นี่ถ้าต้องการ

                if promptpay_payload:
                    qr_image_base64 = generate_qr_code_image_base64(promptpay_payload)

            except InvalidInputError as e:
                error_message = f"เกิดข้อผิดพลาดในการสร้างข้อมูล QR Code: {e}"
            except Exception as e:
                error_message = f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}"
        
    context = {
        'page_title': 'สมัครสมาชิกแบบโปร' if not user_profile.is_pro_member else 'สถานะสมาชิกโปร',
        'qr_image_base64': qr_image_base64,
        'promptpay_payload': promptpay_payload, # ส่ง payload ไปแสดงผลด้วย (เผื่อ debug)
        'membership_price': PRO_MEMBERSHIP_PRICE,
        'error_message': error_message,
        'user_profile': user_profile # ส่ง user_profile ไปด้วย เพื่อเช็ค is_pro_member ใน template
    }
    return render(request, 'myapp/pro_membership.html', context)

@login_required # ตัวอย่าง: ถ้าต้องการให้เฉพาะผู้ที่ login แล้วเข้าถึงได้
def dashboard_page(request):
    user_count = User.objects.count()
    event_count = Event.objects.count()
    community_count = Community.objects.count()
    attendance_count = Attendance.objects.count()

    context = {
        'user_count': user_count,
        'event_count': event_count,
        'community_count': community_count,
        'attendance_count': attendance_count,
        'page_title': 'Dashboard Summary' # สามารถส่ง page_title ไปได้
    }
    return render(request, 'myapp/dashboard.html', context) # ชี้ไปที่ template dashboard.html
