#!/usr/bin/env python3
"""
Tests for Nucamp
"""

import unittest
import json
from nucamp import NuCamp


class TestNucamp(unittest.TestCase):
    """Test cases for Nucamp application"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = NuCamp()
    
    def test_initialization(self):
        """Test app initializes with correct defaults"""
        self.assertEqual(self.app.scan_status, "Stopped")
        self.assertEqual(self.app.current_target, "")
        self.assertEqual(len(self.app.vulnerabilities), 0)
        self.assertEqual(self.app.stats['total'], 0)
    
    def test_severity_style(self):
        """Test severity styling mapping"""
        self.assertEqual(self.app.get_severity_style('critical'), 'bold white on red')
        self.assertEqual(self.app.get_severity_style('high'), 'bold black on yellow')
        self.assertEqual(self.app.get_severity_style('medium'), 'bold black on orange1')
        self.assertEqual(self.app.get_severity_style('low'), 'bold white on blue')
        self.assertEqual(self.app.get_severity_style('info'), 'bold black on cyan')
        self.assertEqual(self.app.get_severity_style('unknown'), 'white')
    
    def test_parse_nuclei_output(self):
        """Test parsing Nuclei JSON output"""
        # Sample Nuclei JSON output
        sample_json = {
            "template-id": "test-template",
            "info": {
                "name": "Test Template",
                "severity": "high"
            },
            "matched-at": "https://example.com/test"
        }
        
        json_line = json.dumps(sample_json)
        self.app.parse_nuclei_output(json_line)
        
        self.assertEqual(len(self.app.vulnerabilities), 1)
        self.assertEqual(self.app.stats['total'], 1)
        self.assertEqual(self.app.stats['high'], 1)
        self.assertEqual(self.app.vulnerabilities[0]['severity'], 'high')
        self.assertEqual(self.app.vulnerabilities[0]['template'], 'test-template')
    
    def test_parse_multiple_vulnerabilities(self):
        """Test parsing multiple vulnerabilities"""
        vulns = [
            {"template-id": "vuln1", "info": {"severity": "critical"}, "matched-at": "https://test1.com"},
            {"template-id": "vuln2", "info": {"severity": "high"}, "matched-at": "https://test2.com"},
            {"template-id": "vuln3", "info": {"severity": "medium"}, "matched-at": "https://test3.com"},
        ]
        
        for vuln in vulns:
            self.app.parse_nuclei_output(json.dumps(vuln))
        
        self.assertEqual(len(self.app.vulnerabilities), 3)
        self.assertEqual(self.app.stats['total'], 3)
        self.assertEqual(self.app.stats['critical'], 1)
        self.assertEqual(self.app.stats['high'], 1)
        self.assertEqual(self.app.stats['medium'], 1)
    
    def test_parse_invalid_json(self):
        """Test handling of invalid JSON"""
        initial_count = len(self.app.vulnerabilities)
        self.app.parse_nuclei_output("This is not JSON")
        # Should not crash and should not add vulnerability
        self.assertEqual(len(self.app.vulnerabilities), initial_count)
    
    def test_ui_components_creation(self):
        """Test that UI components can be created without errors"""
        # These should not raise exceptions
        title = self.app.create_title_bar()
        display = self.app.create_display_panel()
        visualizer = self.app.create_visualizer()
        controls = self.app.create_controls()
        
        self.assertIsNotNone(title)
        self.assertIsNotNone(display)
        self.assertIsNotNone(visualizer)
        self.assertIsNotNone(controls)
    
    def test_layout_creation(self):
        """Test layout creation"""
        layout = self.app.create_layout()
        self.assertIsNotNone(layout)
        
        # Check that layout has expected sections by name
        try:
            title = layout["title"]
            main = layout["main"]
            bottom = layout["bottom"]
            self.assertIsNotNone(title)
            self.assertIsNotNone(main)
            self.assertIsNotNone(bottom)
        except KeyError:
            self.fail("Layout should have title, main, and bottom sections")


if __name__ == '__main__':
    unittest.main()
