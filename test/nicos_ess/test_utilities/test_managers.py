# -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2021 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Kenan Muric <kenan.muric@ess.eu>
#
# *****************************************************************************

import pytest

from nicos_ess.utilities.managers import wait_until_true


def test_wait_until_true_times_out_if_condition_in_conditions_is_false():
    wait_until_true_gen = wait_until_true(conditions=[True, False],
                                          max_call_count=1)
    with pytest.raises(ValueError):
        next(wait_until_true_gen)


def test_wait_until_true_returns_value_error_if_conditions_are_empty():
    wait_until_true_gen = wait_until_true(conditions=[], )
    with pytest.raises(ValueError):
        next(wait_until_true_gen)


def test_wait_until_true_returns_type_error_if_conditions_is_not_list():
    wait_until_true_gen = wait_until_true(conditions=True, )
    with pytest.raises(TypeError):
        next(wait_until_true_gen)


def test_wait_until_true_returns_type_error_if_item_in_conditions_is_not_bool():
    wait_until_true_gen = wait_until_true(conditions=[False, True, "INVALID"],)
    with pytest.raises(TypeError):
        next(wait_until_true_gen)


def test_wait_until_true_generates_as_expected_when_conditions_are_given():
    conditions = [True, True, True, True]
    wait_until_true_gen = wait_until_true(conditions=conditions)
    assert not next(wait_until_true_gen)




