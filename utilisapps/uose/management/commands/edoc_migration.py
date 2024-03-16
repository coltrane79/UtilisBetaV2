import os
import traceback

import pathlib
import pandas as pd

from django.core.management.base import BaseCommand

from uose.models import Entity, EntityDocument


class Command(BaseCommand):

    _data = pd.DataFrame()
    _migration_records = pd.DataFrame()
    _meta = pd.DataFrame()
    _status = pd.DataFrame()

    def __str__(self):
        return f"EntityDocumentsMigration: {self._data.shape[0]} records\n{self._data.info()}"

    def _load_data(self):
        cwd = os.getcwd()
        try:
            # load migration data
            self._migration_records = pd.read_csv(
                os.path.join(
                    cwd,
                    "uose",
                    "management",
                    "load_files",
                    "oeb_data.csv",
                ),
                header=0,
                encoding="cp1252",
            )
            # load meta data
            self._meta = pd.read_csv(
                os.path.join(
                    cwd,
                    "uose",
                    "management",
                    "load_files",
                    "entity_doc_meta.csv",
                ),
                header=0,
                encoding="cp1252",
                low_memory=False,
            )
            # load doc status
            self._status = pd.read_csv(
                os.path.join(
                    cwd,
                    "uose",
                    "management",
                    "load_files",
                    "entity_doc_status.csv",
                ),
                header=0,
                encoding="cp1252",
            )

            # merge data
            self._data = pd.merge(
                self._migration_records,
                self._meta,
                how="left",
                left_on="Id",
                right_on="id",
            )
            self._data = pd.merge(
                self._data,
                self._status,
                how="left",
                left_on="id",
                right_on="EntityDocumentsId",
            )

        except FileNotFoundError as f_ex:
            print(f"File not found: {f_ex}")
        except KeyError as k_ex:
            print(f"Merging Error: {k_ex}")

    def handle(self, **options):
        """
        Prints each row of the merged data.

        This method iterates over each row of the merged data and prints the row.

        """
        self._load_data()
        self._data["IssuedByDate"] = self._data["IssuedByDate"].astype(str)
        self._data["ReceivedByRegulator Date"] = self._data[
            "ReceivedByRegulator Date"
        ].astype(str)

        print(
            f"--ENTITY DOCUMENTS LOAD FROM FILE--\n{self}\n--ENTITY DOCUMENTS SAMPLE--\n{self._data.head()}"
        )

        if len(self._data) > 0:

            try:
                print(f"\n create Document records: {len(self._data)}")
                edocs = [
                    EntityDocument(
                        entity=Entity(entity=row["Entity_x"]),
                        link=row["Link"],
                        case_number=row["CaseNumber"],
                        filename_description=row["Description"],
                        file_url=row["FileURL"],
                        document_type=row["DocumentType"],
                        issued_by_entity_date=row["IssuedByDate"],
                        received_by_entity_date=row["ReceivedByRegulator Date"],
                        submitter=Entity(entity="UNKN"),
                        applicant=Entity(entity="UNKN"),
                    )
                    for index, row in self._data.iterrows()
                ]
                print(f"\n Executing Bulk Create: {len(edocs)} records.")
                EntityDocument.objects.bulk_create(edocs)

            except Exception as ex:
                print(f"Error Migrating Documents: ty=={traceback.format_exc()}")
