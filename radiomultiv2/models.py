from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


# Create your models here.

class CareCode(models.Model):
    verbose_name = _('care code')
    verbose_name_plural = _('care codes')
    code = models.CharField(_('code'), max_length=30)
    name = models.CharField(_('name'), max_length=50)
    description = models.TextField(_('description'), max_length=100)
    applicable_from = models.DateField(_('applicable from'), help_text=_('price applies from date'))
    applicable_to = models.DateField(_('applicable to'), help_text=_('price applies to date'))
    # prix net = 88% du montant brut
    # prix brut
    gross_amount = models.DecimalField(_('gross amount'), max_digits=5, decimal_places=2)
    reimbursed = models.BooleanField(_('reimbursed'), help_text=_('care can be reimbursed by NHS'), default=True)

    # previous_gross_amount = models.DecimalField("Ancien montant brut", max_digits=5, decimal_places=2)
    # price_switch_date = models.DateField( help_text=u"Date d'accident est facultatif", null=True, blank=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s: %s' % (self.code, self.name)



class Service(models.Model):
    #patient = models.ForeignKey(Patient)
    carecode = models.ForeignKey(CareCode)
    date = models.DateTimeField(_('service date'))
    date.editable = True

    #     formfield_overrides = {
    #         models.DateTimeField: {'widget': MyAdminSplitDateTime},
    #     }
    @property
    def net_amount(self):
        "Returns the net amount"
        # normalized_price_switch_date = pytz_chicago.normalize( self.carecode.price_switch_date )
        # if self.date > normalized_price_switch_date:
        # round to only two decimals
        #   return round(((self.carecode.gross_amount * 88) / 100), 2)
        # round to only two decimals
        # return round(((self.carecode.previous_gross_amount * 88) / 100), 2)
        if self.carecode.reimbursed:
            return round(((self.carecode.gross_amount * 88) / 100), 2) + self.fin_part
        else:
            return self.carecode.gross_amount


class Practian(models.Model):
    code_ns = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    address = models.TextField(max_length=30)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_(
        "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex],max_length=20,blank=True)


class MedicalPresciption(models.Model):
    scan = models.ImageField(upload_to='scans')
    practician = models.ForeignKey(Practian)
    startDate = models.DateField(_('start date prescription'))
    endDate = models.DateField(_('end date prescription'))


class Patient(models.Model):
    code_sn = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    address = models.TextField(max_length=30)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_(
        "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    email_address = models.EmailField(default=None, blank=True, null=True)


class JobPosition(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100, blank=True,
                                   null=True)

    def __str__(self):  # Python 3: def __str__(self):
        return '%s' % (self.name.strip())


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_contract = models.DateField('start date')
    end_contract = models.DateField('end date', blank=True,
                                    null=True)
    occupation = models.ForeignKey(JobPosition)
    def __str__(self):  # Python 3: def __str__(self):
        return '%s' % (self.user.username.strip())

