# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2004, 2005, 2006, 2007, 2008, 2010, 2011 CERN.
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


def get_number_of_copies(recid):
    """
    Searches inside crcITEM for the number of appearances of recid

    @param recid:

    @return: Number of copies
    """
    from invenio.dbquery import run_sql
    if recid:
        try:
            return run_sql('SELECT COUNT(*) FROM crcITEM WHERE id_bibrec=%s', (recid,))[0][0]
        except:
            return -1
