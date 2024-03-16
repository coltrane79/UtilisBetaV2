"""
UOSE Models:
This script contains the views for the UOSE application in the UtilisWeb project.

Version History:
- 1.0.0 (2022-01-01): Initial version of the views.

Change Log:
- 2022-01-01: Created the views.py file.

"""

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.postgres.search import SearchQuery

import json

from .models import (
    EntityType,
    Entity,
    EntityDocument,
    EntityDocumentMeta,
    RDSTextModel,
    UserNotesEntityDocuments,
    UserEntityDocuments,
    User,
    UserInboxMessageType,
    UserInbox,
    Client,
    ClientEntityDocument,
)
from .uose_helpers import generate_excel_report, generate_excel_search_results

import pandas as pd
from pathlib import Path
from datetime import datetime


def login_user(request):
    """login:  This is the login view for the UOSE application.

    Args:
        request (django.http.request): request object

    Returns:
        djanog.http.HttpResponse: HTTP response
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # send back if no username or password
        if username is None or password is None or username == "" or password == "":
            return render(
                request,
                "authentication/login.html",
                {"error": "Please Enter a valid username and password."},
            )

        # test password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.success(request, "Invalid username or password")
            return render(
                request,
                "authentication/login.html",
            )
    else:
        return render(request, "authentication/login.html", {"error": None})


def logout_user(request):
    """logout:  This is the logout view for the UOSE application.

    Args:
        request (django.http.request): request object

    Returns:
        djanog.http.HttpResponse: HTTP response
    """
    logout(request)
    return redirect("login")


@login_required
def index(request):
    """indexview:  This is the index view for the UOSE application.

    Args:
        request (django.http.request): request object

    Returns:
        djanog.http.HttpResponse: HTTP response
    """
    e_types = EntityType.objects.all()
    e_doc_list = EntityDocument.objects.filter(
        issued_by_entity_date__gte="2023-12-01"
    ).all
    ctx = {"e_types": e_types, "documents": e_doc_list}

    return render(request, "dashboard/home-dashboard.html", ctx)


@login_required
def document_viewer(request):
    """document_viewer:  This is the document viewer for the UOSE application.

    Args:
        request (django.http.request): request object

    Returns:
        djanog.http.HttpResponse: HTTP response
    """

    entities = Entity.objects.all().filter(entity_type_id="REG").only("entity")
    # Get Form Data Elements
    entity = (
        request.GET.get("entity")
        if request.method == "GET"
        else request.POST.get("entity")
    )
    try:
        entity_code = entity.split("|")[0].strip()
    except:
        entity_code = ""

    date_from = (
        request.GET.get("issued_date_from")
        if request.method == "GET"
        else request.POST.get("issued_date_from")
    )
    date_to = (
        request.GET.get("issued_date_to")
        if request.method == "GET"
        else request.POST.get("issued_date_to")
    )

    page = request.GET.get("page")

    if request.method == "POST" and "excel_download" in request.POST:
        rc, file = generate_excel_report(entity_code, None, date_from, date_to)
        if rc == 0:
            with open(file, "rb") as f:
                response = HttpResponse(f, content_type="application/vnd.ms-excel")
                response["Content-Disposition"] = f"attachment; filename={file}"
                return response
        else:
            messages.error(request, f"Error generating report: {file}")

    if request.method == "GET":
        # get query parameters

        ctx = {
            "entities": entities if len(entities) > 0 else ["OEB"],
            "selected_entity": entity_code,
            "documents": [],
            "sel_entity": entity,
            "sel_date_from": date_from,
            "sel_date_to": date_to,
        }

        # TODO: validate form

        # if form is valid retrieve documents
        if entity is not None:
            # TODO:  Tie into Postgres DB

            documents = EntityDocument.objects.filter(
                entity=entity_code,
                issued_by_entity_date__gte=date_from,
                issued_by_entity_date__lte=date_to,
            ).all()

            if len(documents) > 0:
                paginator = Paginator(documents, 20)
                records = paginator.get_page(page)
                ctx["documents"] = records
            else:
                ctx["documents"] = []

    return render(request, "uose/document-viewer.html", ctx)


@login_required
def docket_viewer(request):
    """document_viewer:  This is the document viewer for the UOSE application.

    Args:
        request (django.http.request): request object

    Returns:
        djanog.http.HttpResponse: HTTP response
    """

    # Get Form Data Elements
    docket = (
        request.GET.get("uose_docket")
        if request.method == "GET"
        else request.POST.get("uose_docket")
    )

    date_from = (
        request.GET.get("issued_date_from")
        if request.method == "GET"
        else request.POST.get("issued_date_from")
    )
    date_to = (
        request.GET.get("issued_date_to")
        if request.method == "GET"
        else request.POST.get("issued_date_to")
    )

    page = request.GET.get("page")

    if request.method == "POST" and "excel_download" in request.POST:
        # call to generate report, passing None for entity
        rc, file = generate_excel_report(None, docket, date_from, date_to)
        if rc == 0:
            with open(file, "rb") as f:
                response = HttpResponse(f, content_type="application/vnd.ms-excel")
                response["Content-Disposition"] = f"attachment; filename={file}"
                return response
        else:
            messages.error(request, f"Error generating report: {file}")

    if request.method == "GET":
        # get query parameters

        ctx = {
            "selected_docket": docket if docket is not None else "",
            "documents": [],
            "sel_date_from": date_from,
            "sel_date_to": date_to,
        }

        # TODO: validate form

        # if form is valid retrieve documents
        if docket is not None:
            # TODO:  Tie into Postgres DB

            documents = (
                EntityDocument.objects.filter(
                    case_number=docket,
                    issued_by_entity_date__gte=date_from,
                    issued_by_entity_date__lte=date_to,
                )
                .order_by("-issued_by_entity_date")
                .all()
            )

            if len(documents) > 0:
                paginator = Paginator(documents, 20)
                records = paginator.get_page(page)
                ctx["documents"] = records
            else:
                ctx["documents"] = []

    return render(request, "uose/docket-viewer.html", ctx)


@login_required
def document_detail(request, doc_id):
    """
    View function that retrieves and displays the details of a document.

    Args:
        request (HttpRequest): The HTTP request object.
        doc_id (int): The ID of the document to retrieve.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.

    Raises:
        Http404: If the document with the specified ID does not exist.

    """
    try:
        # get base document
        users_list = User.objects.all()
        client_groups = Client.objects.all()
        record = get_object_or_404(EntityDocument, id=doc_id)
        record_fav = UserEntityDocuments.objects.filter(
            user=request.user, document_id=record
        ).first()
        # get related documents by on case number
        # order newest to lsata
        related_docs = (
            EntityDocument.objects.filter(case_number=record.case_number)
            .exclude(id=doc_id)
            .order_by("-issued_by_entity_date")
            .all()
        )
        document_notes = UserNotesEntityDocuments.objects.filter(
            document_id=doc_id
        ).all()
        client_groups_docs = ClientEntityDocument.objects.filter(
            entity_document=record
        ).all()
        is_favorite = True if record_fav is not None else False
        is_client_group = True if len(client_groups_docs) > 0 else False
        # TODO: get meta data
        meta = None
        # get text data from text db model
        text_model = RDSTextModel.objects.filter(url=record.file_url).all()
        # load to list if text model has data
        if len(text_model) > 0:
            pages = [page.page_text for page in text_model]
        else:
            pages = []

        if (
            request.method == "POST"
            and "post_new_note"
            or "reply_to_note" in request.POST
        ):

            page_no_ref = request.POST.get("uose_page_no_ref")
            page_ext_ref = request.POST.get("uose_text_document_extract")
            post_text = request.POST.get("uose_document_note")
            post_date = datetime.now()
            private_note = request.POST.get("uose_private_note")
            notify_partn = request.POST.get("notify_partner")
            user_to_notify = request.POST.get("user_to_notify")

            try:
                # create new note
                new_note = UserNotesEntityDocuments(
                    document_id=record,
                    user=request.user,
                    private_note=False,
                    note_text=post_text,
                    note_date=post_date,
                    page_number=int(page_no_ref),
                    text_reference=page_ext_ref,
                )

                # save
                new_note.save()

                if notify_partn == "on" and user_to_notify != "":

                    recv_user = User.objects.filter(id=int(user_to_notify)).first()
                    msg_type = UserInboxMessageType.objects.filter(
                        message_type="NOTE"
                    ).first()

                    # send to inbox
                    new_mail_item = UserInbox(
                        sending_user=request.user,
                        receiving_user=recv_user,
                        message_type=msg_type,
                        message_date=datetime.now(),
                        message_text=post_text,
                        mark_as_read=False,
                        entity_doc_ref=record,
                    )

                    # save item
                    new_mail_item.save()

                document_notes = UserNotesEntityDocuments.objects.filter(
                    document_id=doc_id
                ).all()

                # TODO: redirect after POST

            except Exception as ex:
                messages.error(request, f"Error creating note on {doc_id}: {ex}")

        return render(
            request,
            "uose/document-detail.html",
            {
                "doc_id": doc_id,
                "is_favorite": is_favorite,
                "record": record,
                "related_docs": related_docs,
                "document_notes": document_notes,
                "status": None,
                "meta": meta,
                "pages": pages,
                "users_list": users_list,
                "client_groups": client_groups,
                "is_client_group": is_client_group,
            },
        )

    except Exception as ex:
        messages.error(request, f"Error retrieving document id {id}: {ex}")
        return render(
            request,
            "uose/document-detail.html",
            {
                "doc_id": doc_id,
                "is_favorite": False,
                "record": None,
                "related_docs": None,
                "document_notes": None,
                "status": None,
                "meta": None,
                "pages": [],
                "user_list": users_list,
                "client_groups": client_groups,
                "is_client_group": is_client_group,
            },
        )


@login_required
def search_engine(request):
    """search_engine:  This is the search engine view for the UOSE application.

    Args:
        request (django.http.request): request object

    Returns:
        django.http.HttpResponse: HTTP response
    """

    entities = Entity.objects.all().filter(entity_type_id="REG").only("entity")
    dockets = [
        docket["case_number"]
        for docket in EntityDocument.objects.values("case_number")
        .order_by("-case_number")
        .distinct()
    ]
    document_types = [
        doc_type["document_type"]
        for doc_type in EntityDocument.objects.values("document_type").distinct()
    ]

    ctx = {
        "entities": entities,
        "dockets": dockets,
        "document_types": document_types,
    }

    if request.method == "POST" and "excel_download" in request.POST:
        try:
            entity_code = request.GET.get("entity").split("|")[0].strip()
        except:
            entity_code = "*"

        date_from = request.GET.get("issued_date_from")
        date_to = request.GET.get("issued_date_to")
        # docket_list = request.GET.get("dockets")
        # document_list = request.GET.get("document_types")
        kw_list = request.GET.get("kw_list").split("|")
        rc, file = generate_excel_search_results(
            entity_code, kw_list, date_from, date_to
        )
        if rc == 0:
            with open(file, "rb") as f:
                response = HttpResponse(f, content_type="application/vnd.ms-excel")
                response["Content-Disposition"] = f"attachment; filename={file}"
                return response
        else:
            messages.error(request, f"Error generating report: {file}")

    if "kw_search_documents" in request.GET:
        try:
            entity_code = request.GET.get("entity").split("|")[0].strip()
        except:
            entity_code = "*"

        date_from = request.GET.get("issued_date_from")
        date_to = request.GET.get("issued_date_to")
        ctx["issued_date_from"] = date_from
        ctx["issued_date_to"] = date_to
        # docket_list = request.GET.get("dockets")
        # document_list = request.GET.get("document_types")
        kw_list = request.GET.get("kw_list").split("|")

        # get list of documents
        document_urls = (
            EntityDocument.objects.filter(
                entity=entity_code,
                issued_by_entity_date__gte=date_from,
                issued_by_entity_date__lte=date_to,
                # case_number__in=docket_list,
                # document_type__in=document_list,
            )
            .only("file_url")
            .values_list("file_url", flat=True)
        )
        search_results = []

        for kw in kw_list:
            # search each document for the keyword
            if kw != "":
                search_engine_results = RDSTextModel.objects.filter(
                    url__in=list(document_urls),
                    page_text__search=SearchQuery(kw, search_type="phrase"),
                ).all()
                if search_engine_results is not None:
                    # print(search_engine_results)
                    search_results.extend(list(search_engine_results.values()))

        ctx["search_results"] = []
        ctx["search_count"] = len(search_results)
        if len(search_results) > 0:
            for result in search_results:
                for kw in kw_list:
                    if kw != "":
                        ctx["search_results"].append(
                            [
                                result["url"],
                                result["page_number"],
                                kw,
                                result["page_text"].lower().count(kw.lower()),
                                result["page_text"],
                            ]
                        )

        return render(request, "uose/search-engine-results.html", ctx)

    return render(request, "uose/search-engine.html", ctx)


@login_required
def mark_document_as_favorite(request, doc_id):
    """
    View function that marks a document as a favorite for the user.

    Args:
        request (HttpRequest): The HTTP request object.
        doc_id (int): The ID of the document to mark as a favorite.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.

    Raises:
        Http404: If the document with the specified ID does not exist.

    """

    document = get_object_or_404(EntityDocument, id=doc_id)

    try:
        user_fav = UserEntityDocuments.objects.filter(
            user=request.user, document_id=document
        ).first()
        if user_fav is not None:
            user_fav.delete()
            return HttpResponse(
                json.dumps(
                    {
                        "is_favorite": False,
                        "message": f"Document {doc_id} removed from favorites!",
                    }
                )
            )
        else:
            user_fav = UserEntityDocuments(user=request.user, document_id=document)
            user_fav.save()
            return HttpResponse(
                json.dumps(
                    {
                        "is_favorite": True,
                        "message": f"Document {doc_id} added to favorites!",
                    }
                )
            )
    except Exception as ex:
        print(ex)
        return HttpResponse(json.dumps({"message": f"Error adding to Favoriate! {ex}"}))


@login_required
def mark_document_to_client_group(request, doc_id, client_group_id):
    """
    View function that marks a document as a favorite for the user.

    Args:
        request (HttpRequest): The HTTP request object.
        doc_id (int): The ID of the document to mark as a favorite.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.

    Raises:
        Http404: If the document with the specified ID does not exist.

    """

    document = get_object_or_404(EntityDocument, id=doc_id)
    client_group = Client.objects.filter(client_code=client_group_id).first()

    try:
        client_groups_docs = ClientEntityDocument.objects.filter(
            client=client_group, entity_document=document
        ).all()
        if len(client_groups_docs) > 0:
            client_groups_docs.delete()
            return HttpResponse(
                json.dumps(
                    {
                        "is_client_group": False,
                        "message": f"Document {doc_id} removed from Client Group {client_group.client_name}",
                    }
                )
            )
        else:
            client_group_doc = ClientEntityDocument(
                client=client_group, entity_document=document
            )
            client_group_doc.save()
            return HttpResponse(
                json.dumps(
                    {
                        "is_client_group": True,
                        "message": f"Document {doc_id} added to Client Group {client_group.client_name}",
                    }
                )
            )
    except Exception as ex:
        print(ex)
        return HttpResponse(
            json.dumps({"message": f"Error adding to Client Group {ex}"})
        )
