# coding: utf-8

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import print_function

import warnings
import mxnet as mx
import numpy as np

import gluoncv as gcv
from common import try_gpu

@try_gpu(0)
def test_classification_models():
    ctx = mx.context.current_context()
    x = mx.random.uniform(shape=(2, 3, 32, 32), ctx=ctx)
    cifar_models = [
        'cifar_resnet20_v1', 'cifar_resnet56_v1', 'cifar_resnet110_v1',
        'cifar_resnet20_v2', 'cifar_resnet56_v2', 'cifar_resnet110_v2',
        'cifar_wideresnet16_10', 'cifar_wideresnet28_10', 'cifar_wideresnet40_8',
        'cifar_resnext29_32x4d', 'cifar_resnext29_16x64d',
    ]
    for model in cifar_models:
        net = gcv.model_zoo.get_model(model)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            net.initialize()
        net.collect_params().reset_ctx(ctx)
        net(x)
        mx.nd.waitall()

@try_gpu(0)
def test_imagenet_models():
    ctx = mx.context.current_context()
    x = mx.random.uniform(shape=(2, 3, 224, 224), ctx=ctx)
    models = ['resnet18_v1b', 'resnet34_v1b', 'resnet50_v1b',
              'resnet101_v1b', 'resnet152_v1b', 'resnext50_32x4d', 'resnext101_32x4d']
    for model in models:
        net = gcv.model_zoo.get_model(model)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            net.initialize()
        net.collect_params().reset_ctx(ctx)
        net(x)
        mx.nd.waitall()

@try_gpu(0)
def test_ssd_models():
    ctx = mx.context.current_context()
    x = mx.random.uniform(shape=(1, 3, 512, 544), ctx=ctx)  # allow non-squre and larger inputs
    models = ['ssd_300_vgg16_atrous_voc', 'ssd_512_vgg16_atrous_voc', 'ssd_512_resnet50_v1_voc']
    if not mx.context.current_context().device_type == 'gpu':
        models = ['ssd_512_resnet50_v1_voc']
    for model in models:
        net = gcv.model_zoo.get_model(model, ctx=mx.cpu())
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            net.initialize()
        net.collect_params().reset_ctx(ctx)
        net(x)
        mx.nd.waitall()

@try_gpu(0)
def test_segmentation_models():
    ctx = mx.context.current_context()
    x = mx.random.uniform(shape=(2, 3, 480, 480), ctx=ctx)
    models = ['fcn_resnet50_voc', 'fcn_resnet101_voc']
    for model in models:
        net = gcv.model_zoo.get_model(model, ctx=mx.cpu())
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            net.initialize()
        net.collect_params().reset_ctx(ctx)
        net(x)
        mx.nd.waitall()

if __name__ == '__main__':
    import nose
    nose.runmodule()
