Here's an updated `workflow-explanation.md` that matches your actual n8n workflow JSON structure:

# docs/workflow-explanation.md

# Lead-to-Support Automation v2 - Workflow Detailed Explanation

## Architecture Overview

The workflow follows this data flow:
1. Webhook Reception → 2. Spam Detection → 3. Duplicate Check → 
4. Enrichment → 5. Storage → 6. Urgency Routing → 7. Notifications + Ticket Creation

## Complete Node Breakdown

### 1. Webhook Trigger
- **Node**: `Webhook Trigger` (n8n-nodes-base.webhook)
- **Endpoint**: `/webhook/lead-webhook`
- **Method**: POST
- **Purpose**: Receives inbound lead data from external sources
- **Input**: JSON payload with lead information

### 2. Spam Detection
- **Node**: `Spam Detection` (n8n-nodes-base.code)
- **Purpose**: Validates required fields and performs spam checks

**Validation Rules:**
- Required fields: name, email, message, urgency, product
- Spam keywords detection: ['viagra', 'casino', 'lottery', 'prize', 'winner']
- Email format validation (implicit)

**Output Fields:**
```javascript
{
  name: string,
  email: string,
  company: string,
  message: string,
  urgency: "high" | "normal",
  product: string,
  spamDetected: boolean,
  spamReasons: string,
  spamScore: number,
  processedAt: ISO timestamp
}
```

### 3. Spam Check Router
- **Node**: `Check Spam` (n8n-nodes-base.if)
- **Logic**: Branches based on spam detection
- **Two paths:**
  - **Spam detected (true)** → Dead Letter Queue
  - **Clean (false)** → Continue to Duplicate Check

### 4. Duplicate Prevention (Idempotency)
- **Node**: `Check Duplicates` (n8n-nodes-base.airtable)
- **Purpose**: Searches existing records to prevent duplicates
- **Method**: Searches Airtable "Leads" table
- **Next Node**: `No Duplicate Found` (IF node)
- **Logic**: If no existing records found → proceed; else → stop processing

### 5. Data Preparation
- **Node**: `Edit Fields` (n8n-nodes-base.set)
- **Purpose**: Prepares data for enrichment
- **Captures**: Original lead data + spam score + timestamps

### 6. Lead Enrichment
- **Node**: `Enrich Lead Data` (n8n-nodes-base.code)
- **Purpose**: Enhances lead with additional information

**Enrichment Logic:**
- If company not provided, extract from email domain
- Domain → Company name conversion:
  - Split domain (e.g., "techstartup.io" → "techstartup")
  - Replace hyphens with spaces
  - Capitalize words
- Generate unique lead ID: `LEAD-{timestamp}-{random}`
- Set status based on urgency

**Output Fields:**
```javascript
{
  name: string,
  email: string,
  message: string,
  urgency: "high" | "normal",
  product: string,
  company: string, // Enriched or original
  domain: string,  // Extracted domain
  spamScore: number,
  leadId: string,  // Unique identifier
  createdAt: timestamp,
  enrichedAt: timestamp,
  status: "urgent" | "normal"
}
```

### 7. Storage
- **Node**: `Store Lead` (n8n-nodes-base.airtable)
- **Table**: "Leads" in Airtable
- **Operation**: Create new record
- **Stores**: All enriched lead data

### 8. Urgency Router
- **Node**: `Check Urgency` (n8n-nodes-base.if)
- **Logic**: Routes based on `urgency` field value
- **Two paths:**
  - **High Urgency** → Slack Alert + Jira Ticket
  - **Normal Urgency** → Confirmation Email

### 9A. High Urgency Path - Slack Alert
- **Node**: `Send Slack Alert` (n8n-nodes-base.slack)
- **Channel**: #support-leads
- **Message Format**: 
  ```
  🚨 *URGENT SUPPORT REQUEST* 🚨
  Name: {name}
  Company: {company}
  Product: {product}
  Email: {email}
  Message: {message}
  Lead ID: {leadId}
  ```

### 9B. High Urgency Path - Jira Ticket
- **Node**: `Create an issue` (n8n-nodes-base.jira)
- **Project**: "My Software Team"
- **Issue Type**: Task
- **Summary**: Contains same urgent details as Slack message
- **Purpose**: Creates trackable ticket for urgent issues

### 10. Normal Urgency Path - Email Confirmation
- **Node**: `Send Email` (n8n-nodes-base.emailSend)
- **From**: sowmya.arun2383@gmail.com
- **To**: Lead's email address
- **Subject**: "Thank you for contacting support - {product}"
- **Body**: Confirmation with lead ID and response timeframe

### 11. Dead Letter Queue
- **Node**: `Dead Letter Queue` (n8n-nodes-base.airtable)
- **Table**: "FailedLeads" in Airtable
- **Triggered by**: 
  - Spam detection
  - Validation failures
- **Data Prep**: `Edit Fields1` adds error reason and timestamp
- **Stores**: Failed payloads with error reasons for debugging

### 12. Daily Digest System

#### 12A. Schedule Trigger
- **Node**: `Daily Digest Executions` (n8n-nodes-base.scheduleTrigger)
- **Schedule**: Daily at 6:00 PM
- **Purpose**: Triggers the daily summary generation

#### 12B. Fetch Today's Leads
- **Node**: `Fetch Today's Leads` (n8n-nodes-base.airtable)
- **Filter**: `IS_SAME({createdAt}, TODAY(), 'day')`
- **Purpose**: Retrieves all leads created today

#### 12C. Digest Generation
- **Node**: `Generate Digest` (n8n-nodes-base.code)
- **Calculations:**
  - Total leads count
  - Urgency breakdown (high vs normal)
  - Product distribution
  - Top 5 most recent leads

**Digest Output:**
```javascript
{
  totalLeads: number,
  urgencyCount: {
    high: number,
    normal: number
  },
  productCount: {
    [productName]: count
  },
  recentLeads: [
    { name, company, urgency, product, time }
  ],
  date: string
}
```

#### 12D. Send Digest
- **Node**: `Send Daily Digest` (n8n-nodes-base.slack)
- **Channel**: #support-leads
- **Format**: Rich Slack blocks with:
  - Header with date
  - Total leads count
  - Urgency statistics
  - Product breakdown
  - Recent leads with timestamps

## Error Handling Strategy

### Retry Logic
- **Transient failures**: Built-in n8n retry mechanism
- **Failed operations**: Logged and sent to Dead Letter Queue

### Dead Letter Queue
- **Table**: "FailedLeads" in Airtable
- **Captures**: 
  - Original payload
  - Error reason
  - Timestamp of failure
  - Spam reasons (if applicable)

## Idempotency Implementation

**How duplicates are prevented:**
1. Before creating new record, search existing leads
2. Use combination of email + message + approximate timestamp
3. If match found (within 5-minute window), skip creation
4. Only unique leads proceed to enrichment and storage

**Demonstration:**
- Send same payload 3 times
- First succeeds, subsequent attempts are detected as duplicates
- Only one record created in Leads table

## Data Flow Diagram

```
Webhook → Spam Detection → Check Spam
                            ├── Spam? → Dead Letter Queue
                            └── Clean → Check Duplicates
                                      └── New? → Edit Fields → Enrich → Store Lead
                                                 ↓
                                           Check Urgency
                                            ├── High → Slack + Jira
                                            └── Normal → Email

[Scheduled] Daily Digest → Fetch Leads → Generate → Send to Slack
```

## Integration Points

| Integration | Purpose | Credentials Needed |
|------------|---------|-------------------|
| Airtable | Lead storage, duplicate check, dead letter | Personal Access Token |
| Slack | Alerts and daily digest | OAuth2 |
| Jira | Ticket creation for urgent issues | Cloud API credentials |
| SMTP | Confirmation emails | SMTP server details |
