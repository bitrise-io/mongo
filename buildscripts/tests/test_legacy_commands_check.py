"""Unit tests for legacy_commmands_check.py"""

import textwrap
import unittest
from typing import Iterable

from buildscripts.legacy_commands_check import check_file_for_legacy_type


def create_file_iterator(file_contents: str) -> Iterable[str]:
    return textwrap.dedent(file_contents.strip()).splitlines()


class TestCheckFileForLegacyType(unittest.TestCase):
    def test_typed_command(self):
        content = """ 
        line 0
        class AddShardCmd : public TypedCommand
        """
        self.assertEqual(check_file_for_legacy_type(create_file_iterator(content)), False)

    def test_command(self):
        content = """ 
        line 0
        class AddShardCmd : public Command
        """
        self.assertEqual(check_file_for_legacy_type(create_file_iterator(content)), True)

    def test_basic_command(self):
        content = """ 
        line 0
        class AddShardCmd : public BasicCommand
        """
        self.assertEqual(check_file_for_legacy_type(create_file_iterator(content)), True)

    def test_basic_command_with_reply_builder_interface(self):
        content = """ 
        line 0
        class AddShardCmd : public BasicCommandWithReplyBuilderInterface
        """
        self.assertEqual(check_file_for_legacy_type(create_file_iterator(content)), True)

    def test_basic_command_with_request_parser(self):
        content = """ 
        line 0
        class AddShardCmd : public BasicCommandWithRequestParser
        """
        self.assertEqual(check_file_for_legacy_type(create_file_iterator(content)), True)

    def test_errmsg_command(self):
        content = """ 
        line 0
        class AddShardCmd : public ErrmsgCommandDeprecated
        """
        self.assertEqual(check_file_for_legacy_type(create_file_iterator(content)), True)

    def test_kCommand(self):
        # This log statement appears in many Command files for logging purposes and should not be
        # mistaken for a Command type

        content = """ 
        line 0
        #define MONGO_LOGV2_DEFAULT_COMPONENT ::mongo::logv2::LogComponent::kCommand
        """
        self.assertEqual(check_file_for_legacy_type(create_file_iterator(content)), False)
