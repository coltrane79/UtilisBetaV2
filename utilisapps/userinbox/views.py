from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from uose.models import (
    UserEntityDocuments,
    UserInbox,
    Client,
    ClientEntityDocument,
)


@login_required
def inbox(request):

    # messages
    user_messages = UserInbox.objects.filter(receiving_user=request.user).all()
    # favorites
    favorite_documents = [
        document.document_id
        for document in UserEntityDocuments.objects.filter(user=request.user).all()
    ]

    client_groups = Client.objects.all()

    if "get_client_docs" in request.GET:
        selected_client = request.GET.get("selected_client_group")
        client_group_documents = [
            document.entity_document
            for document in ClientEntityDocument.objects.filter(
                client=selected_client
            ).all()
        ]
    else:
        if len(client_groups) > 0:
            selected_client = client_groups[0]
            client_group_documents = [
                document.entity_document
                for document in ClientEntityDocument.objects.filter(
                    client=selected_client
                ).all()
            ]
        else:
            client_group_documents = []

    return render(
        request,
        "userinbox/inbox.html",
        {
            "user_messages": user_messages,
            "favorite_documents": favorite_documents,
            "client_groups": client_groups,
            "selected_client_group": selected_client,
            "client_group_documents": client_group_documents,
        },
    )
