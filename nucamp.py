#!/usr/bin/env python3
"""
Nucamp - Nuclei Amp
A Winamp/XMMS-style terminal UI for Nuclei vulnerability scanner
It really whips the CLI's ass!
"""

import sys
import subprocess
import json
import argparse
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.style import Style
from rich import box
from rich.align import Align

class NuCamp:
    """Main application class for Nuclei Amp"""
    
    def __init__(self):
        self.console = Console()
        self.vulnerabilities = []
        self.scan_status = "Stopped"
        self.current_target = ""
        self.stats = {
            "total": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
    def create_title_bar(self):
        """Create Winamp-style title bar"""
        title_text = Text()
        title_text.append("♪♫ ", style="bold cyan")
        title_text.append("NUCLEI AMP", style="bold white on blue")
        title_text.append(" - It really whips the CLI's ass! ", style="bold cyan")
        title_text.append("♫♪", style="bold cyan")
        
        return Panel(
            Align.center(title_text),
            style="bold white on blue",
            box=box.DOUBLE
        )
    
    def create_display_panel(self):
        """Create the main display area (like Winamp's playlist)"""
        table = Table(
            show_header=True,
            header_style="bold cyan on black",
            box=box.SQUARE,
            expand=True,
            style="green on black"
        )
        
        table.add_column("Time", style="cyan", width=8)
        table.add_column("Severity", style="yellow", width=10)
        table.add_column("Template", style="magenta", width=25)
        table.add_column("URL", style="white", overflow="fold")
        
        # Show last 15 vulnerabilities
        for vuln in self.vulnerabilities[-15:]:
            severity_style = self.get_severity_style(vuln['severity'])
            table.add_row(
                vuln['time'],
                Text(vuln['severity'].upper(), style=severity_style),
                vuln['template'],
                vuln['url']
            )
        
        if not self.vulnerabilities:
            table.add_row("--:--", "----", "No vulnerabilities found yet", "---")
        
        return Panel(
            table,
            title=f"[bold cyan]SCAN RESULTS - {self.current_target or 'No target'}[/]",
            style="green on black",
            border_style="cyan",
            box=box.DOUBLE
        )
    
    def create_visualizer(self):
        """Create the equalizer/visualizer area showing stats"""
        viz_text = Text()
        
        # Create a bar chart-like visualization
        viz_text.append("╔═══ SEVERITY STATS ═══╗\n", style="bold cyan")
        
        max_width = 30
        total = self.stats['total'] or 1
        
        severities = [
            ('CRITICAL', self.stats['critical'], 'bold white on red'),
            ('HIGH', self.stats['high'], 'bold black on yellow'),
            ('MEDIUM', self.stats['medium'], 'bold black on orange1'),
            ('LOW', self.stats['low'], 'bold white on blue'),
            ('INFO', self.stats['info'], 'bold black on cyan'),
        ]
        
        for label, count, style in severities:
            bar_length = int((count / total) * max_width) if count > 0 else 0
            bar = "█" * bar_length
            viz_text.append(f"║{label:8s}│", style="cyan")
            viz_text.append(f"{bar:<{max_width}}", style=style)
            viz_text.append(f"║ {count:3d}\n", style="cyan")
        
        viz_text.append("╚═════════════════════╝\n", style="bold cyan")
        viz_text.append(f"\nTotal Found: {self.stats['total']}", style="bold white")
        
        return Panel(
            viz_text,
            title="[bold green]║▌▐│║█═╗[/]",
            style="black on green",
            border_style="bold green",
            box=box.HEAVY
        )
    
    def create_controls(self):
        """Create control panel (like Winamp buttons)"""
        controls_text = Text()
        
        # Status indicator
        status_style = "bold green" if self.scan_status == "Scanning" else "bold red"
        controls_text.append("● ", style=status_style)
        controls_text.append(f"Status: {self.scan_status}", style="bold cyan")
        
        return Panel(
            controls_text,
            title="[bold yellow]CONTROLS[/]",
            style="yellow on black",
            border_style="bold yellow",
            box=box.ROUNDED
        )
    
    def get_severity_style(self, severity):
        """Get Rich style for severity level"""
        severity_map = {
            'critical': 'bold white on red',
            'high': 'bold black on yellow',
            'medium': 'bold black on orange1',
            'low': 'bold white on blue',
            'info': 'bold black on cyan',
        }
        return severity_map.get(severity.lower(), 'white')
    
    def parse_nuclei_output(self, line):
        """Parse JSON output from Nuclei"""
        try:
            data = json.loads(line)
            
            if 'info' in data and 'matched-at' in data:
                severity = data['info'].get('severity', 'info')
                template_id = data['template-id']
                matched_at = data['matched-at']
                
                vuln = {
                    'time': datetime.now().strftime("%H:%M:%S"),
                    'severity': severity,
                    'template': template_id[:23] + "..." if len(template_id) > 23 else template_id,
                    'url': matched_at
                }
                
                self.vulnerabilities.append(vuln)
                self.stats['total'] += 1
                self.stats[severity] = self.stats.get(severity, 0) + 1
                
        except json.JSONDecodeError:
            pass  # Skip non-JSON lines
    
    def create_layout(self):
        """Create the main layout"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="title", size=3),
            Layout(name="main", ratio=2),
            Layout(name="bottom", size=12)
        )
        
        layout["bottom"].split_row(
            Layout(name="visualizer", ratio=1),
            Layout(name="controls", ratio=1)
        )
        
        return layout
    
    def update_layout(self, layout):
        """Update all layout components"""
        layout["title"].update(self.create_title_bar())
        layout["main"].update(self.create_display_panel())
        layout["visualizer"].update(self.create_visualizer())
        layout["controls"].update(self.create_controls())
    
    def run_scan(self, nuclei_args):
        """Run Nuclei scan with live updates"""
        self.scan_status = "Scanning"
        self.current_target = " ".join(nuclei_args)
        
        layout = self.create_layout()
        
        try:
            # Run nuclei with JSON output
            cmd = ["nuclei", "-json"] + nuclei_args
            
            with Live(layout, refresh_per_second=4, console=self.console) as live:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )
                
                # Read output line by line
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        self.parse_nuclei_output(line)
                        self.update_layout(layout)
                
                process.wait()
                self.scan_status = "Completed"
                self.update_layout(layout)
                
                # Show final screen for a moment
                import time
                time.sleep(2)
                
        except FileNotFoundError:
            self.console.print("[bold red]Error: Nuclei not found! Please install it first.[/]")
            self.console.print("Visit: https://github.com/projectdiscovery/nuclei")
            sys.exit(1)
        except KeyboardInterrupt:
            self.scan_status = "Stopped"
            self.console.print("\n[bold yellow]Scan interrupted by user[/]")
        except Exception as e:
            self.console.print(f"[bold red]Error: {e}[/]")
            sys.exit(1)
    
    def show_demo(self):
        """Show demo mode with sample data"""
        self.scan_status = "Demo Mode"
        self.current_target = "example.com"
        
        # Add some sample vulnerabilities
        sample_vulns = [
            {'time': '10:23:15', 'severity': 'critical', 'template': 'cve-2024-1234', 'url': 'https://example.com/admin'},
            {'time': '10:23:18', 'severity': 'high', 'template': 'exposed-panel', 'url': 'https://example.com/panel'},
            {'time': '10:23:22', 'severity': 'medium', 'template': 'ssl-tls-weak', 'url': 'https://example.com'},
            {'time': '10:23:25', 'severity': 'low', 'template': 'robots-txt', 'url': 'https://example.com/robots.txt'},
            {'time': '10:23:30', 'severity': 'info', 'template': 'tech-detect', 'url': 'https://example.com'},
        ]
        
        for vuln in sample_vulns:
            self.vulnerabilities.append(vuln)
            self.stats['total'] += 1
            self.stats[vuln['severity']] += 1
        
        layout = self.create_layout()
        self.update_layout(layout)
        self.console.print(layout)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Nucamp - Nuclei Amp: A Winamp-style UI for Nuclei scanner",
        epilog="It really whips the CLI's ass!"
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Show demo mode with sample data'
    )
    parser.add_argument(
        'nuclei_args',
        nargs='*',
        help='Arguments to pass to nuclei (e.g., -u https://example.com)'
    )
    
    args = parser.parse_args()
    
    app = NuCamp()
    
    if args.demo:
        app.show_demo()
    elif args.nuclei_args:
        app.run_scan(args.nuclei_args)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  nucamp --demo")
        print("  nucamp -u https://example.com")
        print("  nucamp -l targets.txt -t cves/")


if __name__ == "__main__":
    main()
