# linkedin-add-ppl

LinkedIn automation script that sends connection requests based on search criteria.

## Features

- Search for people by keyword
- Filter by connection level (1st, 2nd, 3rd+)
- Filter by location
- Filter by current company
- Auto-send connection requests across multiple pages

## Project Structure

```
linkedin-add-ppl/
├── main.py                          # Orchestrator — collects inputs and runs automation
├── requirements.txt                 # Python dependencies
│
├── utils/
│   ├── helpers.py                   # Utility functions (delay, scroll)
│   └── user_input.py               # CLI input collection and validation
│
├── webdrive/
│   └── driver_setup.py             # Chrome WebDriver setup and lifecycle
│
├── search/
│   ├── people_search.py            # LinkedIn keyword search
│   ├── pagination.py               # Page navigation
│   └── filters/
│       ├── connection_level.py     # Connection degree filter
│       ├── location.py             # Location filter
│       └── company.py              # Company filter
│
└── linkedin_connections/
    └── send_connection.py          # Connection request sender
```

## Prerequisites

- Python 3.8+
- Google Chrome installed
- A LinkedIn account (logged in via your Chrome profile)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The script will prompt you for:
1. Chrome profile directory
2. Search term
3. Connection levels (1, 2, 3)
4. Locations
5. Companies
6. Number of pages to navigate

## ⚠️ Disclaimer

This tool is for educational purposes. Use responsibly and in accordance with LinkedIn's Terms of Service.
