from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, second_name, index, si_number, password=None):
        if not email: 
            raise ValueError("Email je vyžadovaný")
        if not username:
            raise ValueError("Přihlašovací jméno je vyžadováno")
        if not first_name:
            raise ValueError("Jméno je vyžadováno")
        if not second_name:
            raise ValueError("Příjmení je vyžadováno")
        if not index:
            raise ValueError("INDEX je vyžadován. Tvar např. GBM9058")
        if not si_number:
            raise ValueError("Číslo čipu musí být vyplněno. Např. 2042535")
        
        user = self.model (
            email=self.normalize_email(email),
            username=username,
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, first_name, second_name, index, si_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            second_name=second_name,
            index=index,
            si_number=si_number,
                              
            )
        user.is_admin = True
        user.is_staff = True
        user.is_repre = True
        user.is_zdr = True
        user.is_seftrener = True
        user.is_veteran = True
        user.is_sekretar = True
        user.is_predseda = True
        user.is_organizator = True
        user.is_clen = True
        user.is_registrovany = True
        user.is_neregistrovany = True 
        user.save(using=self._db)   
        return user

class Account(AbstractBaseUser):
    email               = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    username            = models.CharField(verbose_name="Uživatelské jméno", max_length=30, unique=True)       
    date_joined         = models.DateTimeField(verbose_name='Vytvoření', auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name='Poslední přihlášení', auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False) #oprávnění pro vstup do administrace
    is_sekretar         = models.BooleanField(default=False)
    is_seftrener        = models.BooleanField(default=False)
    is_veteran          = models.BooleanField(default=False)
    is_repre            = models.BooleanField(default=False)
    is_zdr              = models.BooleanField(default=False)
    is_predseda         = models.BooleanField(default=False)
    is_organizator      = models.BooleanField(default=False)
    is_clen             = models.BooleanField(default=False)
    is_registrovany     = models.BooleanField(default=True)
    is_neregistrovany   = models.BooleanField(default=False)
    first_name          = models.CharField(verbose_name='Jméno', max_length=30,)
    second_name         = models.CharField(verbose_name='Příjmení', max_length=30,)
    index               = models.CharField(verbose_name='Index', max_length=7, unique=True, null=True, blank=True)
    si_number           = models.IntegerField(verbose_name='Číslo čipu', validators=[MaxValueValidator(8999999),MinValueValidator(1000)], unique=True, null=True, blank=True)
    club                = models.CharField(max_length=3, blank=True)
    age                 = models.IntegerField(default=0)
    sex                 = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'second_name', 'index', 'si_number']

    objects = MyAccountManager()
    
    def save(self, *args, **kwargs):

        if len(self.index) != 7:
            raise ValueError("Index musí mít přesně 7 symbolů")
        
        if not self.club:
            self.club = self.index[:3].upper()

        birth_year = int(self.index[3:5])
        current_year = date.today().year % 100

        if 0 <= birth_year <= current_year:
            self.age = current_year - birth_year
        else:
            self.age = (100 - birth_year + current_year) % 100

        sex_code = int(self.index[5:7])
        self.sex = 'F' if sex_code >= 50 else 'M'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email + ", " + self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True