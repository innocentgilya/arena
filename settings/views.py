from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from settings.forms import ProfileUpdateForm
from userauths.models import Profile, User
from django.views import View
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ProfileUpdate(View):
    """A view that handles profile update settings."""

    def get(self, request, *args, **kwargs):
        profile_id = kwargs.get('profile_id')
        profile = get_object_or_404(Profile, id=profile_id, user=request.user)
        form = ProfileUpdateForm(instance=profile)
        context = {
            'form': form,
            'profile': profile,
        }
        return render(request, 'settings/profile_update.html', context)

    def post(self, request, *args, **kwargs):
        profile_id = kwargs.get('profile_id')
        profile = get_object_or_404(Profile, id=profile_id, user=request.user)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('library:profile-home',  profile_id=profile.id)  # Replace with the correct success URL
        else:
            context = {
                'form': form,
                'profile': profile,
            }
            return render(request, 'settings/profile_update.html', context)
        


        
        
@login_required
def profile_update(request, profile_id):
    '''a function that let you update your profile'''
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('userauths/profilelist', profile_id=profile.id)
    else:
        form = ProfileUpdateForm()
    return render(request, 'settings/account.html', {'form': form, 'profile': profile})




@login_required
def profile_delete(request, profile_id):
    '''this allows you to delete a profile '''
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Your profile has been deleted successfully!')
        return redirect('home')  # or wherever you want to redirect after deletion
    return render(request, 'settings/profile_confirm_delete.html', {'profile': profile})




@login_required
def account_display(request, user_id, profile_id):
    '''  displays the account details at the front end'''
    # Fetch the profile for the given user and profile_id
    profile = get_object_or_404(Profile, id=profile_id, user_id=user_id)

    context = {
        'profile': profile,
    }
    return render(request, 'settings/account.html', context)




@login_required
def account_settings_display(request, user_id):
    '''a view function to display account settings'''
    account = get_object_or_404(User, user_id=user_id)
    context = {
        'account': account
    }
    return render(request, 'settings/accountsettings.html', context)







@login_required
def account_delete(request):
    """
    Allows a user to delete their account.
    """
    user = request.User
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Your account has been deleted successfully!')
        return redirect('home')  # Adjust to your desired post-deletion route, e.g., a landing or login page.

    return render(request, 'settings:account_confirm_delete.html', {'user': user})




