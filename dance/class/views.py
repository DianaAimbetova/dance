from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Class, Likes
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic.detail import DetailView
from .forms import ClassEnrollForm, ClassForm
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.apps import apps
from django.forms.models import modelform_factory
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import logging
import sys


# Create your views here.
class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    
class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class OwnerClassMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = Class
    fields = ['title', 'slug', 'description']
    success_url = reverse_lazy('manage_class_list')

class OwnerClassEditMixin(OwnerClassMixin, OwnerEditMixin):
    template_name = 'classes/manage/class/form.html'

class ManageClassListView(OwnerClassMixin, ListView):
    template_name = 'classes/manage/class/list.html'
    permission_required = 'class.view_class'

class ClassCreateView(OwnerClassEditMixin, CreateView):
    permission_required = 'class.add_class'

class ClassUpdateView(OwnerClassEditMixin, UpdateView):
    permission_required = 'class.change_class'

class ClassDeleteView(OwnerClassMixin, DeleteView):
    template_name = 'classes/manage/class/delete.html'
    permission_required = 'class.delete_class'

class ClassListView(TemplateResponseMixin, View):
    model = Class
    template_name = 'classes/class/list.html'

    def get(self, request):
        if request.user.groups and request.user.groups.filter(name='Teacher').exists() :
            classes = Class.objects.filter(teacher=request.user, planned_date__gt=timezone.now())
        else:
            classes = Class.objects.filter(planned_date__gt=timezone.now())
        paginator = Paginator(classes, 2)
        page = request.GET.get('page')
        classes_only = request.GET.get('classes_only')
        try:
            classes = paginator.page(page)
        except PageNotAnInteger:
            classes = paginator.page(1)
        except EmptyPage:
            if classes_only:
                return HttpResponse('')
            classes = paginator.page(paginator.num_pages)
        if classes_only:
             return render(request,'classes/class/class_list.html',
                      {'classes': classes})
        return self.render_to_response({'classes': classes})
    

class ClassDetailView(DetailView):
        model = Class
        template_name = 'classes/class/detail.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['enroll_form'] = ClassEnrollForm(
                                    initial={'course':self.object})
            return context

class StudentEnrollClassView(LoginRequiredMixin, FormView):
    course = None
    form_class = ClassEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('student_class_detail',
                            args=[self.course.id])
    

class StudentClassDetailView(DetailView):
    model = Class
    template_name = 'classes/student/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    

class ClassCreateUpdateView(LoginRequiredMixin, TemplateResponseMixin, View):
    module = None
    model = Class
    obj = None
    template_name = 'classes/manage/form.html'

    def get_form(self, model, *args, **kwargs):
        if self.request.user.groups.filter(name='Teacher').exists():
            return ClassForm(*args, **kwargs)
        else:
            raise PermissionDenied

    def dispatch(self, request, id=None):
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         teacher=request.user)
        return super().dispatch(request, id)

    def get(self, request,  id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.teacher = request.user
            obj.save()
        return HttpResponseRedirect(reverse('class'))
    

@login_required
@require_POST
def class_like(request):
    class_id = request.POST.get('id')
    action = request.POST.get('action')
    if class_id and action:
        try:
            my_class = Class.objects.get(id=class_id)
            if action == 'like':
                my_class.users_like.add(request.user)
                my_class.likes_count = my_class.likes_count + 1
                Likes.objects.create(user=request.user, dance_class=my_class)
            else:
                my_class.users_like.remove(request.user)
                my_class.likes_count = my_class.likes_count - 1
                Likes.objects.filter(user=request.user, dance_class=my_class).delete()
            my_class.save()
            return JsonResponse({'status': 'ok'})
        except Class.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

class FavouriteClassListView(TemplateResponseMixin, View):
    model = Class
    template_name = 'classes/class/favourite_list.html'

    def get(self, request):
        classes = Class.objects.filter(planned_date__gt=timezone.now(), users_like__in=[self.request.user])
        paginator = Paginator(classes, 2)
        page = request.GET.get('page')
        classes_only = request.GET.get('classes_only')
        try:
            classes = paginator.page(page)
        except PageNotAnInteger:
            classes = paginator.page(1)
        except EmptyPage:
            if classes_only:
                return HttpResponse('')
            classes = paginator.page(paginator.num_pages)
        if classes_only:
             return render(request,'classes/class/class_list.html',
                      {'classes': classes})
        return self.render_to_response({'classes': classes})
    

class EnrolledClassListView(TemplateResponseMixin, View):
    model = Class
    template_name = 'classes/class/enrolled_list.html'

    def get(self, request):
        classes = Class.objects.filter(planned_date__gt=timezone.now(), students__in=[self.request.user])
        paginator = Paginator(classes, 2)
        page = request.GET.get('page')
        classes_only = request.GET.get('classes_only')
        try:
            classes = paginator.page(page)
        except PageNotAnInteger:
            classes = paginator.page(1)
        except EmptyPage:
            if classes_only:
                return HttpResponse('')
            classes = paginator.page(paginator.num_pages)
        if classes_only:
             return render(request,'classes/class/class_list.html',
                      {'classes': classes})
        return self.render_to_response({'classes': classes})
    
@login_required
@require_POST
def remove_class(request):
    class_id = request.POST.get('id')
    if class_id:
        try:
            class_to_remove = get_object_or_404(Class,
                            id=class_id)
            class_to_remove.delete()
            return JsonResponse({'status': 'ok'})
        except Class.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})
    
    

