__version__ = "1.0.0"

"""
UOSE Models Admin:
This script contains the Admin configuration for the UOSE models.

Version History:
- 1.0.0 (2022-01-01): Initial version of the models.
- 1.1.0 (2022-02-01): Added additional fields to the models.
- 1.2.0 (2022-03-01): Refactored the models for improved performance.

Change Log:
- 2022-01-01: Created the models.py file.
- 2022-02-01: Updated the models to include new fields.
- 2022-03-01: Optimized the models for better performance.
"""

from django.contrib import admin

from .models import (
    EntityType,
    Entity,
    EntityDocument,
    EntityDocumentMeta,
    Country,
    ProvinceState,
    Client,
    UserInboxMessageType,
)

# Entity Data Models
admin.site.register(EntityType)
admin.site.register(Entity)
admin.site.register(EntityDocument)
admin.site.register(EntityDocumentMeta)
admin.site.register(Country)
admin.site.register(ProvinceState)
admin.site.register(Client)
admin.site.register(UserInboxMessageType)
