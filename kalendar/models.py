from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver





def upload_location(instance,filename, **kwargs):
    file_path = 'kalendar/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), event_date=str(instance.event_date), title=str(instance.title), filename=filename
        )
    return file_path


class BlogPost(models.Model):
    event_type = (
        ('trenink', 'Trénink'),
        ('tc-oddil', 'Oddílové soustředění'),
        ('3st', 'Soutěž III. stupně'),
        ('2st', 'Soutěž II. stupně'), 
        ('ostatni', 'Ostatní'),             
        ('mcr-nz', 'MČR/NŽ - I. stupeň'),
        ('repre', 'Reprezentační akce'),
        ('zdr', 'ŽDR akce'),
    )
    title           = models.CharField(max_length=60, null=False, blank=False)
    zprava_info     = models.CharField(max_length=500, null=False, blank=True,)
    zprava_warning  = models.CharField(max_length=500, null=False, blank=True,)
    mapa            = models.ImageField(upload_to=upload_location, null=False, blank=True)
    bulletin        = models.FileField(upload_to=upload_location, null=False, blank=True)
    pokyny          = models.FileField(upload_to=upload_location, null=False, blank=True)
    startlist       = models.FileField(upload_to=upload_location, null=False, blank=True)
    results         = models.FileField(upload_to=upload_location, null=False, blank=True)
    splittimes      = models.FileField(upload_to=upload_location, null=False, blank=True)
    event_date      = models.DateField(null=False, blank=False)
    event_date_end  = models.DateField(null=True, blank=True)
    termin_prihl    = models.DateTimeField(null=False)
    event_type      = models.CharField(max_length=30, choices=event_type, blank=False)
    date_published  = models.DateTimeField(auto_now_add=True, verbose_name="Datum publikace")
    date_updated    = models.DateTimeField(auto_now=True, verbose_name="Datum aktualizace")
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug            = models.SlugField(blank=True, unique=True)
    club            = models.CharField(max_length=3, blank=True)
    start00         = models.DateTimeField(null=True, blank=True)
    discipline      = models.CharField(max_length=40, null=False, blank=True,)
    gps             = models.CharField(max_length=40, null=False, blank=True,)
    contact         = models.CharField(max_length=50, null=False, blank=True,)



    def __str__(self):
        return self.title
# null = True - znamená, že hodnota v tabulce musí vždy být, False, že může zůstat prázdné
#blank = True může být prázdné, False - pole je required

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance,**kwargs):
    instance.mapa.delete(False)

def pre_save_blog_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.event_date.strftime("%d-%m-%Y") + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiever, sender=BlogPost)

class EventEntry(models.Model):

    category = (
        ('mdr', 'MDR'),
        ('m12', 'M12'),
        ('m14', 'M14'),
        ('m16', 'M16'),
        ('m19', 'M19'),
        ('m20', 'M20'),
        ('m40', 'M40'),
        ('m50', 'M50'),
        ('m60', 'M60'),
        ('m70', 'M70'),
        ('d12', 'D12'),
        ('d14', 'D14'),
        ('d16', 'D16'),
        ('d19', 'D19'),
        ('d20', 'D20'),
        ('d35', 'D35'),
        ('d45', 'D45'),
        ('d55', 'D55'),
        ('d65', 'D65'),
    )

    event           = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    first_name      = models.CharField(max_length=30)
    second_name     = models.CharField(max_length=30)
    index           = models.CharField(max_length=7)
    si_number       = models.IntegerField()
    category        = models.CharField(max_length=5, choices=category, blank=False, default='m20')
    note            = models.CharField(max_length=80, blank=True)

    timestamp       = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.index} {self.si_number} {self.category} {self.note} - {self.event.title}"
    
class MicroEvent(models.Model):
    main_event = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    notice = models.CharField(max_length=80, blank=True)
    max_entries = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"MicroEvent for {self.main_event.title}"
    
class MicroEventEntry(models.Model):
    name = models.CharField(max_length=50, blank=True)  # User's name
    notice_name = models.CharField(max_length=80, blank=True)
    microevent = models.ForeignKey(MicroEvent, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    #class Meta:
     #   unique_together = ['name']  # Ensure a user can only enter a microevent once