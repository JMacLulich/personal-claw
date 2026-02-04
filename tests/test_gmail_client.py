"""Unit tests for Gmail client.

Tests verify Gmail client logic with mocked API calls (no real Gmail connection).
"""
from __future__ import annotations

import unittest
from unittest.mock import MagicMock, Mock, patch

from src.config import Config
from src.gmail_client import GmailClient


class TestGmailClient(unittest.TestCase):
    """Test GmailClient with mocked Gmail API."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create mock config
        self.config = Mock(spec=Config)
        self.config.gmail_credentials_path = "fake_credentials.json"
        self.config.gmail_token_path = "fake_token.json"
        
        # Patch TokenManager to avoid real OAuth
        self.token_manager_patch = patch('src.gmail_client.TokenManager')
        self.mock_token_manager_class = self.token_manager_patch.start()
        self.mock_token_manager = self.mock_token_manager_class.return_value
        
        # Mock credentials
        self.mock_creds = Mock()
        self.mock_token_manager.get_credentials.return_value = self.mock_creds
        
        # Patch Gmail service builder
        self.build_patch = patch('src.gmail_client.build')
        self.mock_build = self.build_patch.start()
        self.mock_service = MagicMock()
        self.mock_build.return_value = self.mock_service
    
    def tearDown(self) -> None:
        """Clean up patches."""
        self.token_manager_patch.stop()
        self.build_patch.stop()
    
    def test_init(self) -> None:
        """Test GmailClient initialization."""
        GmailClient(self.config)
        
        # Should create TokenManager with correct paths
        self.mock_token_manager_class.assert_called_once_with(
            credentials_path=self.config.gmail_credentials_path,
            token_path=self.config.gmail_token_path
        )
        
        # Service should not be built yet (lazy connection)
        self.mock_build.assert_not_called()
    
    def test_ensure_connected_creates_service(self) -> None:
        """Test that _ensure_connected creates Gmail service."""
        client = GmailClient(self.config)
        
        # Trigger connection
        client._ensure_connected()
        
        # Should get credentials and build service
        self.mock_token_manager.get_credentials.assert_called_once()
        self.mock_build.assert_called_once_with('gmail', 'v1', credentials=self.mock_creds)
    
    def test_ensure_connected_reuses_service(self) -> None:
        """Test that _ensure_connected doesn't rebuild if already connected."""
        client = GmailClient(self.config)
        
        # Connect twice
        client._ensure_connected()
        client._ensure_connected()
        
        # Should only build service once
        self.mock_build.assert_called_once()
    
    def test_list_messages(self) -> None:
        """Test list_messages calls Gmail API correctly."""
        client = GmailClient(self.config)
        
        # Mock API response
        self.mock_service.users().messages().list().execute.return_value = {
            'messages': [
                {'id': 'msg1', 'threadId': 'thread1'},
                {'id': 'msg2', 'threadId': 'thread2'}
            ]
        }
        
        # Call list_messages
        messages = client.list_messages(max_results=10, query='is:unread')
        
        # Verify API was called with correct parameters
        # Note: Check the actual call, not call count (mock chains can be tricky)
        calls = self.mock_service.users().messages().list.call_args_list
        self.assertTrue(any(
            call[1] == {'userId': 'me', 'maxResults': 10, 'q': 'is:unread'}
            for call in calls
        ))
        
        # Verify result
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['id'], 'msg1')
    
    def test_list_messages_empty(self) -> None:
        """Test list_messages with no messages."""
        client = GmailClient(self.config)
        
        # Mock empty response
        self.mock_service.users().messages().list().execute.return_value = {}
        
        messages = client.list_messages()
        
        # Should return empty list
        self.assertEqual(messages, [])
    
    def test_get_message(self) -> None:
        """Test get_message calls Gmail API correctly."""
        client = GmailClient(self.config)
        
        # Mock API response
        mock_message = {
            'id': 'msg1',
            'threadId': 'thread1',
            'payload': {'headers': [], 'body': {'data': 'test'}}
        }
        self.mock_service.users().messages().get().execute.return_value = mock_message
        
        # Call get_message
        message = client.get_message('msg1', format='full')
        
        # Verify API was called with correct parameters
        calls = self.mock_service.users().messages().get.call_args_list
        self.assertTrue(any(
            call[1] == {'userId': 'me', 'id': 'msg1', 'format': 'full'}
            for call in calls
        ))
        
        # Verify result
        self.assertEqual(message['id'], 'msg1')
    
    def test_get_inbox_summary(self) -> None:
        """Test get_inbox_summary returns correct structure."""
        client = GmailClient(self.config)
        
        # Mock list_messages response
        self.mock_service.users().messages().list().execute.return_value = {
            'messages': [{'id': 'msg1', 'threadId': 'thread1'}]
        }
        
        # Mock get_message response
        self.mock_service.users().messages().get().execute.return_value = {
            'id': 'msg1',
            'payload': {
                'headers': [
                    {'name': 'Subject', 'value': 'Test Email'},
                    {'name': 'From', 'value': 'sender@example.com'}
                ]
            }
        }
        
        # Call get_inbox_summary
        summary = client.get_inbox_summary()
        
        # Verify structure
        self.assertEqual(summary['message_count'], 1)
        self.assertEqual(len(summary['messages']), 1)
        self.assertEqual(summary['messages'][0]['subject'], 'Test Email')
        self.assertEqual(summary['messages'][0]['from'], 'sender@example.com')


if __name__ == '__main__':
    unittest.main()
