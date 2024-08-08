from django.shortcuts import redirect, render
from userauths.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, ProfileCreateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User, Profile
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator


#User = settings.AUTH_USER_MODEL

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey {username}, your account was created successfuly')

            # Authenticate the user with the username and password from the form
            user = authenticate(username=form.cleaned_data.get('email'),
                                    password=form.cleaned_data.get('password1')
            )
            if user is not None:
                login(request, user)
                return redirect('userauths:profile-create') # Redirect to profile creation 
    else:
        print('User cannot be registerd')
        form = UserRegistrationForm()

    form = UserRegistrationForm()
    context = {'form' : form }
    return render(request, "userauths/sign-up.html", context)


def login_view(request):

    if request.user.is_authenticated: #if the user is loged in 
        return redirect('userauths:profile_list') #redirect them to the profile lists 
    
    if request.method == "POST": # here the user has key in the input fields 
        email = request.POST.get("email") # we get the email, and password down below then compare if they are corect 
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in")
                return redirect("userauths:profile_list")
            else:
                messages.warning(request, "Incorrect email or password or User does not exist. Create an account")

        except:
            messages.warning(request, f'User with {email} does not exist')


    context = {

    }

    return render(request, "userauths/sign-in.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You are loged out.")
    return render( request, "library/index.html") 


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'userauths/profile.html', context)

#method_decorator(login_required, name='dispatch')
#class profileList(View):
    #model = Profile
    #template_name = 'userauths/profile_list.html'
    #context_object_name = 'profiles'

    #def get(self, request, *args, **kwargs): 
        #profile = request.user.user_profiles.all()

#        context = {
 #           'profiles': profile
  #      }
   #     return render(request, 'userauths/profilelist.html', context)

@method_decorator(login_required, name='dispatch')
class ProfileList(View):
    template_name = 'userauths:profilelist.html'
    context_object_name = 'profiles'

    def get(self, request, *args, **kwargs):
        profiles = request.user.user_profiles.all()  # Assuming 'profiles' is the related name for Profile model

        context = {
            'profiles': profiles
        }
        return render(request, 'userauths/profilelist.html', context)
    
    
@method_decorator(login_required, name='dispatch')
class ProfileCreate(View):
    def get(self, request, *args, **kwargs):
        form = ProfileCreateForm()
        context = {
            'form': form
        }
        return render(request, 'userauths/ProfileCreate.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ProfileCreateForm(request.POST, request.FILES)  # Note the addition of request.FILES
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Assuming you want to link the profile to the logged-in user
            profile.save()
            return redirect('userauths:profile_list')  # Change this to the appropriate URL name for your profile list
        context = {
            'form': form
        }
        return render(request, 'userauths/ProfileCreate.html', context)
