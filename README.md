# Way-Secure

## Description

This Python script extracts archived file links from the Wayback Machine for a given domain, categorizes them by file type, and saves them into organized text files. It also identifies and extracts links containing emails and sensitive keywords.

## Features

- Fetches archived URLs from the Wayback Machine
- Removes duplicate URLs
- Categorizes links by file extension
- Extracts email-related links into a separate file
- Identifies sensitive links based on predefined keywords
- Saves categorized links into organized text files

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/Golden-Secure/Way-Secure.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Way-Secure
   ```
3. Install dependencies:
   ```sh
   pip install requests
   pip install colorama
   ```

## Usage

1. Run the script:
   ```py
   python Way-Secure.py
   ```
2. Enter the domain when prompted (e.g., `example.com`).
3. The script will:
   - Fetch archived links
   - Categorize them by file type
   - Save them into `output/` folder
   - Extract emails into `domain-emails.txt`
   - Save sensitive links into `domain-sensitive.txt`

## Output Files

- `output/domain-<extension>.txt`: Contains URLs with a specific file extension
- `output/domain-emails.txt`: Contains links with email addresses
- `output/domain-sensitive.txt`: Contains links with sensitive keywords

## Example

```
Enter domain: example.com
Fetching data from Wayback Machine...
Categorizing links...
Saving links...
Process completed!
```

## License

This project is licensed under the MIT License.

## Author

Golden-Secure
https://t.me/GoldenSecure 

