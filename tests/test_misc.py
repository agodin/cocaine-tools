#
# Copyright (c) 2013+ Evgeny Safronov <division494@gmail.com>
# Copyright (c) 2013+ Anton Tiurin <noxiouz@yandex.ru>
# Copyright (c) 2011-2014 Other contributors as noted in the AUTHORS file.
#
# This file is part of Cocaine-tools.
#
# Cocaine is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cocaine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import json
import os
import tarfile

from cocaine.tools.actions import readArchive
from cocaine.tools.actions import CocaineConfigReader

from cocaine.tools.actions.common import split_by_groups
from cocaine.tools.actions.group import validate_routing_group, GroupWithZeroTotalWeight, MalformedGroup

from cocaine.tools.helpers import JSONUnpacker

from nose import tools


@tools.raises(tarfile.TarError)
def test_read_archive():
    readArchive(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             "fixtures/simple_app/manifest.json"))


def test_config_reader():
    CocaineConfigReader.load(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             "fixtures/simple_app/manifest.json"))


def test_json():
    j = JSONUnpacker()
    data = {"A": 1}
    js = json.dumps(data)
    j.feed(js)
    j.feed(js)
    j.feed("A")
    for i in j:
        assert i == data

    assert j.buff == "A"


@tools.raises(GroupWithZeroTotalWeight)
def test_validate_group_empty():
    gr = {}
    validate_routing_group(gr)


@tools.raises(GroupWithZeroTotalWeight)
def test_validate_group_with_zero_total_weight():
    gr = {"A": 0, "B": 0}
    validate_routing_group(gr)


@tools.raises(MalformedGroup)
def test_validate_group_malformed_group_with_float():
    gr = {"A": 9.0, "B": 0}
    validate_routing_group(gr)


@tools.raises(MalformedGroup)
def test_validate_group_malformed_group_with_negative_weight():
    gr = {"A": -1, "B": 1}
    validate_routing_group(gr)


def test_validate_group():
    gr = {"A": 1,
          "B": 99999999999999999999999999}
    validate_routing_group(gr)



def test_split_by_group():
    expected = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
                [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
                [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
                [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
                [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
                [80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
                [90, 91, 92, 93, 94, 95, 96, 97, 98, 99],
                [100, 101]]
    actual = list(split_by_groups(range(0, 102), 10))
    assert expected == actual, actual
