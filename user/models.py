from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class UserProfile(models.Model):
    userprofile         = models.AutoField(primary_key=True, editable=False)
    user                = models.OneToOneField(User,related_name="user_profile", help_text="user_id", unique=True, default="0000000")
    user_type           = models.CharField(max_length=3, db_index=True, default="1",  choices=settings.OPT_USER_TYPE)
    first_name          = models.CharField(max_length=30, help_text="Firstname")
    middle_name         = models.CharField(max_length=30, null=True, blank=True, help_text="middle name")
    last_name           = models.CharField(max_length=30, help_text="lastname")
    birthdate           = models.CharField(max_length=10, help_text="yyyy-mm-dd", null=True, blank=True)
    mobile_no           = models.CharField(max_length=20, help_text="lastname", null=True, blank=True)
    address_line_1      = models.CharField(max_length=50, null=True, blank=True, help_text="address line 1")
    address_line_2      = models.CharField(max_length=50, null=True, blank=True, help_text="address line 2")
    address_line_3      = models.CharField(max_length=50, null=True, blank=True, help_text="address line 3")
    city                = models.CharField(max_length=50, null=True, blank=True, help_text="City")
    state               = models.CharField(max_length=50, null=True, blank=True, help_text="State or Province")
    country             = models.CharField(max_length=3, db_index=True, default="ph", choices=settings.OPT_COUNTRY)
    zip_code            = models.CharField(max_length=10, null=True, blank=True, help_text="Zip Code")
    identification_type = models.CharField(max_length=3, db_index=True, default="0",  choices=settings.OPT_VALID_IDS)
    identification_no   = models.CharField(max_length=50, null=True, blank=True, help_text="e.g SSS / Driver's License / Passport")
    img_url             = models.CharField(max_length=20, null=True, blank=True, help_text="image filename")
    fb_url              = models.CharField(max_length=50, null=True, blank=True, help_text="facebook profile")
    date_created        = models.DateTimeField(auto_now=False, auto_now_add=True, help_text="Date the record was created", default="2017-01-13 17:19:14.230316+00")
    last_modified_by    = models.ForeignKey(User,related_name="user_profile_last_updated", null=True, blank=True, help_text="User who last updated the profile")
    last_modified       = models.DateTimeField(auto_now=True, help_text="Date the record was last edited.", default="2017-01-13 17:19:14.230316+00")

class Organization(models.Model):
    organization        = models.AutoField(primary_key=True)
    user                = models.ForeignKey(User,related_name="organization_owner", help_text="owner of the organization")
    organization_name   = models.CharField(max_length=30, help_text="Organization name")
    description         = models.TextField(null=True, blank=True, help_text="organization description")
    address_line_1      = models.CharField(max_length=50, null=True, blank=True, help_text="Business address line 1")
    address_line_2      = models.CharField(max_length=50, null=True, blank=True, help_text="Business address line 2")
    address_line_3      = models.CharField(max_length=50, null=True, blank=True, help_text="Business address line 3")
    city                = models.CharField(max_length=50, null=True, blank=True, help_text="City")
    state               = models.CharField(max_length=50, null=True, blank=True, help_text="State or Province")
    country             = models.CharField(max_length=3, db_index=True, default="ph", choices=settings.OPT_COUNTRY)
    zip_code            = models.CharField(max_length=10, null=True, blank=True, help_text="Zip Code")
    logo_image          = models.CharField(max_length=20, null=True, blank=True, help_text="Organization Logo")
    website_url         = models.CharField(max_length=20, null=True, blank=True, help_text="organization website url")
    status              = models.CharField(max_length=1, db_index=True, default="A", choices=settings.OPT_STATUS, help_text="Active / Inactive / Deleted")
    date_created        = models.DateTimeField(auto_now=False, auto_now_add=True, help_text="Date the record was created", default="2017-01-13 17:19:14.230316+00")
    last_modified_by    = models.ForeignKey(User,related_name="organization_last_updated", null=True, blank=True, help_text="User who last updated the organization")
    last_modified       = models.DateTimeField(auto_now=True, help_text="Date the record was last edited.", default="2017-01-13 17:19:14.230316+00")
