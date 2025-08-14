"""
Comprehensive unit tests with coverage for dialogue_manager.py
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dialogue_manager import DialogueManager
from llm_factory import LLMClientFactory


class TestDialogueManager(unittest.TestCase):
    """Test DialogueManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_config = {
            'theme': 'test theme',
            'num_agents': 2,
            'form': 'haiku',
            'poem_length': 3,
            'length_unit': 'lines',
            'conversation_length': 1,
            'agent1_llm': 'Claude',
            'agent2_llm': 'Gemini',
            'agent1_claude_model': 'Claude Sonnet 4',
            'agent1_gemini_model': None,
            'agent2_claude_model': None,
            'agent2_gemini_model': 'Gemini 2.5 Pro',
            'use_emojis': False
        }
    
    def test_initialization(self):
        """Test DialogueManager initialization."""
        manager = DialogueManager()
        
        # New interface initializes clients to None initially
        self.assertIsNone(manager.claude_client)
        self.assertIsNone(manager.gemini_client)
        self.assertEqual(manager.agents, [])
        self.assertEqual(manager.conversation_history, [])
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.LLMClientFactory')
    def test_generate_dialogue_claude_gemini(self, mock_factory, mock_get_names):
        """Test dialogue generation with Claude and Gemini."""
        # Setup mocks
        mock_claude = MagicMock()
        mock_gemini = MagicMock()
        mock_factory.create_client.side_effect = [mock_claude, mock_gemini]
        mock_get_names.return_value = ['Elizabeth', 'Gandalf']
        
        mock_claude.generate_poetry.side_effect = [
            'Test Title',  # Title generation
            'ASCII art here',  # ASCII art generation
            'Claude poetry line 1\nLine 2\nLine 3'  # Poetry generation
        ]
        mock_gemini.generate_poetry.return_value = 'Gemini poetry line 1\nLine 2\nLine 3'
        
        manager = DialogueManager()
        result = manager.generate_dialogue(self.test_config)
        
        # Check structure
        self.assertIn('title', result)
        self.assertIn('ascii_art', result)
        self.assertIn('agents', result)
        self.assertIn('conversation', result)
        self.assertIn('config', result)
        
        # Check content
        self.assertEqual(result['title'], 'Test Title')
        self.assertEqual(result['ascii_art'], 'ASCII art here')
        self.assertEqual(result['agents'], ['Elizabeth', 'Gandalf'])
        self.assertEqual(len(result['conversation']), 2)
        
        # Check first agent used Claude
        self.assertEqual(result['conversation'][0]['agent'], 'Elizabeth')
        self.assertIn('llm_used', result['conversation'][0])
        
        # Check second agent used Gemini
        self.assertEqual(result['conversation'][1]['agent'], 'Gandalf')
        self.assertIn('llm_used', result['conversation'][1])
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.LLMClientFactory')
    def test_generate_dialogue_both_claude(self, mock_factory, mock_get_names):
        """Test dialogue generation with both agents using Claude."""
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()
        mock_factory.create_client.side_effect = [mock_client1, mock_client2]
        mock_get_names.return_value = ['Agent1', 'Agent2']
        
        mock_client1.generate_poetry.side_effect = [
            'Title',
            'ASCII',
            'Poetry 1'
        ]
        mock_client2.generate_poetry.return_value = 'Poetry 2'
        
        config = self.test_config.copy()
        config['agent1_llm'] = 'Claude'
        config['agent2_llm'] = 'Claude'
        
        manager = DialogueManager()
        result = manager.generate_dialogue(config)
        
        # Both should use created clients
        self.assertIn('llm_used', result['conversation'][0])
        self.assertIn('llm_used', result['conversation'][1])
        
        # Factory should have been called twice
        self.assertEqual(mock_factory.create_client.call_count, 2)
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.LLMClientFactory')
    def test_generate_dialogue_both_gemini(self, mock_factory, mock_get_names):
        """Test dialogue generation with both agents using Gemini."""
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()
        mock_factory.create_client.side_effect = [mock_client1, mock_client2]
        mock_get_names.return_value = ['Agent1', 'Agent2']
        
        mock_client1.generate_poetry.side_effect = ['Title', 'ASCII', 'Poetry 1']
        mock_client2.generate_poetry.return_value = 'Poetry 2'
        
        config = self.test_config.copy()
        config['agent1_llm'] = 'Gemini'
        config['agent2_llm'] = 'Gemini'
        
        manager = DialogueManager()
        result = manager.generate_dialogue(config)
        
        # Both should use created clients
        self.assertIn('llm_used', result['conversation'][0])
        self.assertIn('llm_used', result['conversation'][1])
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.LLMClientFactory')
    @patch('dialogue_manager.EnhancementService')
    def test_generate_dialogue_with_emojis(self, mock_enhancement_service, mock_factory, mock_get_names):
        """Test dialogue generation with emojis enabled."""
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()
        mock_factory.create_client.side_effect = [mock_client1, mock_client2]
        mock_get_names.return_value = ['Agent1', 'Agent2']
        
        mock_enhancement = MagicMock()
        mock_enhancement_service.return_value = mock_enhancement
        mock_enhancement.add_emojis_to_poetry.return_value = 'Enhanced poetry 🌸'
        
        mock_client1.generate_poetry.side_effect = [
            'Title',
            'ASCII',
            'Poetry without emojis'
        ]
        mock_client2.generate_poetry.return_value = 'Gemini poetry'
        
        config = self.test_config.copy()
        config['use_emojis'] = True
        
        manager = DialogueManager()
        result = manager.generate_dialogue(config)
        
        # Should have called emoji enhancement
        self.assertEqual(mock_enhancement.add_emojis_to_poetry.call_count, 2)
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.LLMClientFactory')
    def test_generate_dialogue_multiple_rounds(self, mock_factory, mock_get_names):
        """Test dialogue generation with multiple conversation rounds."""
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()
        mock_factory.create_client.side_effect = [mock_client1, mock_client2]
        mock_get_names.return_value = ['Agent1', 'Agent2']
        
        mock_client1.generate_poetry.side_effect = [
            'Title',
            'ASCII',
            'Round 1 Agent 1',
            'Round 2 Agent 1'
        ]
        mock_client2.generate_poetry.side_effect = [
            'Round 1 Agent 2',
            'Round 2 Agent 2'
        ]
        
        config = self.test_config.copy()
        config['conversation_length'] = 2
        
        manager = DialogueManager()
        result = manager.generate_dialogue(config)
        
        # Should have 4 total poems (2 rounds × 2 agents)
        self.assertEqual(len(result['conversation']), 4)
        
        # Check round numbers
        self.assertEqual(result['conversation'][0]['round'], 1)
        self.assertEqual(result['conversation'][1]['round'], 1)
        self.assertEqual(result['conversation'][2]['round'], 2)
        self.assertEqual(result['conversation'][3]['round'], 2)
    
    def test_format_dialogue_output(self):
        """Test dialogue output formatting."""
        manager = DialogueManager()
        
        test_dialogue = {
            'title': 'Test Title',
            'conversation': [
                {
                    'agent': 'Agent1',
                    'poetry': 'Line 1\nLine 2\nLine 3',
                    'round': 1,
                    'agent_index': 0
                },
                {
                    'agent': 'Agent2',
                    'poetry': 'Response line 1\nResponse line 2',
                    'round': 1,
                    'agent_index': 1
                }
            ]
        }
        
        output = manager.format_dialogue_output(test_dialogue)
        
        self.assertIsInstance(output, str)
        self.assertIn('# Test Title', output)
        self.assertIn('**Agent1:**', output)
        self.assertIn('**Agent2:**', output)
        self.assertIn('Line 1', output)
        self.assertIn('Response line 1', output)
    
    @patch('dialogue_manager.EnhancementService')
    def test_generate_ascii_art(self, mock_enhancement_service):
        """Test ASCII art generation."""
        mock_enhancement = MagicMock()
        mock_enhancement.generate_ascii_art.return_value = 'ASCII art result'
        mock_enhancement_service.return_value = mock_enhancement
        
        manager = DialogueManager()
        result = manager.generate_ascii_art('test theme')
        
        self.assertEqual(result, 'ASCII art result')
        mock_enhancement.generate_ascii_art.assert_called_once_with('test theme')
    
    @patch('dialogue_manager.EnhancementService')
    def test_add_emojis_to_poetry(self, mock_enhancement_service):
        """Test emoji enhancement."""
        mock_enhancement = MagicMock()
        mock_enhancement.add_emojis_to_poetry.return_value = 'Enhanced poetry 🌸'
        mock_enhancement_service.return_value = mock_enhancement
        
        manager = DialogueManager()
        result = manager.add_emojis_to_poetry('Original poetry', 'flowers')
        
        self.assertEqual(result, 'Enhanced poetry 🌸')
        mock_enhancement.add_emojis_to_poetry.assert_called_once_with('Original poetry', 'flowers')
    
    @patch('dialogue_manager.get_character_info')
    def test_save_dialogue_to_markdown(self, mock_get_character_info):
        """Test saving dialogue to markdown file."""
        mock_get_character_info.return_value = {
            'source': 'Test Literature',
            'qualities': 'Test qualities'
        }
        
        # Create temporary directory for test
        with tempfile.TemporaryDirectory() as temp_dir:
            outputs_dir = os.path.join(temp_dir, 'outputs')
            os.makedirs(outputs_dir, exist_ok=True)
            
            manager = DialogueManager()
            
            test_dialogue = {
                'title': 'Test Dialogue',
                'ascii_art': 'ASCII\nArt',
                'agents': ['Agent1', 'Agent2'],
                'conversation': [
                    {
                        'agent': 'Agent1',
                        'poetry': 'Poetry line 1\nPoetry line 2',
                        'llm_used': 'Claude'
                    }
                ],
                'config': {
                    'theme': 'test',
                    'num_agents': 2,
                    'form': 'haiku',
                    'poem_length': 3,
                    'length_unit': 'lines',
                    'conversation_length': 1,
                    'use_emojis': False
                }
            }
            
            # Patch os.makedirs to use our temp directory
            with patch('dialogue_manager.os.makedirs'):
                with patch('builtins.open', mock_open()) as mock_file:
                    filename = manager.save_dialogue_to_markdown(test_dialogue)
            
            # Check filename format
            self.assertTrue(filename.startswith('outputs/poetry_dialogue_'))
            self.assertTrue(filename.endswith('.md'))
            
            # Check that file was written
            mock_file.assert_called_once()
            
            # Check some content was written
            handle = mock_file()
            handle.write.assert_called()
            written_content = ''.join(call.args[0] for call in handle.write.call_args_list)
            self.assertIn('# Test Dialogue', written_content)
            self.assertIn('Agent1', written_content)
    
    def test_save_dialogue_custom_filename(self):
        """Test saving dialogue with custom filename."""
        manager = DialogueManager()
        
        test_dialogue = {
            'title': 'Test',
            'agents': ['Agent1'],
            'conversation': [],
            'config': {
                'theme': 'test theme',
                'num_agents': 1,
                'form': 'haiku',
                'poem_length': 3,
                'length_unit': 'lines',
                'conversation_length': 1,
                'use_emojis': False
            }
        }
        
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('dialogue_manager.get_character_info', return_value={'source': 'Test', 'qualities': 'Test'}):
                filename = manager.save_dialogue_to_markdown(test_dialogue, 'custom_file.md')
        
        self.assertEqual(filename, 'custom_file.md')
        mock_file.assert_called_with('custom_file.md', 'w', encoding='utf-8')
    
    def test_length_descriptions(self):
        """Test length descriptions for different units."""
        manager = DialogueManager()
        
        test_cases = [
            ({'poem_length': 3, 'length_unit': 'lines', 'form': 'haiku'}, '3 lines (traditional haiku)'),
            ({'poem_length': 4, 'length_unit': 'stanzas', 'form': 'ballad'}, '4 stanzas'),
            ({'poem_length': 1, 'length_unit': 'stanzas', 'form': 'ballad'}, '1 stanza'),
            ({'poem_length': 7, 'length_unit': 'couplets', 'form': 'ghazal'}, '7 couplets'),
            ({'poem_length': 1, 'length_unit': 'couplets', 'form': 'ghazal'}, '1 couplet'),
            ({'poem_length': 3, 'length_unit': 'paragraphs', 'form': 'prose'}, '3 paragraphs'),
            ({'poem_length': 1, 'length_unit': 'paragraphs', 'form': 'prose'}, '1 paragraph'),
        ]
        
        for config_updates, expected_desc in test_cases:
            with self.subTest(config=config_updates):
                test_dialogue = {
                    'title': 'Test',
                    'agents': ['Agent1'],
                    'conversation': [],
                    'config': {**self.test_config, **config_updates}
                }
                
                with patch('builtins.open', mock_open()) as mock_file:
                    with patch('dialogue_manager.get_character_info', return_value={'source': 'Test', 'qualities': 'Test'}):
                        manager.save_dialogue_to_markdown(test_dialogue)
                
                # Check that expected description appears in written content
                handle = mock_file()
                written_content = ''.join(call.args[0] for call in handle.write.call_args_list)
                self.assertIn(expected_desc, written_content)


if __name__ == '__main__':
    unittest.main()