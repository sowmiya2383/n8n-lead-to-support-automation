# n8n-lead-to-support-automation
n8n workflow automation for converting inbound leads into structured support pipeline with routing, storage, notifications, and daily summaries

# n8n Lead-to-Support Automation Workflow

An automated n8n workflow that converts inbound leads into a structured support pipeline with intelligent routing, storage, notifications, and daily summaries.

## 📋 Features

- **Webhook Trigger**: Accepts lead data via HTTP POST requests
- **Validation**: Required field validation and spam detection
- **Lead Enrichment**: Company name inference from email domains
- **Storage**: Records stored in Google Sheets or Airtable
- **Smart Routing**:
  - High urgency → Slack alerts + Jira/Trello tickets
  - Normal urgency → Confirmation emails + status logging
- **Daily Digest**: 6 PM summary of lead statistics
- **Reliability**:
  - Idempotency handling to prevent duplicates
  - Error handling with retries
  - Dead-letter queue for failed payloads

## 🚀 Setup Instructions

### Prerequisites

- n8n instance (self-hosted or cloud)
- Accounts for integrations (choose based on your setup):
  - Google Sheets API access
  - Airtable API key
  - Slack webhook URL
  - Jira/Trello API credentials
  - Email service (SMTP or SendGrid)

### Installation

1. **Import the workflow**
   - Download `lead-to-support-workflow.json` from this repo
   - In n8n, go to Workflows → Import from File
   - Select the downloaded JSON file

2. **Configure credentials**
   Set up the following credentials in n8n:
   - Google Sheets / Airtable
   - Slack
   - Jira / Trello
   - Email (SMTP)
   - HTTP Request (for dead-letter storage)

3. **Environment Variables**
   Create a `.env` file or set these in n8n:
   ```env
   # Storage
   GOOGLE_SHEET_ID=your_sheet_id
   AIRTABLE_BASE_ID=your_base_id
   AIRTABLE_TABLE_NAME=Leads
   
   # Notifications
   SLACK_WEBHOOK_URL=your_slack_webhook
   JIRA_URL=your_jira_instance
   JIRA_EMAIL=your_email
   JIRA_API_TOKEN=your_token
   JIRA_PROJECT_KEY=your_project_key
   
   # Email
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASS=your_app_password
   EMAIL_FROM=support@yourcompany.com
   
   # Dead Letter Storage
   DEAD_LETTER_WEBHOOK=your_dead_letter_endpoint
