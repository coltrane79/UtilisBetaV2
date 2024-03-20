import os
import pathlib
import datetime
import uuid
import pandas as pd
import traceback

from .models import EntityType, Entity, EntityDocument, EntityDocumentMeta, RDSTextModel
from django.contrib.postgres.search import SearchQuery


def generate_excel_report(
    entity_code: str, docket: str, date_from: datetime, date_to: datetime
):
    """
    Generates an Excel report based on the provided entity code, start date, and end date.

    Args:
        entity_code (str): The code of the entity for which the report is generated.
        date_from (datetime): The start date for filtering the documents.
        date_to (datetime): The end date for filtering the documents.

    Returns:
        Tuple[int, str]: A tuple containing the status code and the path to the generated Excel report.
            - If the report is generated successfully, the status code is 0 and the path is returned.
            - If an error occurs during the generation process, the status code is -1 and None is returned.
    """
    dir = pathlib.Path(__file__).parent.absolute()

    # get documents from db
    if entity_code != None:
        documents = EntityDocument.objects.filter(
            entity=entity_code,
            issued_by_entity_date__gte=date_from,
            issued_by_entity_date__lte=date_to,
        ).all()
    elif docket != None:
        documents = EntityDocument.objects.filter(
            case_number=docket,
            issued_by_entity_date__gte=date_from,
            issued_by_entity_date__lte=date_to,
        ).all()
    else:
        return (
            -1,
            "Unsupported query type. Please provide either entity code or docket number.",
        )

    try:
        # conver to list of lists
        data = [
            [
                doc["id"],
                doc["entity_id"],
                doc["link"],
                doc["case_number"],
                doc["filename_description"],
                doc["file_url"],
                doc["document_type"],
                doc["issued_by_entity_date"],
                doc["received_by_entity_date"],
                doc["submitter_id"],
                doc["applicant_id"],
                doc["status"],
            ]
            for doc in list(documents.values())
        ]
        # create dataframe
        df = pd.DataFrame(
            data,
            columns=[
                "id",
                "Entity",
                "Link",
                "Case Number / Docket",
                "File Description",
                "File URL",
                "Document Type",
                "Issued By Entity Date",
                "Received By Entity Date",
                "Submitted Id",
                "Applicant Id",
                "Status",
            ],
        )
        # save to temporary file location
        uid = uuid.uuid4()
        df.to_excel(
            os.path.join(str(dir), "temp", f"utilis_report_{uid}.xlsx"), index=False
        )
        return 0, os.path.join(dir, "temp", f"utilis_report_{uid}.xlsx")
    except Exception as e:
        print(traceback.format_exc())
        return -1, e


def generate_excel_search_results(
    entity_code: str, kw_list: [], date_from: datetime, date_to: datetime
):
    """
    Generates an Excel report based on the provided entity code, start date, and end date.

    Args:
        entity_code (str): The code of the entity for which the report is generated.
        date_from (datetime): The start date for filtering the documents.
        date_to (datetime): The end date for filtering the documents.

    Returns:
        Tuple[int, str]: A tuple containing the status code and the path to the generated Excel report.
            - If the report is generated successfully, the status code is 0 and the path is returned.
            - If an error occurs during the generation process, the status code is -1 and None is returned.
    """
    dir = pathlib.Path(__file__).parent.absolute()

    # get documents from db
    if entity_code != None:
        documents = EntityDocument.objects.filter(
            entity=entity_code,
            issued_by_entity_date__gte=date_from,
            issued_by_entity_date__lte=date_to,
        ).all()

    else:
        return (
            -1,
            "Unsupported query type. Please provide either entity code or docket number.",
        )

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

    try:
        # convert to list of lists

        data = []
        if len(search_results) > 0:
            for result in search_results:
                for kw in kw_list:
                    if kw != "":
                        data.append(
                            [
                                result["url"],
                                result["page_number"],
                                kw,
                                result["page_text"].lower().count(kw.lower()),
                                result["page_text"],
                            ]
                        )

        # create dataframe
        df = pd.DataFrame(
            data,
            columns=[
                "url",
                "Page Number",
                "Keyword",
                "Count of Keyword",
                "Page Text",
            ],
        )
        # save to temporary file location
        uid = uuid.uuid4()
        df.to_excel(
            os.path.join(str(dir), "temp", f"utilis_report_{uid}.xlsx"),
            index=False,
            engine="xlsxwriter",
        )
        return 0, os.path.join(dir, "temp", f"utilis_report_{uid}.xlsx")
    except Exception as e:
        print(traceback.format_exc())
        return -1, e
