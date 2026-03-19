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
