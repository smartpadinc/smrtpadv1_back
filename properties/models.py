from django.db import models
from django.contrib.auth.models import User
from user import models as usermod
from django.conf import settings


class UnitProperty(models.Model):
    unitproperty        = models.AutoField(primary_key=True)
    user                = models.ForeignKey(User,related_name="property_owner", help_text="owner of the property")
    property_code       = models.CharField(max_length=30, help_text="Unique property code", unique=True)
    property_name       = models.CharField(max_length=50, help_text="Property name")
    property_type       = models.CharField(max_length=3, db_index=True, default="1", choices=settings.OPT_PROPERTY_TYPE)
    description         = models.TextField(null=True, blank=True, help_text="organization description")
    address_line_1      = models.CharField(max_length=50, null=True, blank=True, help_text="address line 1")
    address_line_2      = models.CharField(max_length=50, null=True, blank=True, help_text="address line 2")
    city                = models.CharField(max_length=50, null=True, blank=True, help_text="City")
    state               = models.CharField(max_length=50, null=True, blank=True, help_text="State or Province")
    country             = models.CharField(max_length=3, db_index=True, default="ph", choices=settings.OPT_COUNTRY)
    zip_code            = models.CharField(max_length=10, null=True, blank=True, help_text="Zip Code")
    status              = models.CharField(max_length=1, db_index=True, default="A", choices=settings.OPT_STATUS, help_text="Active / Inactive / Deleted")
    date_created        = models.DateTimeField(auto_now=False, auto_now_add=True, help_text="Date the record was created")
    last_modified_by    = models.ForeignKey(User,related_name="unitproperty_last_updated", null=True, blank=True, help_text="User who last updated the unitproperty")
    last_modified       = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, help_text="Date the record was last edited.")
