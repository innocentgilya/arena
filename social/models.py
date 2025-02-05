from django.db import models
from django.conf import settings
from userauths.models import Profile 
from django.core.exceptions import ValidationError
from PIL import Image as PilImage
import io

# my chat models ... # my chat models ... # my chat models ...# my chat models ...
# my chat models ...# my chat models ... # my chat models ... # my chat models ...
class ChatMessage(models.Model):
    '''a model that holds a chatMessage'''
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name}: {self.message[:50]}"

class VoiceNote(models.Model):
    '''model that holds a voice note message '''
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_voice_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_voice_messages')
    voicemessage = models.FileField(upload_to='voicenotes/')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.voicemessage
    
class Document(models.Model):
    '''this holds a specific document message when chatting'''
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_document_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_document_messages')    
    document = models.FileField(upload_to='document_messages/')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.document)
    
    def clean(self):
        super().clean()
        # Check file size
        if self.document.size > 25 * 1024 * 1024:  # 10 MB
            raise ValidationError("File size must be under 25 MB")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Pdf(models.Model):
    '''this holds a specific pdfs message when chatting'''
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_pdf_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_pdf_messages')    
    pdf = models.FileField(upload_to='pdf_messages/')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pdf)
    
    def clean(self):
        super().clean()
        # Check file size
        if self.document.size > 10 * 1024 * 1024:  # 10 MB
            raise ValidationError("File size must be under 10 MB")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Image(models.Model):
    '''this holds the images sent or received during messaging process'''
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_image_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_image_messages')    
    image = models.ImageField(upload_to='image_messages/')
    timestamp = models.DateField(auto_now_add=True)   

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        # Reduce image size before saving
        img = PilImage.open(self.image)
        if img.mode in ("RGBA", "P"): 
            img = img.convert("RGB")
        
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        
        self.image = models.ImageFile(output, self.image.name)
        self.clean()
        super().save(*args, **kwargs)

    