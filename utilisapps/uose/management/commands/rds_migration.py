import os
import sys
import traceback
import pickle
import time
import datetime
import re

import pathlib
import pandas as pd

from django.core.management.base import BaseCommand

from uose.models import RDSTextModel


class Command(BaseCommand):

    _SAVE_TO_DB = True

    def __str__(self):
        return f"EntityDocumentsMigration: {self._data.shape[0]} records\n{self._data.info()}"

    def handle(self, **options):
        """
        Prints each row of the merged data.

        This method iterates over each row of the merged data and prints the row.

        """
        cwd = os.getcwd()
        analytics = os.path.join(cwd, "uose", "management", "analytics_files")

        # create empty list of rds text objects
        rds_obj = []
        # loop through files

        sys.stdout.write(
            f"\n -- Processing RDS Text Files @ {datetime.datetime.now().strftime('%H:%M:%S')}-- \n"
        )
        for file in os.listdir(analytics):
            if file.endswith(".pickle"):  # check if file is a pickle file
                with open(os.path.join(analytics, file), "rb") as t_file:
                    rds_db = pickle.load(t_file)

                    sys.stdout.write(
                        f"\n -- Processing {file} @ @ {datetime.datetime.now().strftime('%H:%M:%S')}-- \n"
                    )

                    for url, text in rds_db.items():
                        sys.stdout.write(f"\n -- Processing {url} -- \n")
                        try:
                            for p_number, p_text in text.items():

                                if "\x00" in p_text:
                                    sys.stdout.write(
                                        f"\n -- Found Null Byte in Page {p_number} -- \n"
                                    )
                                    p_text = p_text.replace("\x00", "")
                                    time.sleep(1)

                                if self._SAVE_TO_DB:

                                    clean_text = p_text.replace("\00", "")
                                    newline_match = re.findall(
                                        "(.+?)([\n\r]+)(.+?[\.\?\!]+)", clean_text
                                    )

                                    # handling newline removal

                                    newline_bypass_str = [
                                        "Appendix",
                                        "appendix" "reference",
                                        "Reference",
                                        "Ref",
                                        "ref" "Ref.",
                                        "ref.",
                                        "Exhibit",
                                        "exhibit",
                                        "Exhibits",
                                        "exhibits",
                                    ]

                                    for newline in newline_match:
                                        apply_modifer = True
                                        for nbs in newline_bypass_str:
                                            """if newline[0] == " " and newline[2] == " ":
                                            apply_modifer = False
                                            break"""
                                            if newline[0] == " ":
                                                apply_modifer = False
                                                break
                                            if nbs in newline[0] or nbs in newline[2]:
                                                apply_modifer = False
                                                break
                                        if apply_modifer:
                                            clean_text = clean_text.replace(
                                                newline[0] + newline[1] + newline[2],
                                                newline[0] + newline[2],
                                            )

                                    rds_entry = RDSTextModel(
                                        url=url,
                                        page_number=p_number,
                                        page_text=clean_text,
                                    )

                                    print("\n -- Start RDS Entry -- ")
                                    print(f"\n -- URL: {rds_entry.url}")
                                    print(f"\n -- Page Number: {rds_entry.page_number}")
                                    print(
                                        f"\n -- Page Text: {rds_entry.page_text[:100]}"
                                    )
                                    print("\n -- End RDS Entry -- ")

                                    try:
                                        rds_entry.save()
                                    except Exception as ex:
                                        sys.stdout.write(
                                            f"\n -- Error Saving RDS Object: {traceback.format_exc()}  -- \n"
                                        )
                                        time.sleep(5)

                                else:
                                    sys.stdout.write(
                                        f"\n -- URL: {url} -- Page: {p_number} -- Text: {p_text} -- \n"
                                    )
                        except Exception as ex:
                            sys.stdout.write(
                                f"\n -- Error handling url: {traceback.format_exc()} -- "
                            )
                            time.sleep(5)

        # sys.stdout.write("\n -- Saving RDS Object -- \n")
        # try:
        #     if self._SAVE_TO_DB:
        #         RDSTextModel.objects.bulk_create(rds_obj)
        # except Exception as ex:
        #     sys.stdout.write(
        #         f"\n -- Error Saving RDS Object: {traceback.format_exc()}  -- \n"
        #     )

        sys.stdout.write(
            f"\n -- Completed Saving RDS Object @ {datetime.datetime.now().strftime('%H:%M:%S')}-- \n"
        )
