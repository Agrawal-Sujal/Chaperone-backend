from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Model

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        # Set default flags for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    recent_otp = models.IntegerField(blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    is_walker = models.BooleanField(blank=True, null=True)
    date_of_birth = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default = False)
    is_profile_completed = models.BooleanField(default = False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    photo_url = models.TextField(blank=True, null=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


# Walker & Wanderer

class Walker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length = 100,null = True,blank = True)
    photo_url = models.TextField(blank=True, null=True)
    about_yourself = models.TextField(blank=True, null=True)
    total_rating = models.IntegerField(null=True, blank=True, default=0)
    total_wanderer = models.IntegerField(null = True, blank = True, default = 0)
    is_free_plan = models.BooleanField(default=True)
    expiry_date = models.DateField(null=True, blank = True)
    latitude = models.FloatField(null = True, blank = True)
    longitude = models.FloatField(null = True, blank = True)
    location_name = models.TextField(null = True,blank = True)
    is_active = models.BooleanField(default= False)
    max_walk_distance = models.FloatField(null = True, blank = True,default= 1.00)
    male = models.BooleanField(null=True, blank= True)
    total_walks = models.IntegerField(default = 0)
    total_earning = models.FloatField(default=0.0)

    def __str__(self):
        return f"Walker: {self.user.email}"


class Wanderer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length = 100, null = True, blank = True)
    photo_url = models.TextField(blank=True, null=True)
    total_rating = models.IntegerField(null=True, blank=True, default = 0)
    total_walker = models.IntegerField(null = True, blank = True, default = 0)
    total_walks = models.IntegerField(default = 0)
    total_charity = models.FloatField(default=0.0)

    def __str__(self):
        return f"Wanderer: {self.user.email}"


# Preferences

class WandererPreferences(models.Model):
    wanderer = models.OneToOneField(Wanderer, on_delete=models.CASCADE, primary_key=True)
    need_mobility_assistance = models.BooleanField(default=False)
    male = models.BooleanField(default=False)
    female = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferences for {self.wanderer.user.email}"


# Support Tables

class Charity(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class WalkingPace(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Many-to-Many Relationships

class WalkerLanguage(models.Model):
    walker = models.ForeignKey(Walker, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('walker', 'language')


class WandererPreferenceWalkingPace(models.Model):
    wanderer = models.ForeignKey(WandererPreferences, on_delete=models.CASCADE)
    walking_pace = models.ForeignKey(WalkingPace, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('wanderer', 'walking_pace')


class WandererPreferenceLanguage(models.Model):
    wanderer = models.ForeignKey(WandererPreferences, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('wanderer', 'language')


class WalkerWalkingPace(models.Model):
    walker = models.ForeignKey(Walker, on_delete=models.CASCADE)
    walking_pace = models.ForeignKey(WalkingPace, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('walker', 'walking_pace')


class WandererPreferenceCharity(models.Model):
    wanderer = models.ForeignKey(WandererPreferences, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('wanderer', 'charity')
