# Devin Structured Output App Example - Checkmarx Vulnerability Scanner

Automated vulnerability detection and remediation system that integrates Checkmarx security scanning with Devin AI sessions for automated fixes.

## 📁 Project Structure

```
.
├── schedule/                             # Prefect scheduling and automation
│   ├── checkmarx_prefect_flow.py       # Initial Prefect flow implementation
│   ├── simple_prefect_flow.py          # Simplified local Prefect flow (no server required)
│   ├── scheduled_prefect_flow.py       # Production-ready scheduled flow (runs daily at 8 AM)
│   └── run_scheduled_flow.py           # Manual test runner for scheduled flow
├── checkmarx_vulnerability_handler.py   # Basic standalone script with mock Checkmarx API
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment variables template
└── QUICK_REFERENCE.md                   # Quick command reference
```

## 🚀 Quick Start

### Prerequisites

1. Set up your environment:
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install requests python-dotenv prefect
```

2. Configure your API key:
```bash
# Create .env file
cp .env.example .env
# Add your DEVIN_API_KEY to .env file
```

## 💻 Usage Options

### Option 1: Basic One-Time Scan

Run a simple vulnerability scan that creates Devin sessions for each issue found:

```bash
python checkmarx_vulnerability_handler.py
```

**Features:**
- Mock Checkmarx API returns 5 sample vulnerabilities
- Creates 1 Devin session per vulnerability (5 total)
- Interactive prompt to monitor completion
- Displays all session URLs

### Option 2: Prefect Flow (Local)

Run as a Prefect flow with enhanced logging and task management:

```bash
python schedule/simple_prefect_flow.py
```

**Features:**
- Structured task execution with Prefect
- Automatic retries on failures
- Better logging and monitoring
- Parallel task execution support

### Option 3: Scheduled Daily Scans (Production)

Set up automated daily vulnerability scans at 8:00 AM:

```bash
# Start the scheduled server (runs continuously)
python schedule/scheduled_prefect_flow.py
```

**Features:**
- Runs automatically every day at 8:00 AM
- Cron expression: `0 8 * * *`
- Date-stamped sessions for tracking
- Automated notifications
- Two deployments available:
  - `daily-8am-vulnerability-scan` - Scheduled 8 AM run
  - `test-immediate` - Manual trigger for testing

### Option 4: Test Scheduled Flow Manually

Test the scheduled flow without waiting for 8 AM:

```bash
python schedule/run_scheduled_flow.py
```

## 📊 Mock Vulnerability Data

The current implementation uses mock data simulating these vulnerability types:

| ID | Type | Severity | File |
|---|---|---|---|
| CX-SQL-001 | SQL Injection | High | /api/users.py |
| CX-XSS-002 | Cross-Site Scripting | Medium | /frontend/components/UserProfile.tsx |
| CX-PATH-003 | Path Traversal | High | /api/files.py |
| CX-CRYPTO-004 | Weak Cryptography | Medium | /auth/password_utils.py |
| CX-HEADER-005 | Missing Security Headers | Low | /server/app.py |

## 🔄 Workflow

1. **Detection Phase**
   - Checks Checkmarx API for vulnerabilities (currently mocked)
   - Categorizes by severity (High/Medium/Low)
   - Groups vulnerabilities by repository

2. **Session Creation Phase**
   - Python script orchestrates the remediation process
   - Creates individual Devin sessions for each vulnerability
   - Each session receives full context including repository name
   - Sessions are tagged with severity level

3. **Monitoring Phase**
   - Tracks session progress (optional)
   - Displays all session URLs for monitoring
   - Reports total vulnerabilities and severity breakdown

## 📝 Session Output Structure

### Individual Fix Session
```json
{
  "repository": "backend-api",
  "vulnerability_id": "CX-SQL-001",
  "status": "fixing",
  "fixed": false,
  "fix_timestamp": null
}
```

## ⚙️ Configuration

### Scheduling Options

Modify the cron expression in `schedule/scheduled_prefect_flow.py`:

```python
# Daily at 8 AM (default)
cron="0 8 * * *"

# Every Monday at 9 AM
cron="0 9 * * 1"

# Every 6 hours
cron="0 */6 * * *"

# Every day at 2:30 PM
cron="30 14 * * *"
```

### Customizing Vulnerabilities

Edit the `mock_checkmarx_api()` function to return different vulnerabilities:

```python
def mock_checkmarx_api() -> List[Dict[str, Any]]:
    vulnerabilities = [
        {
            "id": "CUSTOM-001",
            "type": "Custom Vulnerability",
            "severity": "Critical",
            "file": "/your/file.py",
            "line": 100,
            "description": "Your description"
        }
    ]
    return vulnerabilities
```

## 🔌 Production Integration

To integrate with real Checkmarx API:

1. Replace `mock_checkmarx_api()` with actual API calls:
```python
def check_checkmarx_api() -> List[Dict[str, Any]]:
    response = requests.get(
        "https://api.checkmarx.com/vulnerabilities",
        headers={"Authorization": f"Bearer {CHECKMARX_TOKEN}"}
    )
    return response.json()
```

2. Add Checkmarx API credentials to `.env`:
```
DEVIN_API_KEY=your_devin_key
CHECKMARX_API_KEY=your_checkmarx_key
CHECKMARX_PROJECT_ID=your_project_id
```

## 📈 Monitoring

### View Prefect Dashboard

When running Prefect flows, access the local dashboard:
```bash
# Start Prefect server
prefect server start

# View at http://localhost:4200
```

### Check Session Status

All created Devin sessions can be monitored through their individual URLs.
Each session handles one specific vulnerability in its repository.

## 🛡️ Security Notes

- API keys are stored in `.env` (never commit this file)
- Sessions are tagged for easy filtering and tracking
- Vulnerabilities are prioritized by severity
- All sessions include structured output for progress tracking

## 📚 Additional Resources

- [Devin API Documentation](https://docs.devin.ai)
- [Prefect Documentation](https://docs.prefect.io)
- [Checkmarx Documentation](https://checkmarx.com/resource/documents)

## 🐛 Troubleshooting

### Common Issues

1. **No API Key Error**
   - Ensure `.env` file exists with `DEVIN_API_KEY`

2. **Prefect Connection Error**
   - Run `prefect config unset PREFECT_API_URL` to use local mode

3. **Schedule Not Running**
   - Ensure the schedule/scheduled_prefect_flow.py process stays running
   - Check system time and timezone settings

4. **Sessions Not Created**
   - Verify API key is valid
   - Check network connectivity to api.devin.ai
