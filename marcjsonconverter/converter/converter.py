# -*- coding: utf-8 -*-
"""
  Copyright 2018 INFN (Italy)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""

__author__ = 'marco'

import json
import sys
from datetime import datetime
from marcjsonconverter.bibfield.bibfield import create_record

class Converter:
    def __init__(self, list_files, collection, doi_filter, communities):
        self.list_files = list_files
        self.collection = collection
        self.doi_filter = doi_filter
        self.no_doi = 0
        self.communities = communities

    @classmethod
    def marc_to_record(cls, blob):
        record = create_record(blob)
        return record

    def marc_to_json(self, blob):
        record = Converter.marc_to_record(blob)
        # print("The original record is: %s"%str(record))
        record._dict["access_right"] = "open"
        record._dict.pop("__meta_metadata__")
        if "meeting" in record._dict:
            record._dict["upload_type"] = {"type": "publication",
                                           "subtype": "conferencepaper"}
            record._dict["publication_date"] = record._dict["meeting"]["dates"]
        elif "journal" in record._dict:
            record._dict["upload_type"] = {"type": "publication",
                                           "subtype": "article"}
            date = record._dict["journal"].pop("date")
        elif "imprint" in record._dict:
            if isinstance(record._dict["imprint"], (list)):
                record._dict["imprint"] = record._dict["imprint"][0]
            if record._dict["collection"]["primary"].startswith("SOFTWARE"):
                record._dict["upload_type"] = {"type": "software"}
            elif record._dict["collection"]["primary"].startswith("PRESENTATION"):
                record._dict["upload_type"] = {"type": "presentation"}
            else:
                record._dict["upload_type"] = {"type": "publication",
                                               "subtype": "section"}
            if "date" in record._dict["imprint"]:
                date = record._dict["imprint"].pop("date")
        else:
            record._dict["upload_type"] = {"type": "publication",
                                           "subtype": "preprint"}

        try:
            date
        except:
            if "version_id" in record._dict:
                date = record._dict["version_id"][0:10]

        try:
            record._dict["publication_date"] = datetime.strptime(
                date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except:
            try:
                record._dict["publication_date"] = datetime.strptime(
                    date, "%Y-%m").strftime("%Y-%m-%d")
            except:
                try:
                    record._dict["publication_date"] = datetime.strptime(
                        date[0:4], "%Y").strftime("%Y-%m-%d")
                except:
                    print >> sys.stderr, "Problem with record %s"%str(record._dict)
                    print >> sys.stderr, "Date is %s" % (date)

        if "comment" in record._dict:
            if isinstance(record._dict["comment"], (list, tuple)):
                for com in record._dict["comment"]:
                    if "license" in com:
                        license = com["license"]
                    if "comment" in com:
                        record._dict["notes"] = com["comment"]
            else:
                if "license" in record._dict["comment"]:
                    license = record._dict["comment"]["license"]

                if "comment" in record._dict["comment"]:
                    record._dict["notes"] = record._dict["comment"]["comment"]

            record._dict.pop("comment")

        if "license" in record._dict:
            license = record._dict["license"]["identifier"]

        try:
            license
        except:
#            print >> sys.stderr, "No recognised license for record %s\n"%str(record._dict)
            license = "Check Publication"

        if license.lower() in ["cc-by", "cc-by-3.0", "cc-by-4.0", "ccy v4.0"]:
            record._dict["license"] = dict()
            record._dict["license"]["identifier"] = "cc-by"
            record._dict["license"]["license"] = "Creative Commons Attribution"
            record._dict["license"]["url"] = "http://www.opendefinition.org/licenses/cc-by"
        elif license.lower().startswith("cc-by-nc-nd"):
            record._dict["license"] = dict()
            record._dict["license"]["license"] = "Creative Commons Attribution-NonCommercial-NoDerivatives"
            record._dict["license"]["identifier"] = "cc-by-nc-nd-4.0"
            record._dict["license"]["url"] = "https://creativecommons.org/licenses/by-nc-nd/4.0/"
        elif license.lower().startswith("cc-by-sa"):
            record._dict["license"] = dict()
            record._dict["license"]["identifier"] = "cc-by-sa"
            record._dict["license"]["url"] = "http://www.opendefinition.org/licenses/cc-by-sa"
            record._dict["license"][
                "license"] = "Creative Commons Attribution Share-Alike"
        elif license.lower().startswith("cc-by-nc"):
            record._dict["license"] = dict()
            record._dict["license"]["identifier"] = "cc-by-nc-4.0"
            record._dict["license"]["url"] = "https://creativecommons.org/licenses/by-nc/4.0/"
            record._dict["license"][
                "license"] = "Creative Commons Attribution-NonCommercial"
        elif license.lower().startswith("cc-zero"):
            record._dict["license"] = dict()
            record._dict["license"]["identifier"] = "cc-zero"
            record._dict["license"]["url"] = "http://www.opendefinition.org/licenses/cc-zero"
            record._dict["license"][
                "license"] = "Creative Commons CCZero"
        elif license == ("Check Publication"):
            record._dict["license"] = dict()
            record._dict["license"]["identifier"] = "cc-by"
            record._dict["license"]["url"] = "http://www.opendefinition.org/licenses/cc-by"
            record._dict["license"]["license"] = "Creative Commons Attribution"
        else:
            print >> sys.stderr, "No recognised license %s for record %s\n"%(license, record._dict["recid"])


        try:
            if "primary_report_number" in record._dict and record._dict["primary_report_number"].startswith("arXiv"):
                if not "alternate_identifiers" in record._dict:
                    record._dict["alternate_identifiers"] = []
                record._dict["alternate_identifiers"].append(
                    {"identifier": record._dict["primary_report_number"],
                     "scheme": "arxiv"})
        except:
            if isinstance(record._dict["primary_report_number"], (list, tuple)):
                for elem in record._dict["primary_report_number"]:
                    if elem.startswith("arXiv"):
                        if not "alternate_identifiers" in record._dict:
                            record._dict["alternate_identifiers"] = []
                        record._dict["alternate_identifiers"].append(
                            {"identifier": elem, "scheme": "arxiv"})

        if "reference" in record._dict:
            # print("This record has reference: %s"%record._dict)
            # record._dict.pop("reference")
            pass

        if self.communities:
            record._dict["communities"] = [
                x.strip() for x in self.communities.split(',')
            ]

        if "bibdocs" in record._dict:
            record._dict.pop("bibdocs")
        if "primary_report_number" in record._dict:
            record._dict.pop("primary_report_number")
        if "publication_info" in record._dict:
            record._dict.pop("publication_info")
        if "number_of_citations" in record._dict:
            record._dict.pop("number_of_citations")
        if "funding_info" in record._dict:
            record._dict.pop("funding_info")
        if "copyright_status" in record._dict:
            record._dict.pop("copyright_status")
        if "files" in record._dict:
            record._dict.pop("files")
        if "collection" in record._dict:
            record._dict.pop("collection")
        if "physical_description" in record._dict:
            record._dict.pop("physical_description")
        if "version_id" in record._dict:
            record._dict.pop("version_id")
        if "number_of_reviews" in record._dict:
            record._dict.pop("number_of_reviews")
        if "number_of_comments" in record._dict:
            record._dict.pop("number_of_comments")
        if "persistent_identifiers_keys" in record._dict:
            record._dict.pop("persistent_identifiers_keys")
        if "issn" in record._dict:
            record._dict.pop("issn")
        if "number_of_authors" in record._dict:
            record._dict.pop("number_of_authors")
        if "email" in record._dict:
            record._dict.pop("email")
        if "subject" in record._dict:
            record._dict.pop("subject")
        if "action_note" in record._dict:
            record._dict.pop("action_note")
        if "other_report_number" in record._dict:
            record._dict.pop("other_report_number")
        if "authority_another_topical_term" in record._dict:
            record._dict.pop("authority_another_topical_term")
        if "comment" in record._dict:
            if not record._dict["comment"]:
                record._dict.pop("comment")
        if "imprint" in record._dict:
            if not record._dict["imprint"]:
                record._dict.pop("imprint")
        return record._dict


    def record_with_json_field_from_marc(self):
        self.json_data = []
        self.rec_no_doi = []
        results = []
        doi_list = []

        for file in self.list_files:
            results.append(self._parse_file(file))

        for res in results:
            for rec in res:
                if "doi" in rec["record"][0]["json"]:
                    if rec["record"][0]["json"]["doi"] in doi_list:
                        continue
                    doi_list.append(rec["record"][0]["json"]["doi"])
                    if self.doi_filter:
                        if (rec["record"][0]["json"]["doi"]).startswith(self.doi_filter):
                            self.json_data.append(rec)
                    else:
                        self.json_data.append(rec)
                else:
                    self.no_doi = self.no_doi + 1
                    self.rec_no_doi.append(rec["record"][0]["json"]["recid"])
        print("Found %d records without doi"%self.no_doi)
        print("They are: %s"%str(self.rec_no_doi))
        return self.json_data

    def _in_collection(self, record):
        return self.collection in record["collections"]

    def _parse_file(self, file_name):
        with open(file_name) as json_file:
            json_data = list(filter(self._in_collection, json.load(json_file)))

        for rec in json_data:
            ver = rec["record"][-1]
            if ver["json"] is None:
                ver["json"] = self.marc_to_json(ver["marcxml"])
            rec["record"] = [ver]
            rec.pop("collections")
        return json_data
