from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, gender, profile_picture=None, password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not full_name:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.full_name = full_name
        user.set_password(password)  # change password to hash
        # user.profile_picture = profile_picture
        user.gender = gender
        user.admin = is_admin
        user.profile_picture = profile_picture
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name, gender, password=None):
        user = self.create_user(
            email,
            full_name,
            gender,
            profile_picture=None,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, full_name, gender, password=None):
        user = self.create_user(
            email,
            full_name,
            gender,
            profile_picture=None,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser, SimpleEmailConfirmationUserMixin):
    username = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True,)
    profile_picture = models.ImageField(upload_to='user_data/profile_picture', null=True, blank=True)
    gender = models.CharField(max_length=255, blank=True, default='rather_not_say')
    birth_date = models.DateField(default='1999-09-09', blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'gender']  # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    @staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        # "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        # "Is the user active?"
        return self.active


"""
class Extender(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # extend other data fields

"""


class CreatedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=128)
    event_date_time = models.DateTimeField()
    address = models.CharField(max_length=510)

    def __str__(self):
        # return '%s %s %s'%(self.event_name, self.event_date_time, self.address)
        return '{} {} {} {}'.format(self.user, self.event_name, self.event_date_time, self.address)

    """
    @staticmethod
    def delete_event(uid, eid):
        event = CreatedEvent.objects.get(user_id=uid, id=eid)
        event.delete()
        if event is None:
            return True
        else:
            return False
    """
