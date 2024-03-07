from .forms import CustomDurationForm

from .models import Activity, ActivityUpdate, Staffuser
from django.db.models import Count, Prefetch


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
# views.py
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity#, ActivityUpdate
from .forms import ActivityForm#, ActivityUpdateForm

from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required



def tryy(request):
    return render(request, 'try.html')

@login_required
def create_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.created_by_id = request.user.id
            form.save()
            return redirect('activity_list')
    else:
        form = ActivityForm()
    return render(request, 'create_activity.html', {'form': form})


@login_required
def update_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity_update = activity.activityupdate_set.first()
    print(activity.name)
    
    print(activity.status)
    
    print(activity.comment)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            update = form.save(commit=False)
            update.activity = activity
            update.user = request.user
            # update.updated_by = request.user
            update.updated_at = timezone.now()
            update.save()
            
            
            # if activity_update:
            #     activity_update.status = form.cleaned_data['status']
            #     activity_update.remark = form.cleaned_data['comment']
            #     activity_update.updated_by = request.user
            #     activity_update.save()
            # else:
            ActivityUpdate.objects.create(
                    activity=activity,
                    status=form.cleaned_data['status'],
                    remark=form.cleaned_data['comment'],
                    updated_by=request.user
                )
                
            return redirect('activity_list')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'update_activity.html', {'form': form, 'activity': activity})


# def update_activity(request, activity_id):
#     activity = get_object_or_404(Activity, pk=activity_id)
#     if request.method == 'POST':
#         form = ActivityForm(request.POST, instance=activity)
#         if form.is_valid():
#             form.save()
#             return redirect('activity_list')  # Assuming you have a view named 'activity_list' to redirect to
#     else:
#         form = ActivityForm(instance=activity)
#     return render(request, 'update_activity.html', {'form': form, 'activity': activity})


@login_required
def activity_list(request):
    activities = Activity.objects.all()
    activities_count = activities.count()
    return render(request, 'index.html', {'activities': activities, 'activities_count': activities_count, 'user': request.user})





def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('activity_list')  # Redirect to home page after successful login
        else:
            context = {'error_message': 'Invalid username or password.', 'username': request.POST['username'], 'password': request.POST['password']}
            # Return an 'invalid login' error message.
            return render(request, 'auth-login.html', context=context)
    else:

        return render(request, 'auth-login.html',)
    
    
    
    
    


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout





def user_registration(request):
    print("okay")
    if request.method == 'POST':
        print("bad")
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            position = form.cleaned_data['position']
            contact = form.cleaned_data['contact']
            password = form.cleaned_data['password']
            user = Staffuser.objects.create_user(username=username, email=email, position=position, contact=contact, password=password)
            # Optionally, you can log in the user after registration
            # login(request, user)
            return redirect('login')  # Redirect to login page after successful registration
        
        
        context = {'form': form, 'error_message': 'Registration Unsuccessful', 'username': request.POST['username'], 'email': request.POST['email'], 'password': request.POST['password'], 'position': request.POST['position'], 'contact': request.POST['contact'],}
        return render(request, 'auth-register.html', context=context)
    else:
        form = UserRegistrationForm()
    return render(request, 'auth-register.html', {'form': form})




# views.py

def activity_updates_per_day(request):
    activities_with_updates = Activity.objects.prefetch_related(
        Prefetch('activityupdate_set', queryset=ActivityUpdate.objects.order_by('-updated_at'))
    ).annotate(num_updates=Count('activityupdate')).order_by('-num_updates')
    return render(request, 'activity_updates_per_day.html', {'activities_with_updates': activities_with_updates})



def activity_history(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    # Retrieve all activity updates for the clicked activity
    updates = ActivityUpdate.objects.filter(activity=activity).order_by('-updated_at')
    update_count = updates.count()
    return render(request, 'activity_history.html', {'activity': activity, 'updates': updates, 'updates_count': update_count})





# views.py


def activity_history_report(request):
    if request.method == 'POST':
        form = CustomDurationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            activity_histories = ActivityUpdate.objects.filter(updated_at__date__range=[start_date, end_date])
            activity_count = activity_histories.count()
            print(activity_count )
            return render(request, 'activity_history_report.html', {'activity_histories': activity_histories, 'form': form, 'activity_count': activity_count})
    else:
        form = CustomDurationForm()
    return render(request, 'activity_history_report.html', {'form': form})



def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.method == 'POST':
        activity.delete()
        return redirect('activity_list')
    return render(request, 'delete_confirmation1.html', {'activity': activity})

def delete_activity_history(request, activity_id):
    activity_updates =  get_object_or_404(ActivityUpdate, pk=activity_id)
    activity_updates.delete()
    return redirect('activity_list')