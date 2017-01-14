from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from user import models as usermod


class UnitProperty(models.Model):
    unitproperty        = models.AutoField(primary_key=True)
    organization        = models.ForeignKey(usermod.Organization, related_name="organization_property", blank=True, null=True, help_text="Organization where property belongs to. Can be blank.")
    user                = models.ForeignKey(User,related_name="property_owner", help_text="Owner of this property.")
    property_code       = models.CharField(max_length=30, help_text="System-generated unique code", unique=True)
    property_name       = models.CharField(max_length=50, help_text="Property name")
    property_type       = models.CharField(max_length=3, db_index=True, default="1", choices=settings.OPT_PROPERTY_TYPE)
    url_slug            = models.CharField(max_length=50, null=True, blank=True, help_text="Url slug")
    search_tags         = models.TextField(null=True, blank=True, help_text="Comma-separated, search tags, for search and seo")
    description         = models.TextField(null=True, blank=True, help_text="Property Description")
    address_line_1      = models.CharField(max_length=50, null=True, blank=True, help_text="address line 1")
    address_line_2      = models.CharField(max_length=50, null=True, blank=True, help_text="address line 2")
    city                = models.CharField(max_length=50, null=True, blank=True, help_text="City")
    state               = models.CharField(max_length=50, null=True, blank=True, help_text="State or Province")
    country             = models.CharField(max_length=3, db_index=True, default="ph", choices=settings.OPT_COUNTRY)
    zip_code            = models.CharField(max_length=10, null=True, blank=True, help_text="Zip Code")
    gmaps_url           = models.TextField(null=True, blank=True, help_text="Google maps url")
    recurring_payment   = models.DecimalField(max_digits=10, decimal_places=3, help_text="Payment", default="0")
    payment_type        = models.CharField(max_length=1, db_index=True, choices=settings.OPT_PAYMENT_TYPE, default="1")
    rent_status         = models.CharField(max_length=1, db_index=True, default="1", choices=settings.OPT_RENT_STATUS, help_text="Open / Rented / Available Soon")
    status              = models.CharField(max_length=1, db_index=True, default="A", choices=settings.OPT_STATUS, help_text="Active / Inactive / Deleted")
    date_created        = models.DateTimeField(auto_now=False, auto_now_add=True, help_text="Date the record was created")
    last_modified_by    = models.ForeignKey(User,related_name="unitproperty_last_updated", null=True, blank=True, help_text="User who last updated the unitproperty")
    last_modified       = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="Date the record was last edited.")
