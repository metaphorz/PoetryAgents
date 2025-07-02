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
            'use_emojis': False
        }
    
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_initialization(self, mock_llm_client, mock_gemini_client):
        """Test DialogueManager initialization."""
        mock_claude = MagicMock()
        mock_gemini = MagicMock()
        mock_llm_client.return_value = mock_claude
        mock_gemini_client.return_value = mock_gemini
        
        manager = DialogueManager()
        
        self.assertEqual(manager.claude_client, mock_claude)
        self.assertEqual(manager.gemini_client, mock_gemini)
        self.assertEqual(manager.agents, [])
        self.assertEqual(manager.conversation_history, [])
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_generate_dialogue_claude_gemini(self, mock_llm_client, mock_gemini_client, mock_get_names):
        """Test dialogue generation with Claude and Gemini."""
        # Setup mocks
        mock_claude = MagicMock()
        mock_gemini = MagicMock()
        mock_llm_client.return_value = mock_claude
        mock_gemini_client.return_value = mock_gemini
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
        self.assertEqual(result['conversation'][0]['llm_used'], 'Claude')
        
        # Check second agent used Gemini
        self.assertEqual(result['conversation'][1]['agent'], 'Gandalf')
        self.assertEqual(result['conversation'][1]['llm_used'], 'Gemini')
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_generate_dialogue_both_claude(self, mock_llm_client, mock_gemini_client, mock_get_names):
        """Test dialogue generation with both agents using Claude."""
        mock_claude = MagicMock()
        mock_gemini = MagicMock()
        mock_llm_client.return_value = mock_claude
        mock_gemini_client.return_value = mock_gemini
        mock_get_names.return_value = ['Agent1', 'Agent2']
        
        mock_claude.generate_poetry.side_effect = [
            'Title',
            'ASCII',
            'Poetry 1',
            'Poetry 2'
        ]
        
        config = self.test_config.copy()
        config['agent1_llm'] = 'Claude'
        config['agent2_llm'] = 'Claude'
        
        manager = DialogueManager()
        result = manager.generate_dialogue(config)
        
        # Both should use Claude
        self.assertEqual(result['conversation'][0]['llm_used'], 'Claude')
        self.assertEqual(result['conversation'][1]['llm_used'], 'Claude')
        
        # Gemini should not be called for poetry
        mock_gemini.generate_poetry.assert_not_called()
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_generate_dialogue_both_gemini(self, mock_llm_client, mock_gemini_client, mock_get_names):
        """Test dialogue generation with both agents using Gemini."""
        mock_claude = MagicMock()
        mock_gemini = MagicMock()
        mock_llm_client.return_value = mock_claude
        mock_gemini_client.return_value = mock_gemini
        mock_get_names.return_value = ['Agent1', 'Agent2']
        
        mock_claude.generate_poetry.side_effect = ['Title', 'ASCII']  # Only title and ASCII
        mock_gemini.generate_poetry.side_effect = ['Poetry 1', 'Poetry 2']
        
        config = self.test_config.copy()
        config['agent1_llm'] = 'Gemini'
        config['agent2_llm'] = 'Gemini'
        
        manager = DialogueManager()
        result = manager.generate_dialogue(config)
        
        # Both should use Gemini
        self.assertEqual(result['conversation'][0]['llm_used'], 'Gemini')
        self.assertEqual(result['conversation'][1]['llm_used'], 'Gemini')
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_generate_dialogue_with_emojis(self, mock_llm_client, mock_gemini_client, mock_get_names):
        """Test dialogue generation with emojis enabled."""
        mock_claude = MagicMock()
        mock_gemini = MagicMock()
        mock_llm_client.return_value = mock_claude
        mock_gemini_client.return_value = mock_gemini
        mock_get_names.return_value = ['Agent1', 'Agent2']
        
        mock_claude.generate_poetry.side_effect = [
            'Title',
            'ASCII',
            'Poetry without emojis',
            'Enhanced poetry 🌸',  # Emoji enhancement
            'Enhanced poetry 2 🌸'  # Emoji enhancement
        ]
        mock_gemini.generate_poetry.return_value = 'Gemini poetry'
        
        config = self.test_config.copy()
        config['use_emojis'] = True
        
        manager = DialogueManager()
        result = manager.generate_dialogue(config)
        
        # Should have called emoji enhancement
        self.assertEqual(mock_claude.generate_poetry.call_count, 5)  # Title, ASCII, poetry, 2 emoji enhancements
    
    @patch('dialogue_manager.get_random_names')
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_generate_dialogue_multiple_rounds(self, mock_llm_client, mock_gemini_client, mock_get_names):
        """Test dialogue generation with multiple conversation rounds."""
        mock_claude = MagicMock()
        mock_gemini = MagicMock()
        mock_llm_client.return_value = mock_claude
        mock_gemini_client.return_value = mock_gemini
        mock_get_names.return_value = ['Agent1', 'Agent2']
        
        mock_claude.generate_poetry.side_effect = [
            'Title',
            'ASCII',
            'Round 1 Agent 1',
            'Round 2 Agent 1'
        ]
        mock_gemini.generate_poetry.side_effect = [
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
    
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_format_dialogue_output(self, mock_llm_client, mock_gemini_client):
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
    
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_generate_ascii_art(self, mock_llm_client, mock_gemini_client):
        """Test ASCII art generation."""
        mock_claude = MagicMock()
        mock_claude.generate_poetry.return_value = '  ASCII art result  '
        mock_llm_client.return_value = mock_claude
        
        manager = DialogueManager()
        result = manager.generate_ascii_art('test theme')
        
        self.assertEqual(result, 'ASCII art result')
        mock_claude.generate_poetry.assert_called_once()
        
        # Check that the prompt contains theme and ASCII instructions
        call_args = mock_claude.generate_poetry.call_args
        prompt = call_args[0][0]
        self.assertIn('test theme', prompt)
        self.assertIn('ASCII art', prompt)
    
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_add_emojis_to_poetry(self, mock_llm_client, mock_gemini_client):
        """Test emoji enhancement."""
        mock_claude = MagicMock()
        mock_claude.generate_poetry.return_value = '  Enhanced poetry 🌸  '
        mock_llm_client.return_value = mock_claude
        
        manager = DialogueManager()
        result = manager.add_emojis_to_poetry('Original poetry', 'flowers')
        
        self.assertEqual(result, 'Enhanced poetry 🌸')
        mock_claude.generate_poetry.assert_called_once()
        
        # Check that the prompt contains original poetry and theme
        call_args = mock_claude.generate_poetry.call_args
        prompt = call_args[0][0]
        self.assertIn('Original poetry', prompt)
        self.assertIn('flowers', prompt)
        self.assertIn('emoji', prompt)
    
    @patch('dialogue_manager.get_character_info')
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_save_dialogue_to_markdown(self, mock_llm_client, mock_gemini_client, mock_get_character_info):
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
    
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_save_dialogue_custom_filename(self, mock_llm_client, mock_gemini_client):
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
    
    @patch('dialogue_manager.GeminiClient')
    @patch('dialogue_manager.LLMClient')
    def test_length_descriptions(self, mock_llm_client, mock_gemini_client):
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