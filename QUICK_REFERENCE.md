# Checkmarx Scanner - Quick Reference

## 🚀 Most Common Commands

```bash
# One-time vulnerability scan
python checkmarx_vulnerability_handler.py

# Run as Prefect flow (recommended)
python simple_prefect_flow.py

# Start daily 8 AM scheduled scans
python scheduled_prefect_flow.py

# Test the scheduled flow immediately
python run_scheduled_flow.py
```

## 📅 Schedule Options

| Schedule | Cron Expression | Description |
|----------|----------------|-------------|
| Daily 8 AM | `0 8 * * *` | Every day at 8:00 AM |
| Hourly | `0 * * * *` | Every hour at :00 |
| Every 6 hours | `0 */6 * * *` | 00:00, 06:00, 12:00, 18:00 |
| Weekdays 9 AM | `0 9 * * 1-5` | Mon-Fri at 9:00 AM |
| Weekly Monday | `0 8 * * 1` | Every Monday at 8:00 AM |

## 🔧 Setup Checklist

- [ ] Install dependencies: `uv pip install requests python-dotenv prefect`
- [ ] Create `.env` file with `DEVIN_API_KEY`
- [ ] Test with: `python run_scheduled_flow.py`
- [ ] Deploy with: `python scheduled_prefect_flow.py`

## 📊 Output Summary

Each run creates:
- 1 Orchestrator session (manages overall process)
- N Fix sessions (one per vulnerability found)
- Console notification with statistics
- Tagged sessions for easy tracking
