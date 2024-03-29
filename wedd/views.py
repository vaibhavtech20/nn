from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required 
# from .models import kumbi
from .models import MatrimonialProfile
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from django.views.generic import  ListView
from django.template import loader
from django.urls import reverse
# from .forms import kumbiForm
# Create your views here.
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render
from acc.models import CustomUser
# from .forms import MatrimonialProfileForm , ProfilePictureForm
from .forms import MatrimonialProfileForm 
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        # Create a new user instance
        if password == password1:
            user = CustomUser(email=email,name=name)
            user.set_password(password)
            user.save()
            return redirect('login')
        # Optionally, log the user in after registration
        # login(request, user)
        else:
            messages.info(request, 'Passwords do not match.')
          # Redirect to the login page or another desired page

    return render(request, 'register.html')


def login(request):
    if request.session.has_key('is_logged'):
        return redirect('profile')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
       
        if user is not None:
            auth.login(request, user)
            request.session['is_logged'] = True
            return redirect('profile')
            # login(request, user)
            # messages.success(request, 'Login successful!')
            # return redirect('profile')
        else:
            messages.info(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'login.html')

def logout(request): 
    auth.logout(request)
    return redirect('login')


# @login_required(login_url='login')
# def profile(request):
#     user = request.user
#     user_profile_exists = MatrimonialProfile.objects.filter(user=user).exists()

#     if user_profile_exists:
#         MatrimonialProfiles = MatrimonialProfile.objects.all()
#         data = {
#             'MatrimonialProfiles': MatrimonialProfiles,
#         }
#         return render(request, 'profile.html', data)
#     else:
#         return redirect('create_profile')

# @login_required(login_url='login')
# def profile(request):
#     user_profile_exists = MatrimonialProfile.objects.filter(email=request.user.email).exists()

#     if user_profile_exists:
#         MatrimonialProfiles = MatrimonialProfile.objects.all()
#         data = {
#             'MatrimonialProfiles': MatrimonialProfiles,
#         }
#         return render(request, 'profile.html',  data)
#     else:
#         return redirect('create_profile')

# @login_required(login_url='login')
# def profile(request):
#     # यहां हम request.user.profile का उपयोग करके उपयोगकर्ता की प्रोफ़ाइल की जानकारी प्राप्त कर रहे हैं।
#     user_profile = request.user.email

#     # प्रोफ़ाइल मौजूद है या नहीं यह जाँचें
#     if user_profile:
#         MatrimonialProfiles = MatrimonialProfile.objects.all()
#         data = {
#             'user_profile': user_profile,
#             'MatrimonialProfiles': MatrimonialProfiles,
#         }
#         return render(request, 'profile.html', data)
#     else:
#         # प्रोफ़ाइल नहीं है, तो प्रोफ़ाइल बनाने के लिए पेज पर पुनर्निर्देशित करें
#         return redirect('create_profile')

@login_required(login_url='login')
def profile(request):
    try:
        user_profile = MatrimonialProfile.objects.get(email=request.user.email)
    except MatrimonialProfile.DoesNotExist:
        # If the profile doesn't exist, redirect to the profile creation page or handle it as per your requirements
        return redirect('create_profile')

    other_profiles = MatrimonialProfile.objects.exclude(email=request.user.email)
    
    context = {
        'user_profile': user_profile,
        'other_profiles': other_profiles,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def create_profile(request):
    if request.method == 'POST':
        form = MatrimonialProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Replace 'profile_list' with the URL pattern for listing profiles
    else:
        form = MatrimonialProfileForm()
    
    return render(request, 'create_profile.html', {'form': form})

@login_required(login_url='login')
def update_profile(request):
    user_profile = MatrimonialProfile.objects.get(email=request.user.email)

    if request.method == 'POST':
        form = MatrimonialProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page after successful update
    else:
        form = MatrimonialProfileForm(instance=user_profile)

    context = {
        'form': form,
    }

    return render(request, 'update_profile.html', context)



# def create_profile(request):
#     if request.method == 'POST':
#         profile_form = MatrimonialProfileForm(request.POST)
#         # picture_form = ProfilePictureForm(request.POST, request.FILES)
#         #  and picture_form.is_valid()
#         if profile_form.is_valid():
#             profile = profile_form.save(commit=False)
#             profile.user = request.user
#             profile.save()

#             # picture = picture_form.save(commit=False)
#             # picture.save()
            
#             # profile.profile_pics.add(picture)

#             return redirect('profile')  # Redirect to the profile page or any other page
#     else:
#         profile_form = MatrimonialProfileForm()
#         # picture_form = ProfilePictureForm()

#     return render(request, 'create_profile.html', {'profile_form': profile_form})
#     # , 'picture_form': picture_form
        
# def create_profile(request):
#     if request.method == 'POST':
#         form = MatrimonialProfileForm(request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             return redirect('profile')  # Redirect to a success page
#     else:
#         form = MatrimonialProfileForm()

#     return render(request, 'create_profile.html', {'form': form})


# @login_required(login_url='login')
# def profile(request):
#     MatrimonialProfiles= MatrimonialProfile.objects.all()
#     data = {
#           'MatrimonialProfiles' : MatrimonialProfiles,
#     }
#     # return render(request, 'home.html',data)
#     return render(request,'profile.html',data)

# views.py

# @login_required(login_url='login')
# def profile(request):
#     # Assuming the user is logged in
#     if request.user.is_authenticated:
#         user_name = request.user.name 
#         user_profile = MatrimonialProfile.objects.get(user=request.name)
#         other_profiles = MatrimonialProfile.objects.exclude(user=request.name)
#         return render(request, 'profile.html', {'user_name': user_name,'user_profile': user_profile, 'other_profiles': other_profiles})
#         # return render(request, 'profile.html', {'user_profile': user_profile, 'other_profiles': other_profiles})
#     else:
#         # Handle the case where the user is not logged in
#         return render(request, 'profile.html', {'user_name': None,'user_profile': None, 'other_profiles': None})
#         # return render(request, 'profile.html', {'user_profile': None, 'other_profiles': None})



# def profile(request):


#     user = request.user
#     # Retrieve logged-in user's profile
#     user_profile = MatrimonialProfile.objects.get(user=user)

#     # Retrieve all other profiles (excluding the logged-in user)
#     all_profiles = MatrimonialProfile.objects.exclude(user=user)

#     context = {
#         'user_profile': user_profile,
#         'all_profiles': all_profiles,
#     }

#     return render(request, 'profiles.html', context)



def home(request):
    return render(request,'home.html')

# views.py

# from django.shortcuts import render, redirect
# from .forms import MatrimonialProfileForm

# def create_profile(request):
#     if request.method == 'POST':
#         form = MatrimonialProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # Redirect to a success page
#     else:
#         form = MatrimonialProfileForm()

#     return render(request, 'create_profile.html', {'form': form})

# from django.shortcuts import render, get_object_or_404
# def profile_detail(request, profile_id):
#     profile = get_object_or_404(MatrimonialProfile, pk=profile_id)
#     return render(request, 'profile_detail.html', {'profile': profile})
# @login_required(login_url='login')
# def profile_detail(request):
#     # try:
#     #     user_profile = MatrimonialProfile.objects.get(email=request.user.email)
#     # except MatrimonialProfile.DoesNotExist:
#     #     # If the profile doesn't exist, redirect to the profile creation page or handle it as per your requirements
#     #     return redirect('create_profile')

#     other_profiles = MatrimonialProfile.objects.exclude(email=request.user.email)
    
#     context = {
#         # 'user_profile': user_profile,
#         'other_profiles': other_profiles,
#     }

#     return render(request, 'profile_detail.html', context)

# views.py

# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse

# from .models import MatrimonialProfile, Interaction

# def send_interaction(request, action, receiver_id):
#     sender_profile = get_object_or_404(MatrimonialProfile, user=request.user)
#     receiver_profile = get_object_or_404(MatrimonialProfile, id=receiver_id)

#     # Check if the interaction already exists
#     existing_interaction = Interaction.objects.filter(sender=sender_profile, receiver=receiver_profile, action=action).exists()

#     if not existing_interaction:
#         Interaction.objects.create(sender=sender_profile, receiver=receiver_profile, action=action)
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'already_exists'})

# def profile_detail(request, MatrimonialProfile_id):
#     # Retrieve profile details and interactions for the current user
#     profile = get_object_or_404(MatrimonialProfile, id=MatrimonialProfile_id)
#     interactions = Interaction.objects.filter(sender=request.user.profile, receiver=profile)

#     return render(request, 'profile_detail.html', {'profile': profile, 'interactions': interactions})

# Features app 
# views.py

from django.shortcuts import render, redirect
from features.models import Interest,Message,Shortlist,ConnectionRequest

def send_interest(request, receiver_id):
    sender_profile = MatrimonialProfile.objects.get(email=request.user.email)
    # receiver_profile = MatrimonialProfile.objects.exclude(id=request.user.id)
    
    receiver_profile = MatrimonialProfile.objects.exclude(email=request.user.email).get(id=receiver_id)
    # Check if the interest is not already sent
    existing_interest = Interest.objects.filter(sender=sender_profile, receiver=receiver_profile)
    if not existing_interest.exists():
        Interest.objects.create(sender=sender_profile, receiver=receiver_profile)
    
    return redirect('profile_detail', receiver_id=receiver_id)

# views.py

def chat(request, receiver_id):
    # sender_profile = MatrimonialProfile.objects.get(user=request.user)
    # receiver_profile = MatrimonialProfile.objects.get(id=receiver_id)
    sender_profile = MatrimonialProfile.objects.get(email=request.user.email)
    
    receiver_profile = MatrimonialProfile.objects.exclude(email=request.user.email).get(id=receiver_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=sender_profile, receiver=receiver_profile, content=content)
    
    messages = Message.objects.filter(
        (Q(sender=sender_profile, receiver=receiver_profile) | Q(sender=receiver_profile, receiver=sender_profile))
    ).order_by('timestamp')

     # Fetch phone numbers
    phone_numbers = MatrimonialProfile.objects.filter(id__in=[sender_profile.id, receiver_profile.id])

    return render(request, 'chat.html', {'messages': messages, 'receiver_id': receiver_id , 'phone_numbers': phone_numbers})


# views.py

# def shortlist(request, profile_id):
#     # user_profile = MatrimonialProfile.objects.get(user=request.user)
#     # profile_to_shortlist = MatrimonialProfile.objects.get(id=profile_id)
#     user_profile = MatrimonialProfile.objects.get(email=request.user.email)
    
#     profile_to_shortlist = MatrimonialProfile.objects.exclude(email=request.user.email).get(id=profile_id)

#     # Check if the profile is not already shortlisted
#     existing_shortlist = Shortlist.objects.filter(user=user_profile, profile=profile_to_shortlist)
#     if not existing_shortlist.exists():
#         Shortlist.objects.create(user=user_profile, profile=profile_to_shortlist)
    
#     return redirect('profile_detail', profile_id=profile_id)


def shortlist(request, profile_id):
    user_profile = MatrimonialProfile.objects.get(email=request.user.email)
    profile_to_shortlist = MatrimonialProfile.objects.exclude(email=request.user.email).get(id=profile_id)

    existing_shortlist = Shortlist.objects.filter(user=user_profile, profile=profile_to_shortlist)
    if not existing_shortlist.exists():
        Shortlist.objects.create(user=user_profile, profile=profile_to_shortlist)

    # Assuming 'profiles' is a queryset of all profiles you want to display
    # on the page. Adjust this queryset according to your needs.
    profiles = MatrimonialProfile.objects.exclude(email=request.user.email)

    # Other context variables can be added as needed
    context = {
        'user_profile': user_profile,
        'profiles': profiles,
        'shortlisted_profile': profile_to_shortlist,  # The recently shortlisted profile
    }

    return render(request, 'profile.html', context)
#notification
from django.shortcuts import get_object_or_404
from features.models import Notification

def create_notification(user, content):
    Notification.objects.create(user=user, content=content)



@login_required
def profile_detail(request, receiver_id):
    # Get the receiver's profile
    # receiver_profile = get_object_or_404(MatrimonialProfile, id=request.receiver.id)
    receiver_profile = MatrimonialProfile.objects.exclude(email=request.user.email).get(id=receiver_id)

    # Check if the receiver is the logged-in user
    is_self_profile = request.user.email == receiver_profile.email

    # Check if the sender has already sent interest
    sender_has_sent_interest = False

    connection_request_accepted = False

    if not is_self_profile:
        sender_profile = MatrimonialProfile.objects.get(email=request.user.email)
        sender_has_sent_interest = receiver_profile.received_interests.filter(sender=sender_profile).exists()

        connection_request_accepted = check_connection_acceptance(sender_profile, receiver_profile)

    context = {
        'receiver_profile': receiver_profile,
        'is_self_profile': is_self_profile,
        'sender_has_sent_interest': sender_has_sent_interest,
        'connection_request_accepted': connection_request_accepted, 
    }

    return render(request, 'profile_detail.html', context)

# @login_required
# def profile_detail(request, receiver_id):
#     # Get the receiver's profile
#     receiver_profile = MatrimonialProfile.objects.exclude(email=request.user.email).get(id=receiver_id)

#     # Check if the receiver is the logged-in user
#     is_self_profile = request.user.email == receiver_profile.email

#     # Check if the sender has already sent a connection request
#     sender_has_sent_request = False
#     if not is_self_profile:
#         sender_has_sent_request = ConnectionRequest.objects.filter(
#             sender=request.user,
#             receiver=receiver_profile.user,
#             status='pending'
#         ).exists()

#     context = {
#         'receiver_profile': receiver_profile,
#         'is_self_profile': is_self_profile,
#         'sender_has_sent_request': sender_has_sent_request,
#     }

#     return render(request, 'profile_detail.html', context)

# views.py
# views.py
# views.py
# wedd/views.py

# wedd/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from features.models import ConnectionRequest
from acc.models import CustomUser

# @login_required
# def profile_detail(request, receiver_id):
#     receiver_profile = get_object_or_404(MatrimonialProfile, id=receiver_id)

#     is_self_profile = request.user.email == receiver_profile.email

#     # Check if the sender has already sent connection request
#     sender_has_sent_request = False
#     if not is_self_profile:
#         # Assuming sender_name is passed in the URL parameters
#         sender_name = request.GET.get('sender_name', '')
        
#         try:
#             # Get the sender instance based on the name
#             sender = CustomUser.objects.get(name=sender_name)

#             # Check if the sender has sent a request
#             sender_has_sent_request = ConnectionRequest.objects.filter(
#                 sender=sender,
#                 receiver=receiver_profile.user.matrimonialprofile,
#                 status='pending'
#             ).exists()
#         except CustomUser.DoesNotExist:
#             # Handle the case when the sender is not found
#             # You can redirect to an error page or show an appropriate message
#             return HttpResponse("Sender not found", status=404)

#     context = {
#         'receiver_profile': receiver_profile,
#         'is_self_profile': is_self_profile,
#         'sender_has_sent_request': sender_has_sent_request,
#     }

#     return render(request, 'profile_detail.html', context)






from features.models import Interest, Shortlist, Message
# @login_required
# def dashboard(request):
#     user_profile = MatrimonialProfile.objects.get(email=request.user.email)

#     # Fetch sent and received interests
#     sent_interests = Interest.objects.filter(sender=user_profile)
#     received_interests = Interest.objects.filter(receiver=user_profile)

#     # Fetch shortlisted profiles
#     shortlisted_profiles = Shortlist.objects.filter(user=user_profile)

#     # Fetch chat history
#     sent_messages = Message.objects.filter(sender=user_profile)
#     received_messages = Message.objects.filter(receiver=user_profile)
#     chat_history = sent_messages | received_messages

#     context = {
#         'sent_interests': sent_interests,
#         'received_interests': received_interests,
#         'shortlisted_profiles': shortlisted_profiles,
#         'chat_history': chat_history,
#     }

#     return render(request, 'dashboard.html', context)


# @login_required
# def dashboard(request):
#     user_profile = MatrimonialProfile.objects.get(email=request.user.email)

#     # Fetch received interests
#     received_interests = Interest.objects.filter(receiver=user_profile, is_accepted=None)
#     accepted_interests = Interest.objects.filter(receiver=user_profile, is_accepted=True)

#     # Fetch shortlisted profiles
#     shortlisted_profiles = Shortlist.objects.filter(user=user_profile)

#     # Fetch chat history
#     sent_messages = Message.objects.filter(sender=user_profile)
#     received_messages = Message.objects.filter(receiver=user_profile)
#     chat_history = sent_messages | received_messages

#     context = {
#         'received_interests': received_interests,
#         'accepted_interests': accepted_interests,
#         'shortlisted_profiles': shortlisted_profiles,
#         'chat_history': chat_history,
#     }

#     return render(request, 'dashboard.html', context)

# @login_required
# def accept_reject_interest(request, interest_id, action):
#     interest = Interest.objects.get(pk=interest_id)

#     if action == 'accept':
#         # Perform actions when interest is accepted
#         interest.is_accepted = True
#         interest.save()

#         # Optionally, you can perform other actions here, like enabling chat or phone number visibility
#         # ...

#     elif action == 'reject':
#         # Perform actions when interest is rejected
#         interest.is_accepted = False
#         interest.save()

#     return redirect('dashboard')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from features.models import Interest, Message, MatrimonialProfile

@login_required
def dashboard(request):
    user_profile = MatrimonialProfile.objects.get(email=request.user.email)

    # Fetch received interests
    sent_interests = Interest.objects.filter(sender=user_profile)
    received_interests = Interest.objects.filter(receiver=user_profile, is_accepted=None)
    accepted_interests = Interest.objects.filter(receiver=user_profile, is_accepted=True)

    # Fetch shortlisted profiles
    shortlisted_profiles = Shortlist.objects.filter(user=user_profile)

    # Fetch chat history
    sent_messages = Message.objects.filter(sender=user_profile)
    received_messages = Message.objects.filter(receiver=user_profile)
    chat_history = sent_messages | received_messages
    
    # Fetch phone numbers
    phone_numbers = MatrimonialProfile.objects.filter(id__in=[interest.sender.id for interest in received_interests if interest.is_accepted])
    context = {
        'received_interests': received_interests,
        'accepted_interests': accepted_interests,
        'shortlisted_profiles': shortlisted_profiles,
        'chat_history': chat_history,
        'phone_numbers': phone_numbers,  # Add this line to include phone numbers in the context
    }

    return render(request, 'dashboard.html', context)

@login_required
def accept_reject_interest(request, interest_id, action):
    interest = Interest.objects.get(pk=interest_id)

    if action == 'accept':
        # Perform actions when interest is accepted
        interest.is_accepted = True
        interest.save()

        # Additional actions - enable chat or phone number visibility
        enable_chat_phone_visibility(interest)

    elif action == 'reject':
        # Perform actions when interest is rejected
        interest.is_accepted = False
        interest.save()

    return redirect('dashboard')

# views.py

from features.models import Message  # Import your chat message model

def enable_chat_phone_visibility(interest):
    sender_profile = interest.sender
    receiver_profile = interest.receiver

    # Placeholder for phone visibility logic (replace with your actual logic)
    sender_profile.is_phone_visible = True
    sender_profile.save()

    receiver_profile.is_phone_visible = True
    receiver_profile.save()

    # Create a chat message (replace with your actual logic)
    chat_message = Message.objects.create(
        sender=sender_profile,
        receiver=receiver_profile,
        content=f"Congratulations! You can now chat with {sender_profile.name}."
    )

    # Placeholder for chat visibility logic (replace with your actual logic)
    sender_profile.sent_messages.add(chat_message)
    receiver_profile.received_messages.add(chat_message)


def download_biodata(request, pk):
    profile = get_object_or_404(MatrimonialProfile, pk=pk)

    if profile.biodata:
        # Build the response with the file
        response = HttpResponse(profile.biodata.file, content_type='application/pdf')  # Change the content type based on your file type
        response['Content-Disposition'] = f'attachment; filename="{profile.biodata.name}"'
        return response

    # Handle the case when biodata file is not present
    return HttpResponse("File not found", status=404)

from django.shortcuts import get_object_or_404, redirect
# @login_required
# def send_connection_request(request, receiver_id):
#     receiver = get_object_or_404(MatrimonialProfile, id=receiver_id)

#     # Check if a request already exists
#     existing_request = ConnectionRequest.objects.filter(sender=request.user, receiver=receiver, status='pending').exists()
#     if not existing_request:
#         connection_request = ConnectionRequest.objects.create(sender=request.user, receiver=receiver, status='pending')
#         request.user.matrimonialprofile.connection_requests.add(connection_request)

#     return redirect('profile_detail', receiver_id=receiver_id)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import MatrimonialProfile

# @login_required
# def send_connection_request(request, receiver_id):
#     # Get the receiver's profile
#     # receiver = get_object_or_404(MatrimonialProfile, id=receiver_id)
#     receiver = MatrimonialProfile.objects.exclude(email=request.user.email).get(id=receiver_id)
    

#     # Check if a pending connection request already exists
#     existing_request = ConnectionRequest.objects.filter(
#         sender=request.user.matrimonialprofile,
#         receiver=receiver,
#         status='pending'
#     ).exists()

#     if not existing_request:
#         # Create a new connection request with the sender field set
#         ConnectionRequest.objects.create(
#             sender=request.user.matrimonialprofile,
#             receiver=receiver,
#             status='pending'
#         )

#     # Redirect or add appropriate logic based on your requirements
#     return HttpResponse("Connection request sent successfully")

@login_required
def send_connection_request(request, receiver_id):
    # Get the receiver's profile
    receiver = get_object_or_404(MatrimonialProfile, id=receiver_id)

    # Check if the sender has a MatrimonialProfile
    try:
        # sender_profile = request.user.matrimonialprofile
        sender_profile = MatrimonialProfile.objects.get(email=request.user.email)
    except MatrimonialProfile.DoesNotExist:
        # Handle the case where the sender doesn't have a MatrimonialProfile
        return HttpResponse("Sender profile not found", status=400)

    # Check if a pending connection request already exists
    existing_request = ConnectionRequest.objects.filter(
        sender=sender_profile,
        receiver=receiver,
        status='pending'
    ).exists()

    if not existing_request:
        # Create a new connection request with the sender field set
        ConnectionRequest.objects.create(
            sender=sender_profile,
            receiver=receiver,
            status='pending'
        )

    # Redirect or add appropriate logic based on your requirements
    return HttpResponse("Connection request sent successfully")
    # return redirect('dashboard')
# views.py
@login_required
def handle_connection_request(request, request_id, action):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user, status='pending')

    if action == 'accept':
        connection_request.status = 'accepted'
        connection_request.save()

        # Additional actions - enable chat or phone number visibility
        enable_chat_phone_no_visibility(connection_request.sender, connection_request.receiver)

    elif action == 'reject':
        connection_request.status = 'rejected'
        connection_request.save()

    return redirect('profile_detail', receiver_id=request.user.id)

def check_connection_acceptance(sender_profile, receiver_profile):
    
    connection_request = ConnectionRequest.objects.filter(
        sender=sender_profile,
        receiver=receiver_profile,
        status='accepted'
    ).exists()

    return connection_request
