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
    target_user = get_object_or_404(User, username=username) if username else request.user
    profile, _ = UserProfile.objects.get_or_create(user=target_user)
    organized_events = Event.objects.filter(organizer=target_user)
    attending_events = Event.objects.filter(
        attendees__user=target_user,
        attendees__status='attending'
    )
    context = {
        'profile_user': target_user,
        'profile': profile,
        'organized_events': organized_events,
        'attending_events': attending_events,
        'is_own_profile': target_user == request.user
    }
    return render(request, 'myapp/user_profile.html', context)

@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user_profile')
    return render(request, 'myapp/edit_profile.html', {'form': form})

# --- Butterfly Quiz ---
@login_required
def butterfly_quiz_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if user_profile.assigned_butterfly_type and user_profile.quiz_completed_at:
        return redirect(reverse('butterfly_result_page_slug', kwargs={'slug': user_profile.assigned_butterfly_type.slug}))

    questions = Question.objects.prefetch_related('choices').order_by('order').all()
    page_title = "แบบทดสอบค้นหาผีเสื้อของคุณ" # ส่ง page_title ไปยัง template

    if request.method == 'POST':
        type_scores = {bt.id: 0 for bt in ButterflyType.objects.all()}
        all_questions_answered = True
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            if not choice_id:
                all_questions_answered = False
                break
            try:
                selected_choice = Choice.objects.get(id=choice_id, question=question)
                if selected_choice.points_to_type:
                    type_scores[selected_choice.points_to_type.id] += 1
            except Choice.DoesNotExist:
                all_questions_answered = False
                break

        if not all_questions_answered:
            context = {
                'questions': questions,
                'page_title': page_title,
                'error_message': "กรุณาตอบคำถามให้ครบทุกข้อ",
            }
            # --- Render template หน้าคำถาม Quiz ---
            return render(request, 'myapp/butterfly_quiz.html', context)

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
                final_winning_type_id = sorted(winning_type_ids)[0]
                assigned_type = ButterflyType.objects.get(id=final_winning_type_id)
                user_profile.assigned_butterfly_type = assigned_type
                user_profile.quiz_completed_at = timezone.now()
                user_profile.save()
                # --- Redirect ไปยังหน้าผลลัพธ์ ---
                return redirect(reverse('butterfly_result_page_slug', kwargs={'slug': assigned_type.slug}))
        else:
            context = {
                'questions': questions,
                'page_title': page_title,
                'error_message': "เกิดข้อผิดพลาดในการประมวลผลคำตอบ หรือคุณอาจจะยังไม่ได้เลือกคำตอบใดๆ",
            }
            # --- Render template หน้าคำถาม Quiz ---
            return render(request, 'myapp/butterfly_quiz.html', context)

    context = {
        'questions': questions,
        'page_title': page_title,
    }
    # --- Render template หน้าคำถาม Quiz ---
    return render(request, 'myapp/butterfly_quiz.html', context)


@login_required
def butterfly_result_view(request, slug):
    butterfly_type = get_object_or_404(ButterflyType, slug=slug)
    # user_profile, created = UserProfile.objects.get_or_create(user=request.user) # อาจจะไม่จำเป็นต้องดึง profile ที่นี่ ถ้าไม่ใช้

    # ถ้าต้องการตรวจสอบว่า user นี้เป็นคนได้ผลลัพธ์นี้จริงๆ
    # current_user_profile = request.user.profile
    # if current_user_profile.assigned_butterfly_type != butterfly_type:
    #     # อาจจะ redirect ไปผลลัพธ์ของ user เอง หรือแจ้งเตือน
    #     if current_user_profile.assigned_butterfly_type:
    #         return redirect(reverse('butterfly_result_page_slug', kwargs={'slug': current_user_profile.assigned_butterfly_type.slug}))
    #     else: # ถ้ายังไม่เคยทำ quiz
    #         return redirect(reverse('butterfly_quiz'))


    context = {
        'butterfly_type': butterfly_type,
        # page_title สามารถตั้งใน template butterfly_result.html ได้เลย
    }
    # --- Render template หน้าผลลัพธ์ Quiz ---
    return render(request, 'myapp/butterfly_result.html', context)

# ใน views.py
def signup(request):
    if request.user.is_authenticated: # เพิ่มบรรทัดนี้
        return redirect('home')      # เพิ่มบรรทัดนี้
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('butterfly_quiz') # ถูกต้อง
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

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
