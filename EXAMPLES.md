# Examples

## Demo Mode

Run the demo to see Nucamp in action without needing to install Nuclei:

```bash
python3 nucamp.py --demo
```

## Real Scanning Examples

### Single Target
```bash
python3 nucamp.py -u https://example.com
```

### Multiple Targets
```bash
# Create a targets file
echo "https://example.com" > targets.txt
echo "https://test.com" >> targets.txt

python3 nucamp.py -l targets.txt
```

### With Specific Templates
```bash
python3 nucamp.py -u https://example.com -t cves/
```

### Filter by Severity
```bash
python3 nucamp.py -u https://example.com -severity critical,high
```

### Advanced Usage
```bash
# Use rate limiting
python3 nucamp.py -u https://example.com -rate-limit 10

# Use specific tags
python3 nucamp.py -u https://example.com -tags xss,sqli

# Exclude specific templates
python3 nucamp.py -u https://example.com -exclude-templates dns/
```

## Output Explanation

The Nucamp interface has four main areas:

1. **Title Bar**: Shows the application name and tagline
2. **Scan Results Panel**: Displays vulnerabilities as they're found (like a playlist)
   - Time: When the vulnerability was detected
   - Severity: Importance level (Critical → Info)
   - Template: The Nuclei template that detected it
   - URL: Where the vulnerability was found

3. **Severity Stats (Visualizer)**: Bar chart showing vulnerability breakdown
   - Visual representation of findings by severity
   - Total count display

4. **Controls**: Shows current scan status
   - Scanning: Active scan in progress
   - Completed: Scan finished
   - Stopped: Scan interrupted
   - Demo Mode: Running demo data
