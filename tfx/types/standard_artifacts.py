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
"""A set of standard TFX Artifact types.

Note: the artifact definitions here are expected to change.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from decimal import Decimal  # pylint: disable=g-importing-member
from typing import Text
import warnings

from tfx.types.artifact import Artifact
from tfx.types.artifact import Property
from tfx.types.artifact import PropertyType
from tfx.types.artifact import ValueArtifact

# Span for an artifact.
SPAN_PROPERTY = Property(type=PropertyType.INT)
# Comma separated of splits for an artifact. Empty string means artifact
# has no split.
SPLIT_NAMES_PROPERTY = Property(type=PropertyType.STRING)
# Value for a string-typed artifact.
STRING_VALUE_PROPERTY = Property(type=PropertyType.STRING)


class Examples(Artifact):
  TYPE_NAME = 'Examples'
  PROPERTIES = {
      'span': SPAN_PROPERTY,
      'split_names': SPLIT_NAMES_PROPERTY,
  }


class ExampleAnomalies(Artifact):
  TYPE_NAME = 'ExampleAnomalies'
  PROPERTIES = {
      'span': SPAN_PROPERTY,
  }


class ExampleStatistics(Artifact):
  TYPE_NAME = 'ExampleStatistics'
  PROPERTIES = {
      'span': SPAN_PROPERTY,
      'split_names': SPLIT_NAMES_PROPERTY,
  }


class ExternalArtifact(Artifact):
  TYPE_NAME = 'ExternalArtifact'


class InferenceResult(Artifact):
  TYPE_NAME = 'InferenceResult'


class InfraBlessing(Artifact):
  TYPE_NAME = 'InfraBlessing'


class Model(Artifact):
  TYPE_NAME = 'Model'


class ModelBlessing(Artifact):
  TYPE_NAME = 'ModelBlessing'


class ModelEvaluation(Artifact):
  TYPE_NAME = 'ModelEvaluation'


class PushedModel(Artifact):
  TYPE_NAME = 'PushedModel'


class Schema(Artifact):
  TYPE_NAME = 'Schema'


class Bytes(ValueArtifact):
  """Artifacts representing raw bytes."""
  TYPE_NAME = 'Bytes'

  def encode(self, value: bytes):
    if not isinstance(value, bytes):
      raise TypeError('Expecting bytes but got value %s of type %s' %
                      (str(value), type(value)))
    return value

  def decode(self, serialized_value: bytes):
    return serialized_value


class String(ValueArtifact):
  """String-typed artifact."""
  TYPE_NAME = 'String'

  # Note, currently we enforce unicode-encoded string.
  def encode(self, value: Text) -> bytes:
    if not isinstance(value, Text):
      raise TypeError('Expecting Text but got value %s of type %s' %
                      (str(value), type(value)))
    return value.encode('utf-8')

  def decode(self, serialized_value: bytes) -> Text:
    return serialized_value.decode('utf-8')


class Integer(ValueArtifact):
  """Integer-typed artifact."""
  TYPE_NAME = 'Integer'

  def encode(self, value: int) -> bytes:
    if not isinstance(value, int):
      raise TypeError('Expecting int but got value %s of type %s' %
                      (str(value), type(value)))
    return str(value).encode('utf-8')

  def decode(self, serialized_value: bytes) -> int:
    return int(serialized_value)


class Float(ValueArtifact):
  """Float-typed artifact."""
  TYPE_NAME = 'Float'

  def encode(self, value: float) -> bytes:
    if not isinstance(value, float):
      raise TypeError('Expecting float but got value %s of type %s' %
                      (str(value), type(value)))
    return str(value).encode('utf-8')

  def decode(self, serialized_value: bytes) -> float:
    # float() can handle bytes, but Decimal() cannot
    serialized_value = serialized_value.decode('utf-8')
    result = float(serialized_value)
    reserialized_value = str(result)
    is_exact = Decimal(reserialized_value) == Decimal(serialized_value)
    if not is_exact:
      warnings.warn(
          'The number "{}" has lost precision when converted to float "{}"'
          .format(serialized_value, reserialized_value))
    return result


class TransformGraph(Artifact):
  TYPE_NAME = 'TransformGraph'


# Still WIP and subject to change.
class HyperParameters(Artifact):
  TYPE_NAME = 'HyperParameters'
