# n8n-lead-to-support-automation
n8n workflow automation for converting inbound leads into structured support pipeline with routing, storage, notifications, and daily summaries

# n8n Lead-to-Support Automation Workflow

An automated n8n workflow that converts inbound leads into a structured support pipeline with intelligent routing, storage, notifications, and daily summaries.

## 📋 Features

- **Webhook Trigger**: Accepts lead data via HTTP POST requests
- **Validation**: Required field validation and spam detection
- **Lead Enrichment**: Company name inference from email domains
- **Storage**: Records stored in Airtable
- **Smart Routing**:
  - High urgency → Slack alerts + Jira tickets
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
  - Airtable API key
  - Slack webhook URL
  - Jira API credentials
  - Email service (SMTP or SendGrid)

### Installation

1. **Import the workflow**
   - Download `lead-to-support-workflow.json` from this repo
   - In n8n, go to Workflows → Import from File
   - Select the downloaded JSON file

2. **Configure credentials**
   Set up the following credentials in n8n:
   - Airtable
   - Slack
   - Jira
   - Email (SMTP)
   - HTTP Request (for dead-letter storage)

3. **Environment Variables**
   set these in n8n:
   ```env
   # Storage
   AIRTABLE_BASE_ID=app1Dyz2SNXDLS44P
   AIRTABLE_TABLE_NAME=Leads
   
   # Notifications
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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
   JIRA_URL=https://sowmiya23.atlassian.net/
   JIRA_EMAIL=sowmya.arun2383@gmail.com
   JIRA_API_TOKEN=ATATT3xFfGF0Bc4-aqBAaOYucXnnXqViOmZsw4vrJ1ObvTIbzbEMOp6FAIPdAD_uyrLqDVYSEMLDuD6IZFLH50DgIRUKpUbICRoIxfKegjU0kGp7cqW0cO-Y4ms19p30hLzSLHPsi2RN-8e0L00JFvawHB7eRjt9I5FBCUPcT0rCId0wFHU3Vrk=5E1A5ADD
   JIRA_PROJECT_KEY=KAN
   
   # Email
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=sowmya.arun2383@gmail.com
   SMTP_PASS=sowmya.arun2383@gmail.com
   EMAIL_FROM=sowmya.arun2383@gmail.com
   
   # Dead Letter Storage(Airtable)
   DEAD_LETTER_WEBHOOK=FailedLeads
