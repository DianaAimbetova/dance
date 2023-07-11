from django.shortcuts import render
from .models import Profile
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
          group = Group.objects.get(name='Teacher')
          user = form.save(commit=False)
          user.set_password(form.cleaned_data['password'])
          user.save()
          if form.cleaned_data['role'] == 'TEACHER':
             user.groups.add(group)
          user.save()  
          if form.cleaned_data['role'] == 'TEACHER':
             Profile.objects.create(user = user, type = 'TEACHER')
          else:
             Profile.objects.create(user = user)
          return render(request, 'account/register_done.html',{'new_user': user})
    else:
       form = UserRegistrationForm()
       return render(request,'account/register.html',{'form': form} )
    
@login_required    
def edit(request):
   if request.method == 'POST':
      user_form = UserEditForm(instance=request.user,
                               data = request.POST)
      profile_form = ProfileEditForm(instance=request.user.profile,
                                      data = request.POST,
                                      files=request.FILES)
      if user_form.is_valid() and profile_form.is_valid():
         user_form.save()
         profile_form.save()
         messages.success(request, 'Profile updated successfully')
      else:
         messages.error(request, 'Error updating your profile')
   else:
      user_form = UserEditForm(instance=request.user)
      profile_form = ProfileEditForm(instance=request.user.profile)
    
   return render(request, 'account/edit.html', {'user_form' : user_form,
                                             'profile_form' : profile_form})


def get_teachers(request):
    users = Profile.objects.filter(type='TEACHER')
    return render(request, 'account/main.html', {'users':users})
