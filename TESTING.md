# Website Feature Testing Scripts

This repository contains comprehensive testing scripts for the Südwest-Energie website.

## Files

- `test_website_http.py` - HTTP-based testing script (no browser required)
- `test_website_features.py` - Full browser-based testing script (requires Selenium)
- `test_results.json` - Output file for browser-based tests
- `http_test_results.json` - Output file for HTTP-based tests

## Installation

Before running the tests, make sure you have the required dependencies:

```bash
cd /home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt
source .venv/bin/activate
pip install selenium webdriver-manager
```

## Usage

### HTTP-based Testing (Recommended)

This tests the website functionality without requiring a browser:

```bash
cd /home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt
source .venv/bin/activate
python test_website_http.py
```

### Full Browser Testing

This tests the website with a full browser simulation:

```bash
cd /home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt
source .venv/bin/activate
python test_website_features.py
```

**Note:** The browser testing requires Chrome to be installed on your system.

## Features Tested

Both scripts test the following website features:

- Logo visibility and accessibility
- Page loading and navigation
- Contact form fields and submission
- Static asset accessibility
- Response times
- Footer and header elements
- Ninox database integration configuration
- Thank you page functionality
- Impressum and Datenschutz pages

## Ninox Integration Testing

The scripts specifically test the Ninox integration by:

- Verifying environment configuration
- Testing database client initialization
- Validating contact form data flow

## Output

Test results are saved to JSON files for further analysis:
- Browser tests: `test_results.json`
- HTTP tests: `http_test_results.json`

## Prerequisites

- The website must be running at http://localhost:3000 (start with `reflex run`)
- For Ninox integration tests, ensure environment variables are set:
  - `NINOX_API_KEY`
  - `NINOX_DATABASE_ID`
  - `NINOX_TABLE_ID`