from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Warehouse(models.Model):
    loan_num = models.CharField(max_length=16)
    funded_dt = models.DateField(auto_now=False, blank=True, null=True)
    borrower_nm = models.CharField(max_length=64)
    loan_amt = models.IntegerField(blank=True, null=True)
    advance_amt = models.IntegerField(blank=True, null=True)
    warehouse_bank = models.CharField(max_length=64)
    investor_nm = models.CharField(max_length=64)
    commitment_type = models.CharField(max_length=36)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    slug = models.SlugField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    submitted = models.BooleanField(verbose_name='Submitted', default=False)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         slg = timezone.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
    #         self.slug = slugify(slg)
    #     super(Warehouse,self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

def warehouse_model_pre_save_receiver(sender, instance, *args, **kwargs):
    # print("before save")
    # print(dir(settings.AUTH_USER_MODEL))
    # print()
    pass

def warehouse_model_post_save_receiver(sender, instance, *args, **kwargs):
    # print("after save")
    pass

pre_save.connect(warehouse_model_pre_save_receiver, sender=Warehouse)
post_save.connect(warehouse_model_post_save_receiver, sender=Warehouse)