import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add root folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core import configure_client
import src.agent as agent

class TestFormAgentCore(unittest.TestCase):
    
    @patch.dict(os.environ, {}, clear=True)
    def test_configure_client_missing_key(self):
        """Test that configure_client raises ValueError when key is missing and not in env."""
        with self.assertRaises(ValueError):
            configure_client(api_key=None)
            
    @patch('google.generativeai.configure')
    def test_configure_client_with_arg_key(self, mock_configure):
        """Test configure_client with an explicit key argument."""
        configure_client(api_key="TEST_KEY_ABC")
        mock_configure.assert_called_once_with(api_key="TEST_KEY_ABC")
        
    @patch.dict(os.environ, {"GEMINI_API_KEY": "ENV_KEY_XYZ"})
    @patch('google.generativeai.configure')
    def test_configure_client_with_env_key(self, mock_configure):
        """Test configure_client with key fetched from env variables."""
        configure_client(api_key=None)
        mock_configure.assert_called_once_with(api_key="ENV_KEY_XYZ")

class TestFormAgentCLI(unittest.TestCase):
    
    @patch('src.agent.extract_structured_data')
    @patch('sys.argv', ['agent.py', 'extract', 'non_existent_file.png'])
    def test_cli_file_not_found(self, mock_extract):
        """Test that CLI exits when the specified file does not exist."""
        # Since 'non_existent_file.png' doesn't exist, parser should exit with code 1
        with self.assertRaises(SystemExit) as cm:
            agent.main()
        self.assertEqual(cm.exception.code, 1)

    @patch('src.agent.extract_structured_data')
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['agent.py', 'extract', 'dummy_file.png', '--key', 'KEY123'])
    def test_cli_extract_success(self, mock_exists, mock_extract):
        """Test that extract command calls core extract function with correct arguments."""
        mock_extract.return_value = {"status": "success"}
        with patch('builtins.print') as mock_print:
            agent.main()
            mock_extract.assert_called_once_with('dummy_file.png', api_key='KEY123')
            # Verify printed JSON output contains expected data
            mock_print.assert_called_once()
            args, _ = mock_print.call_args
            self.assertIn("success", args[0])

    @patch('src.agent.ask_question')
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['agent.py', 'ask', 'dummy_file.png', 'What is the date?', '--key', 'KEY456'])
    def test_cli_ask_success(self, mock_exists, mock_ask):
        """Test that ask command calls core ask function with correct arguments."""
        mock_ask.return_value = "Answer Text"
        with patch('builtins.print') as mock_print:
            agent.main()
            mock_ask.assert_called_once_with('dummy_file.png', 'What is the date?', api_key='KEY456')
            mock_print.assert_called_once_with("Answer Text")

if __name__ == '__main__':
    unittest.main()
