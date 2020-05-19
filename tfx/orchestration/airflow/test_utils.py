# Lint as: python3
# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Common utility for testing airflow-based orchestrator."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import subprocess

from typing import Text
from absl import logging


# mysql utilities.
# This assumes mysql instance on localhost:3307 with user tfx.
# For example, you can launch and configure mysql with docker using following
# commands:
#
# $ docker run --name mysqld -p 3307:3306 \
#     -e MYSQL_ROOT_PASSWORD="root" -d mysql
# $ docker exec -i mysqld mysql -uroot -proot <<EOF
# CREATE USER 'tfx'@'%' IDENTIFIED BY '';
# GRANT ALL ON *.* TO 'tfx'@'%' WITH GRANT OPTION;
# FLUSH PRIVILEGES;
# EOF
#
def _run_sql_on_mysql(sql: Text):
  logging.info('[SQL] %s', sql)
  subprocess.run(
      ['mysql', '-u', 'tfx', '-h', '127.0.0.1', '-P', '3307', '-e', sql],
      check=True)


def create_mysql_database(db: Text):
  """Create a mysql database in integration test environment."""
  _run_sql_on_mysql('CREATE DATABASE %s' % db)


def drop_mysql_database(db: Text):
  """Drop a mysql database if exists in integration test environment."""
  _run_sql_on_mysql('DROP DATABASE IF EXISTS %s' % db)
