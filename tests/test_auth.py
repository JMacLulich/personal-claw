"""Tests for user authentication and authorization."""

from unittest.mock import MagicMock, patch

import pytest

from src.auth import check_allowlisted_user


class TestCheckAllowlistedUser:
    """Test suite for check_allowlisted_user function."""
    
    @patch('src.auth.load_config')
    def test_authorized_user_returns_true(self, mock_load_config):
        """Test that allowlisted user ID returns True."""
        # Arrange: Set up mock config with allowlisted user ID
        mock_config = MagicMock()
        mock_config.discord_allowlisted_user_id = 123456789
        mock_load_config.return_value = mock_config
        
        # Mock Discord context with matching user ID
        mock_ctx = MagicMock()
        mock_ctx.author.id = 123456789  # Matches allowlisted ID
        
        # Act: Check if user is authorized
        result = check_allowlisted_user(mock_ctx)
        
        # Assert: Should return True for allowlisted user
        assert result is True
    
    @patch('src.auth.load_config')
    def test_unauthorized_user_returns_false(self, mock_load_config):
        """Test that non-allowlisted user ID returns False."""
        # Arrange: Set up mock config with allowlisted user ID
        mock_config = MagicMock()
        mock_config.discord_allowlisted_user_id = 123456789
        mock_load_config.return_value = mock_config
        
        # Mock Discord context with different user ID
        mock_ctx = MagicMock()
        mock_ctx.author.id = 987654321  # Does NOT match allowlisted ID
        
        # Act: Check if user is authorized
        result = check_allowlisted_user(mock_ctx)
        
        # Assert: Should return False for non-allowlisted user
        assert result is False
    
    @patch('src.auth.load_config')
    def test_multiple_unauthorized_users_all_rejected(self, mock_load_config):
        """Test that various unauthorized user IDs are all rejected."""
        # Arrange: Set up mock config
        mock_config = MagicMock()
        mock_config.discord_allowlisted_user_id = 123456789
        mock_load_config.return_value = mock_config
        
        # Test multiple different unauthorized user IDs
        unauthorized_ids = [111111111, 222222222, 333333333, 999999999]
        
        for user_id in unauthorized_ids:
            mock_ctx = MagicMock()
            mock_ctx.author.id = user_id
            
            # Act & Assert: Each should be rejected
            assert check_allowlisted_user(mock_ctx) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
