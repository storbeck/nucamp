#!/bin/bash
# Installation script for Nucamp

echo "╔═══════════════════════════════════════╗"
echo "║  Installing Nucamp - Nuclei Amp       ║"
echo "║  It really whips the CLI's ass!       ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

echo "✓ pip3 found"

# Install requirements
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "✓ Installation complete!"
echo ""
echo "Note: Nucamp requires Nuclei to be installed."
echo "If you haven't installed it yet, visit:"
echo "https://github.com/projectdiscovery/nuclei"
echo ""
echo "Usage:"
echo "  python3 nucamp.py --demo              # Show demo"
echo "  python3 nucamp.py -u https://example.com"
echo ""
