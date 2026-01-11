# 🎵 Nucamp - Nuclei Amp

**Nuclei Amp... it really whips the CLI's ass!**

A Winamp/XMMS-inspired terminal UI for the [Nuclei](https://github.com/projectdiscovery/nuclei) vulnerability scanner. Experience vulnerability scanning with that classic late-90s multimedia player aesthetic! 🎸

![Nucamp Banner](https://img.shields.io/badge/Nuclei-Amp-00ff00?style=for-the-badge)

## 🎼 Features

- **Retro Winamp/XMMS-style interface** in your terminal
- **Real-time scan visualization** with live updates
- **Severity-based color coding** (Critical → Info)
- **Equalizer-style statistics display** showing vulnerability breakdown
- **Playlist-like results view** for easy scanning of findings
- **JSON parsing** of Nuclei output for accurate data display

## 📦 Installation

### Prerequisites

1. **Python 3.6+** 
2. **Nuclei** - Install from [ProjectDiscovery](https://github.com/projectdiscovery/nuclei)

### Install Nucamp

```bash
# Clone the repository
git clone https://github.com/storbeck/nucamp.git
cd nucamp

# Run the installer
./install.sh

# Or manually install dependencies
pip3 install -r requirements.txt
```

## 🎮 Usage

### Quick Start

```bash
# See the demo
python3 nucamp.py --demo

# Scan a single URL
python3 nucamp.py -u https://example.com

# Scan with specific templates
python3 nucamp.py -u https://example.com -t cves/

# Scan multiple targets from a file
python3 nucamp.py -l targets.txt

# Use any Nuclei arguments
python3 nucamp.py -u https://example.com -severity critical,high
```

### Arguments

Nucamp accepts all standard Nuclei arguments. Just pass them after `nucamp.py`:

- `-u <URL>` - Target URL
- `-l <file>` - Target list file  
- `-t <templates>` - Template or template directory
- `-severity <level>` - Filter by severity (critical, high, medium, low, info)
- And all other [Nuclei options](https://docs.projectdiscovery.io/tools/nuclei/running)

## 🎨 Interface

```
╔══════════════════════════════════════════════════════════════╗
║          ♪♫ NUCLEI AMP - It really whips the CLI's ass! ♫♪  ║
╚══════════════════════════════════════════════════════════════╝

╔══════════ SCAN RESULTS - example.com ═══════════════════════╗
║ Time     │ Severity  │ Template         │ URL               ║
║──────────┼───────────┼──────────────────┼──────────────────║
║ 10:23:15 │ CRITICAL  │ cve-2024-1234    │ https://...       ║
║ 10:23:18 │ HIGH      │ exposed-panel    │ https://...       ║
╚══════════════════════════════════════════════════════════════╝

╔═ SEVERITY STATS ═╗     ╔═══ CONTROLS ═══╗
║CRITICAL │████     ║     ║ ● Status: Scanning
║HIGH     │██       ║     ╚═════════════════╝
║MEDIUM   │█        ║
║LOW      │█        ║
║INFO     │███      ║
╚═══════════════════╝
```

## 🎯 Why?

Because vulnerability scanning should be fun! Inspired by the classic Winamp tagline "It really whips the llama's ass!", this project brings that same energy to security scanning.

## 🤝 Contributing

Pull requests welcome! Whether it's adding more Winamp-style features, improving the UI, or fixing bugs - all contributions are appreciated.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Credits

- [Nuclei](https://github.com/projectdiscovery/nuclei) by ProjectDiscovery
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Winamp & XMMS for the inspiration

---

*"It really whips the CLI's ass!" 🎵*
