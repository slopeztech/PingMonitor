# Ping Monitor

A Python-based monitoring tool that checks the availability of websites and services using various protocols (ICMP, HTTP, DNS) and stores the results in a SQLite database.

## Features

- Multi-protocol support:
  - ICMP (ping)
  - HTTP
  - DNS
- Configurable timeout and retry settings
- SQLite database storage for historical data
- Telegram notifications for failed pings
- Easy configuration through INI files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/slopeztech/PingMonitor.git
cd PingMonitor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Configuración de Sitios

Create configuration files in the `sites` directory for each site you want to monitor. Example (`sites/example.com.conf`):

```ini
[SiteConfig]
site = test.es
protocol = icmp
storage = sqlite
storage_file = C:\Users\username\PingMonitor\data\sqlite\test.es.sqlite


[reporter]
type = telegram
bot_token = xxx
chat_id = xxx

```

### Global Configuration

Create a `config/pingmonitor.conf` file to set global settings:

```ini
hostname = monitoring-server
```

If not specified, the system hostname will be used.

## Usage

### Database Management

Create the database and tables:
```bash
python main.py runscript database/create
```
### Sites Management

Create the site config:
```bash
python main.py runscript site/create
```

### Reporters Management

Create the reporter config:
```bash
python main.py runscript reporter/create
```

### Command Line Interface

1. Check a site configuration:
```bash
python main.py check example.com
```

2. Ping a site:
```bash
python main.py ping example.com
```


## Reporters

### Telegram Reporter

The Telegram reporter sends notifications when a ping fails. To configure it:

1. Create a Telegram bot using [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Get your chat ID (you can use [@userinfobot](https://t.me/userinfobot))
4. Add the reporter configuration to your site's config file:

```ini
[reporter]
type = telegram
bot_token = your_bot_token
chat_id = your_chat_id
```

## Automation

### Linux/Unix (cron)

1. Open your crontab:
```bash
crontab -e
```

2. Add a line to run the ping every 5 minutes:
```bash
*/5 * * * * cd /path/to/ping-monitor && /path/to/venv/bin/python main.py ping example.com >> /path/to/ping-monitor/ping.log 2>&1
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Click "Create Basic Task"
3. Set name and description
4. Choose "Daily" or "Custom" schedule
5. Action: Start a program
6. Program/script: Path to your Python executable
7. Arguments: `main.py ping example.com`
8. Start in: Path to your ping-monitor directory

### Windows (PowerShell)

Create a scheduled task using PowerShell:

```powershell
$action = New-ScheduledTaskAction -Execute "C:\path\to\venv\Scripts\python.exe" -Argument "main.py ping example.com" -WorkingDirectory "C:\path\to\ping-monitor"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "PingMonitor" -Description "Monitor example.com every 5 minutes"
```

## Database Schema

The SQLite database stores the following information for each ping:

- Site (hostname or IP)
- Protocol used
- Success status
- Response time (ms)
- Error message (if any)
- Timestamp
- Raw output
- Hostname of the monitoring machine

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
