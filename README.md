# PingMonitor

PingMonitor is a Python-based network monitoring tool that allows performing different types of pings to websites and servers. The tool supports multiple protocols and data storage methods.

## Features

- Support for multiple ping protocols:
  - ICMP (traditional ping)
  - HTTP
  - DNS
  - TCP Port
- Flexible data storage:
  - SQLite
  - Plain text files
- Intuitive command-line interface
- Site-specific configuration through configuration files
- Response time measurement

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`:
  - flake8 (for style analysis)
  - requests (for HTTP requests)
  - pythonping (for ICMP pings)
  - peewee (ORM for SQLite)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/PingMonitor.git
cd PingMonitor
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Basic Commands

1. Create a new database:
```bash
python main.py runscript database/create
```

2. Create a new site configuration:
```bash
python main.py runscript sites/create
```

3. Check a site's configuration:
```bash
python main.py check site_name
```

4. Ping a site:
```bash
python main.py ping site_name
```

### Directory Structure

```
PingMonitor/
├── config/            # Configuration files
├── data/              # Data storage
│   ├── sqlite/        # SQLite databases
│   └── plain/         # Plain text files
├── scripts/           # Utility scripts
│   ├── database/      # Database-related scripts
│   └── sites/         # Site-related scripts
├── sites/             # Site configurations
├── utils/             # Utility modules
├── main.py            # Main script
└── requirements.txt   # Project dependencies
```

## Configuration

### General Configuration File

The `config/pingmonitor.conf` file contains the system's general configuration:

```ini
[general]
lang = en
```

### Site Configuration

Each site has its own configuration file in the `sites/` directory with the following format:

```ini
[SiteConfig]
site = example.com
protocol = http
storage = sqlite
storage_file = /path/to/database.sqlite
```

## Contributing

Contributions are welcome. Please make sure to:

1. Follow the project's style conventions (configured in `.flake8`)
2. Test your changes before submitting a pull request
3. Update documentation as needed

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
