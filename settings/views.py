from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from settings.forms import ProfileUpdateForm
from userauths.models import Profile, User


# Create your views here.
@login_required
def profile_update(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_update', profile_id=profile.id)
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'settings/profile_update.html', {'form': form, 'profile': profile})

@login_required
def profile_delete(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Your profile has been deleted successfully!')
        return redirect('home')  # or wherever you want to redirect after deletion
    return render(request, 'settings/profile_confirm_delete.html', {'profile': profile})

@login_required
def account_display(request, user_id, profile_id):
    '''A view that displays the account details at the front end'''

    # Fetch the profile for the given user and profile_id
    profile = get_object_or_404(Profile, id=profile_id, user_id=user_id)

    context = {
        'profile': profile,
    }
    return render(request, 'settings/account.html', context)