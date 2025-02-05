from django.shortcuts import render, get_object_or_404
from social.models import ChatMessage, VoiceNote, Pdf, Document
from userauths.models import Profile
from django.contrib.auth.decorators import login_required

# views for chating and mesaging feature.
@login_required
def chat_view(request, profile_id):
    '''View to handle chat messages with voice notes, PDFs, and documents.'''

    # Get sender's profile (current user)
    sender_profile = get_object_or_404(Profile, id=profile_id, user=request.user)

    # Get receiver's profile
    receiver_profile = get_object_or_404(Profile, id=profile_id, user=request.user)

    # Fetch all chat content (messages, voice notes, PDFs, documents)
    messages = ChatMessage.objects.filter(sender=sender_profile, receiver=receiver_profile) | \
               ChatMessage.objects.filter(sender=receiver_profile, receiver=sender_profile)

    voice_notes = VoiceNote.objects.filter(sender=sender_profile, receiver=receiver_profile) | \
                  VoiceNote.objects.filter(sender=receiver_profile, receiver=sender_profile)

    pdfs = Pdf.objects.filter(sender=sender_profile, receiver=receiver_profile) | \
           Pdf.objects.filter(sender=receiver_profile, receiver=sender_profile)

    documents = Document.objects.filter(sender=sender_profile, receiver=receiver_profile) | \
                Document.objects.filter(sender=receiver_profile, receiver=sender_profile)

    # Combine all messages and sort them by timestamp
    chat_history = sorted(
        list(messages) + list(voice_notes) + list(pdfs) + list(documents),
        key=lambda x: x.timestamp
    )

    context= {
        "chat_history": chat_history,
        "sender_profile": sender_profile,
        "receiver_profile": receiver_profile,
    }

    return render(request, "social/chat.html", context)


