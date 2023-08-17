#!/bin/bash

# Copyright 2013-present Barefoot Networks, Inc. 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

source $THIS_DIR/../env.sh
P4C_BM_SCRIPT=/usr/local/bin/p4c

SWITCH_PATH=/usr/local/bin/simple_switch

CLI_PATH=$BMV2_PATH/tools/runtime_CLI.py 
$P4C_BM_SCRIPT --target bmv2 -x p4-16 p4file/priority_queues.p4 -o p4prog
# This gives libtool the opportunity to "warm-up"

sudo $SWITCH_PATH >/dev/null 2>&1
sudo PYTHONPATH=$PYTHONPATH:$BMV2_PATH/mininet/ python2 topo.py \
    --behavioral-exe $SWITCH_PATH \
    --json p4prog/priority_queues.json \
    --cli $CLI_PATH \
