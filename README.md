🕵️ Rapid Recon
Rapid Recon is a Python-based reconnaissance and information-gathering tool built for cybersecurity professionals, ethical hackers, bug bounty hunters, and SOC analysts.

It automates intelligence-gathering tasks such as DNS lookups, GeoIP tracking, WHOIS analysis, port scanning, HTTP fingerprinting, and technology stack detection — delivering structured outputs for quick analysis and decision-making.

---

## 🔧 Features

- 🔎 **DNS Lookup**: Retrieve DNS records including subdomains, MX (mail) records, NS (name servers), and more.
- 🌍 **GeoIP Lookup**: Determine the geographical location of an IP address using external APIs.
- 🌐 **HTTP Info**:Fetch HTTP response headers, status codes, server details, and more.
- 🕵️ **WHOIS Lookup**: Access domain registration details, expiration dates, and ownership records.
- 🚪 **Port Scanning**: Scan for open TCP ports using efficient socket-based scanning.
- 💻 **Technology Stack Detection**: Identify frontend and backend technologies used by the target site.
- 📤 **Export to JSON**: Save all gathered data in structured JSON format for future analysis.
- 📝 **Report Generator**: Generate a readable, summarized report of all findings.
- ✅ **Input Validation**: Clean and validate user input (IP/domain) before processing.

---

## 🚀 Getting Started

### Prerequisites and .env Configuration

- Python 3.8+
- Internet connection (for external lookups)
- Recommended: Virtual environment
- Within .env file : IPINFO_TOKEN=your_token

---

### Install Dependencies and Usage

```bash
pip install -r requirements.txt
python recon.py --help
python recon.py --all example.com
