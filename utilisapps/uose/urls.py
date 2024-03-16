from django.urls import path

from . import views

# app_name = "uose"

urlpatterns = [
    path("", views.index, name="index"),
    path("document-viewer/", views.document_viewer, name="document_viewer"),
    path("docket-viewer/", views.docket_viewer, name="docket_viewer"),
    path("document-viewer/<int:doc_id>", views.document_detail, name="document_detail"),
    path(
        "document-viewer/e-maintain-favorite/<int:doc_id>",
        views.mark_document_as_favorite,
        name="e_doc_favorite",
    ),
    path(
        "document-viewer/e-client-group/<int:doc_id>/<str:client_group_id>",
        views.mark_document_to_client_group,
        name="e_doc_client_group",
    ),
    # path("search-engine", views.search_engine, name="search_engine"),
    path("search-engine/", views.search_engine, name="search_engine"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]
