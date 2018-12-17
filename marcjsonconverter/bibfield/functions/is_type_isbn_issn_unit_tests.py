# This file is part of Invenio.
# Copyright (C) 2012 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from invenio.testutils import InvenioTestCase

from invenio.testutils import make_test_suite, run_test_suite
from invenio.bibfield_functions.is_type_isbn import is_type_isbn10, is_type_isbn13, is_type_isbn
from invenio.bibfield_functions.is_type_issn import is_type_issn


class ISBNISSNValidationTest(InvenioTestCase):
    valid_isbn10 = ['99921-58-10-7', '9971-5-0210-0', '960-425-059-0',
                    '80-902734-1-6', '85-359-0277-5', '1-84356-028-3',
                    '0-684-84328-5', '0-8044-2957-X', '0-85131-041-9',
                    '0-943396-04-2', '0-9752298-0-X', '9814401196',
                    '1847922570', ]
    valid_isbn13 = ["978-158488-540-5", "9781576754993",
                    "9789814401197", "9781847922571", "978-0307886279"]
    invalid_isbn = ["1-58488-540-5", "1-8758488-540-8",
                    "975-0307886279", "978-0307886274", "0307886272"]

    valid_issn = ['0378-5955', '00280836', '0369 3392', '1523-388X',
                  '0065 132X']
    invalid_issn = ['14317732', '0028-0838']

    def _test_isbn_func(self, func, tests):
        for isbns, expected in tests:
            for n in isbns:
                if expected:
                    msg = "%s did not validate with %s" % (n, func.__name__)
                else:
                    msg = "%s was not expected to validate with %s" % (
                        n, func.__name__)
                self.assertEqual(func(n), expected, msg)

    def test_isbn10(self):
        tests = [(self.valid_isbn10, True), (self.valid_isbn13,
                                             False), (self.invalid_isbn, False), ]
        self._test_isbn_func(is_type_isbn10, tests)

    def test_isbn13(self):
        tests = [(self.valid_isbn10, False), (self.valid_isbn13,
                                              True), (self.invalid_isbn, False), ]
        self._test_isbn_func(is_type_isbn13, tests)

    def test_isbn(self):
        tests = [(self.valid_isbn10, True), (self.valid_isbn13,
                                             True), (self.invalid_isbn, False), ]
        self._test_isbn_func(is_type_isbn, tests)

    def test_issn(self):
        tests = [(self.valid_issn, True), (self.invalid_issn, False), ]
        self._test_isbn_func(is_type_issn, tests)

TEST_SUITE = make_test_suite(ISBNISSNValidationTest,)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)
