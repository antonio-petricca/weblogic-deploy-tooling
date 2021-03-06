"""
Copyright (c) 2017, 2018, Oracle and/or its affiliates. All rights reserved.
The Universal Permissive License (UPL), Version 1.0
"""
import unittest

from wlsdeploy.aliases.alias_jvmargs import JVMArguments
from wlsdeploy.logging.platform_logger import PlatformLogger

class JVMArgumentsTestCase(unittest.TestCase):

    _logger = PlatformLogger('wlsdeploy.aliases')

    def testArgParsing(self):
        input = '-XX:MaxPermSize=512m -verify:none -XX:+HeapDumpOnOutOfMemoryError -Xms1024m -Dfoo=bar -Xmx2g -server -dsa -verbose:gc -Xrs'
        expected = '-server -Xms1024m -Xmx2g -Xrs -XX:+HeapDumpOnOutOfMemoryError -XX:MaxPermSize=512m -Dfoo=bar -verify:none -dsa -verbose:gc'

        args = JVMArguments(self._logger, input)
        actual = args.get_arguments_string()
        self.assertEqual(actual, expected)

    def testArgMerging(self):
        existing = '-XX:MaxPermSize=512m -verify:none -XX:+HeapDumpOnOutOfMemoryError -Xms1024m -Dfoo=bar -Xmx2g -server -dsa -verbose:gc -Xrs'
        model = '-Dmodel=testme -Xmx4096m -client'
        expected = '-client -Xms1024m -Xmx4096m -Xrs -XX:+HeapDumpOnOutOfMemoryError -XX:MaxPermSize=512m -Dfoo=bar -Dmodel=testme -verify:none -dsa -verbose:gc'

        existing_args = JVMArguments(self._logger, existing)
        model_args = JVMArguments(self._logger, model)
        existing_args.merge_jvm_arguments(model_args)
        actual = existing_args.get_arguments_string()
        self.assertEqual(actual, expected)
