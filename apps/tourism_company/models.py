from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class TourismCompany(models.Model):
    
#     company_id = models.AutoField(primary_key=True)
#     user_name = models.CharField(max_length=100)
#     user_phone = models.CharField(max_length=20)
#     user_email = models.EmailField(max_length=55)
#     company_name = models.CharField(max_length=255)
#     company_phone = models.CharField(max_length=255)
#     company_address = models.CharField(max_length=255)

#     def __str__(self):
#         return self.company_name



class TourismCompanyManager(BaseUserManager):
    def create_user(self, user_name, user_phone, user_email, company_name, company_phone, company_address):
        if not user_email:
            raise ValueError("Users must have an email address")
        user = self.model(
            user_name=user_name,
            user_phone=user_phone,
            user_email=self.normalize_email(user_email),
            company_name=company_name,
            company_phone=company_phone,
            company_address=company_address
        )
        # user.set_password(password)
        user.save(using=self._db)
        return user

class TourismCompany(models.Model):
    company_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=20)
    user_email = models.EmailField(max_length=55, unique=True)
    company_name = models.CharField(max_length=255, unique=True)
    company_phone = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)


    def __str__(self):
        return self.company_name



