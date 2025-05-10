from django.db import models

class CV(models.Model):
    file = models.FileField(upload_to='cvs/')
    id = models.BigAutoField(primary_key=True)  # Specify BigAutoField if necessary
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name or f"CV #{self.id}"

