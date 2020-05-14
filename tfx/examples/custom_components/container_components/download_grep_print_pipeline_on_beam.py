# Lint as: python2, python3
# Copyright 2019 Google LLC. All Rights Reserved.
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
"""Container-based pipeline sample."""

import os

import absl

from tfx.examples.custom_containers.container_components import download_grep_print_pipeline
from tfx.orchestration import pipeline as pipeline_module
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner


if __name__ == '__main__':

  absl.logging.set_verbosity(absl.logging.INFO)

  text_url = 'https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt'
  pattern = 'art thou'
  tasks = download_grep_print_pipeline.create_pipeline_tasks(
      text_url=text_url,
      pattern=pattern,
  )

  _pipeline_name = 'download-grep-print-pipelin'

  _tfx_root = os.path.join(os.environ['HOME'], 'tfx_root')
  _pipeline_root = os.path.join(_tfx_root, 'pipelines', _pipeline_name)
  # Sqlite ML-metadata db path.
  _metadata_path = os.path.join(_tfx_root, 'metadata', _pipeline_name,
                                'metadata.db')

  pipeline = pipeline_module.Pipeline(
      pipeline_name=_pipeline_name,
      pipeline_root=_pipeline_root,
      components=tasks,
  )
  BeamDagRunner().run(pipeline)
