from django.db import models
from django.contrib.auth.models import User


OPT_COUNTRY = (
    ('ph', 'Philippines'),
    ('sg', 'Singapore'),
)

OPT_VALID_IDS = {
    ('0', 'none'),
    ('1', 'SSS'),
    ('2', 'Passport'),
    ('3', "Driver's License"),
}

OPT_USER_TYPE = (
    ('1', 'TENANT'),
    ('2', 'OWNER'),
)

class UserProfile(models.Model):
    userprofile         = models.AutoField(primary_key=True)
    user                = models.OneToOneField(User,related_name="user_profile", help_text="user_id", unique=True)
    user_type           = models.CharField(max_length=3, db_index=True, default="1",  choices=OPT_USER_TYPE)
    first_name          = models.CharField(max_length=30, help_text="Firstname")
    middle_name         = models.CharField(max_length=5, null=True, blank=True, help_text="middle name")
    last_name           = models.CharField(max_length=30, help_text="lastname")
    birthdate           = models.CharField(max_length=10, help_text="yyyy-mm-dd", null=True, blank=True)
    mobile_no           = models.CharField(max_length=20, help_text="lastname", null=True, blank=True)
    address             = models.CharField(max_length=100, null=True, blank=True, help_text="address")
    city                = models.CharField(max_length=50, null=True, blank=True, help_text="City")
    state               = models.CharField(max_length=50, null=True, blank=True, help_text="State")
    country             = models.CharField(max_length=3, db_index=True, default="ph", choices=OPT_COUNTRY)
    zip_code            = models.CharField(max_length=10, null=True, blank=True, help_text="Zip Code")
    identification_type = models.CharField(max_length=3, db_index=True, default="0",  choices=OPT_VALID_IDS)
    identification_no   = models.CharField(max_length=50, null=True, blank=True, help_text="e.g SSS / Driver's License / Passport")
    img_url             = models.CharField(max_length=20, null=True, blank=True, help_text="image filename")
    fb_url              = models.CharField(max_length=50, null=True, blank=True, help_text="facebook profile")
    date_created        = models.DateTimeField(auto_now=False, auto_now_add=True, help_text="Date the record was created")
    last_modified_by    = models.ForeignKey(User,related_name="user_profile_last_updated", null=True, blank=True, help_text="User who last updated the profile")
    last_modified       = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, help_text="Date the record was last edited.")
