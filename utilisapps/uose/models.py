"""
UOSE Models:
This script contains the models for the UOSE application in the UtilisWeb project.

Version History:
- 1.0.0 (2022-01-01): Initial version of the models.
- 1.1.0 (2022-02-01): Added additional fields to the models.
- 1.2.0 (2022-03-01): Refactored the models for improved performance.

Change Log:
- 2022-01-01: Created the models.py file.
- 2022-02-01: Updated the models to include new fields.
- 2022-03-01: Optimized the models for better performance.
"""

import os
import pathlib
import pandas as pd

from django.utils import timezone

from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.auth.models import User


class EntityType(models.Model):
    """Entity Types;  Classification of Entity Types

    Args:
        models (models.Model): Django Based Model Class

    Returns:
        models.Model: Django Based Model Class
    """

    entity_type = models.CharField(max_length=4, unique=True, primary_key=True)
    entity_type_description = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.entity_type} | {self.entity_type_description}"


class Country(models.Model):
    """Country:  Represents a country in the world.

    Args:
        models (models.Model): Django Based Model Class

    Returns:
        models.Model: Django Based Model Class
    """

    country = models.CharField(max_length=4, unique=True)
    country_name = models.CharField(max_length=250)
    country_iso_code = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.country} | {self.country_name} | {self.country_iso_code}"


class ProvinceState(models.Model):
    """ProvinceState:  Represents a province or state in a country.

    Args:
        models (models.Model): Django Based Model Class

    Returns:
        models.Model: Django Based Model Class
    """

    province_state = models.CharField(max_length=4, unique=True, primary_key=True)
    province_state_name = models.CharField(max_length=250)
    province_state_iso_code = models.CharField(max_length=4)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.province_state} | {self.province_state_name} | {self.province_state_iso_code} | {self.country}"


class Entity(models.Model):
    """Entity:  Reprents various entities, like regulators, utilites,
    companies, etc....

    Args:
        models (models.Model): Django Based Model Class

    Returns:
        models.Model: Django Based Model Class
    """

    entity = models.CharField(max_length=4, unique=True, primary_key=True)
    entity_name = models.CharField(max_length=250)
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE)
    entity_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    entity_province_state = models.ForeignKey(ProvinceState, on_delete=models.CASCADE)
    entity_link = models.URLField()  # link to the entity site

    def __str__(self):
        return f"{self.entity} | {self.entity_name} | {self.entity_type}"


class EntityDocument(models.Model):
    """Entity Documents Model:  Represents regulated   the documents associated with an entity.

    Args:
        models (models.Model): Django Based Model Class
    """

    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="entity_ref"
    )
    link = models.URLField()  # link to the entity site
    case_number = models.CharField(
        max_length=100
    )  # docket or case number of the document
    filename_description = models.CharField(
        max_length=250
    )  # description of the documents
    file_url = models.URLField()
    document_type = models.CharField(max_length=100)
    issued_by_entity_date = (
        models.DateField()
    )  # Date the document was issued by the entity
    received_by_entity_date = (
        models.DateField()
    )  # Date the document was received by the entity
    submitter = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="submitter"
    )  # submitter of the document
    applicant = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="applicant"
    )  # applicant for the document
    status = models.CharField(max_length=100)


class UserEntityDocuments(models.Model):
    """
    Represents the relationship between a user and an entity document.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_id = models.ForeignKey(EntityDocument, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}.{self.document_id}"


class UserNotesEntityDocuments(models.Model):
    """
    Tracks notes that a user had made on a document
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_id = models.ForeignKey(EntityDocument, on_delete=models.CASCADE)
    private_note = models.BooleanField(default=False)
    page_number = models.IntegerField()
    text_reference = models.TextField()
    note_text = models.TextField()
    note_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.user}.{self.document_id}"


class EntityDocumentMeta(models.Model):
    """Descriptive information about the linked entity document.  Contains any
    type of information related to type, number of pages, content size,
    etc.....

    Anything that can be used to described the information about the document

    Args:
        models (models.Model): Django Based Model Class

    Returns:
        models.Model: Django Based Model Class
    """

    doc_id = models.ForeignKey(
        EntityDocument, on_delete=models.CASCADE, unique=True, primary_key=True
    )
    new_doc_indicator = models.BooleanField(default=True)
    content_type = models.CharField(max_length=100)
    content_size = models.IntegerField()
    num_pages = models.IntegerField()
    is_loaded_to_analytics = models.BooleanField(default=False)
    analytics_scrape_date = models.DateField()
    record_insert_date = models.DateField()

    def __str__(self):
        return f"{self.id} | {self.new_doc_indicator} | {self.content_type} | {self.is_loaded_to_analytics}"


class RDSTextModel(models.Model):
    url = models.URLField()
    page_number = models.IntegerField()
    page_text = models.TextField()
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self):
        return f"{self.url} | Page {self.page_number}"


class RegulatorApplicaations(models.Model):
    """Regulator Applications:  Represents the applications to the regulator
    for various things like rate changes, new services, etc....

    Args:
        models (models.Model): Django Based Model Class

    Returns:
        models.Model: Django Based Model Class
    """

    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="entity_detail"
    )
    case_number = models.CharField(
        max_length=100
    )  # docket or case number of the document
    applicant = models.CharField(max_length=100, default="N/A")
    market_type = models.CharField(max_length=100, default="N/A")
    appl_category = models.CharField(max_length=100, default="N/A")
    application_start_date = models.DateField()
    appl_description = models.CharField(
        max_length=250
    )  # description of the application

    def __str__(self) -> str:
        return f"{self.id} | {self.entity} | {self.case_number} | {self.applicant} | {self.application_start_date}"


class UserRegulatorApplicaations(models.Model):
    """
    Represents the relationship between a user and an entity document.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applicant_id = models.ForeignKey(RegulatorApplicaations, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}.{self.applicant_id}"


class UserInboxMessageType(models.Model):
    message_type = models.CharField(max_length=4, unique=True, primary_key=True)
    message_type_description = models.CharField(max_length=250)


class UserInbox(models.Model):
    id = models.AutoField(primary_key=True)
    sending_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sending_user"
    )
    receiving_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiving_user"
    )
    message_type = models.ForeignKey(UserInboxMessageType, on_delete=models.CASCADE)
    message_date = models.DateField()
    message_text = models.TextField()
    mark_as_read = models.BooleanField(default=False)
    entity_doc_ref = models.ForeignKey(EntityDocument, on_delete=models.CASCADE)


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    client_code = models.CharField(max_length=4, unique=True)
    client_name = models.CharField(max_length=250)


class ClientEntityDocument(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    entity_document = models.ForeignKey(EntityDocument, on_delete=models.CASCADE)
