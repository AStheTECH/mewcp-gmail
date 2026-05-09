**Send, search, and manage Gmail — directly from your AI workflows.**

A Model Context Protocol (MCP) server that exposes Gmail's API for reading, sending, organizing, and managing email messages, threads, labels, and drafts.


## Overview

The Gmail MCP Server provides full programmatic access to Gmail through a stateless, multi-tenant interface:

- Send, reply to, and draft emails with optional attachments
- Search and retrieve messages and threads using Gmail's native query syntax
- Organize your inbox with label management and read/unread state control

Perfect for:

- Automating email workflows and notifications from AI agents
- Building assistants that can read, respond to, and triage email
- Integrating Gmail actions into LLM-powered pipelines


## Tools

<details>
<summary><code>get_profile</code> — Get the user's Gmail profile information</summary>

Returns the authenticated user's Gmail profile including email address and mailbox statistics.

**Inputs:**
```
None
```

**Output:**

```json
{
  "emailAddress": "user@gmail.com",
  "messagesTotal": 1024,
  "threadsTotal": 512,
  "historyId": "123456"
}
```

</details>


<details>
<summary><code>get_message</code> — Get a specific message by ID with full details</summary>

Fetches a single Gmail message by its ID in the requested format.

**Inputs:**
```
- `message_id` (string, required) — Gmail message ID
- `format` (string, optional) — Message format. Common values: `minimal`, `full`, `raw`, `metadata`. Default: `full`
```

**Output:**

```json
{
  "id": "18b1c2d3e4f5",
  "threadId": "18b1c2d3e4f5",
  "labelIds": ["INBOX", "UNREAD"],
  "payload": { "...": "message payload" }
}
```

</details>


<details>
<summary><code>send_message</code> — Send an email message</summary>

Composes and sends a plain-text email to one or more recipients.

**Inputs:**
```
- `to` (string, required) — Recipient email address
- `subject` (string, required) — Email subject
- `body` (string, required) — Plain-text email body
- `cc` (string, optional) — Comma-separated CC recipients
- `bcc` (string, optional) — Comma-separated BCC recipients
```

**Output:**

```json
{
  "message": "Email sent successfully",
  "id": "18b1c2d3e4f5",
  "threadId": "18b1c2d3e4f5"
}
```

</details>


<details>
<summary><code>send_message_with_attachment</code> — Send an email message with file attachments</summary>

Composes and sends an email with a file attachment from the local filesystem.

**Inputs:**
```
- `to` (string, required) — Recipient email address
- `subject` (string, required) — Email subject
- `body` (string, required) — Plain-text email body
- `attachment_path` (string, required) — Local filesystem path to the file attachment
- `cc` (string, optional) — Comma-separated CC recipients
```

**Output:**

```json
{
  "message": "Email with attachment sent successfully",
  "id": "18b1c2d3e4f5",
  "threadId": "18b1c2d3e4f5"
}
```

</details>


<details>
<summary><code>reply_to_message</code> — Reply to an existing email message</summary>

Sends a reply to an existing message, preserving the thread and original headers.

**Inputs:**
```
- `message_id` (string, required) — Gmail message ID of the message to reply to
- `body` (string, required) — Reply body text
```

**Output:**

```json
{
  "message": "Reply sent successfully",
  "id": "18b1c2d3e4f5",
  "threadId": "18b1c2d3e4f5"
}
```

</details>


<details>
<summary><code>delete_message</code> — Delete a message permanently</summary>

Permanently deletes a message. This action cannot be undone.

**Inputs:**
```
- `message_id` (string, required) — Gmail message ID
```

**Output:**

```json
{
  "message": "Message 18b1c2d3e4f5 deleted successfully",
  "id": "18b1c2d3e4f5"
}
```

</details>


<details>
<summary><code>trash_message</code> — Move a message to trash</summary>

Moves a message to the trash folder. The message can be recovered until the trash is emptied.

**Inputs:**
```
- `message_id` (string, required) — Gmail message ID
```

**Output:**

```json
{
  "message": "Message moved to trash successfully",
  "id": "18b1c2d3e4f5"
}
```

</details>


<details>
<summary><code>untrash_message</code> — Remove a message from trash</summary>

Restores a message from the trash back to the inbox.

**Inputs:**
```
- `message_id` (string, required) — Gmail message ID
```

**Output:**

```json
{
  "message": "Message removed from trash successfully",
  "id": "18b1c2d3e4f5"
}
```

</details>


<details>
<summary><code>modify_message_labels</code> — Add or remove labels from a message</summary>

Applies or removes one or more labels from a message in a single operation.

**Inputs:**
```
- `message_id` (string, required) — Gmail message ID
- `add_labels` (list of strings, optional) — Label IDs to add to the message
- `remove_labels` (list of strings, optional) — Label IDs to remove from the message
```

**Output:**

```json
{
  "message": "Labels modified successfully",
  "id": "18b1c2d3e4f5",
  "labelIds": ["INBOX", "STARRED"]
}
```

</details>


<details>
<summary><code>list_labels</code> — Get all labels in the user's mailbox</summary>

Returns all system and user-defined labels available in the authenticated user's mailbox.

**Inputs:**
```
None
```

**Output:**

```json
{
  "count": 12,
  "labels": [
    { "id": "INBOX", "name": "INBOX", "type": "system" },
    { "id": "Label_123", "name": "Work", "type": "user" }
  ]
}
```

</details>


<details>
<summary><code>create_label</code> — Create a new label</summary>

Creates a new user-defined label with configurable visibility settings.

**Inputs:**
```
- `name` (string, required) — Label name
- `label_list_visibility` (string, optional) — Visibility in the label list. Values: `labelShow`, `labelShowIfUnread`, `labelHide`. Default: `labelShow`
- `message_list_visibility` (string, optional) — Visibility in message lists. Values: `show`, `hide`. Default: `show`
```

**Output:**

```json
{
  "message": "Label created successfully",
  "label": {
    "id": "Label_456",
    "name": "Projects",
    "labelListVisibility": "labelShow",
    "messageListVisibility": "show"
  }
}
```

</details>


<details>
<summary><code>delete_label</code> — Delete a label</summary>

Permanently deletes a user-defined label. Messages with this label are not deleted.

**Inputs:**
```
- `label_id` (string, required) — Label ID to delete
```

**Output:**

```json
{
  "message": "Label Label_456 deleted successfully",
  "id": "Label_456"
}
```

</details>


<details>
<summary><code>search_messages</code> — Search messages using Gmail search syntax</summary>

Searches messages using Gmail's native query syntax and returns matching message stubs.

**Inputs:**
```
- `query` (string, required) — Gmail search query e.g. `from:example@gmail.com`, `is:unread`, `subject:invoice`
- `max_results` (integer, optional) — Maximum number of results to return, capped at 500. Default: `10`
```

**Output:**

```json
{
  "count": 3,
  "messages": [
    { "id": "18b1c2d3e4f5", "threadId": "18b1c2d3e4f5" }
  ],
  "resultSizeEstimate": 3
}
```

</details>


<details>
<summary><code>mark_as_read</code> — Mark a message as read</summary>

Removes the UNREAD label from a message, marking it as read.

**Inputs:**
```
- `message_id` (string, required) — Gmail message ID
```

**Output:**

```json
{
  "message": "Message marked as read successfully",
  "id": "18b1c2d3e4f5"
}
```

</details>


<details>
<summary><code>mark_as_unread</code> — Mark a message as unread</summary>

Adds the UNREAD label to a message, marking it as unread.

**Inputs:**
```
- `message_id` (string, required) — Gmail message ID
```

**Output:**

```json
{
  "message": "Message marked as unread successfully",
  "id": "18b1c2d3e4f5"
}
```

</details>


<details>
<summary><code>get_thread</code> — Get an entire email thread</summary>

Fetches a full email thread including all messages it contains.

**Inputs:**
```
- `thread_id` (string, required) — Gmail Thread ID
- `format` (string, optional) — Message format within the thread. Common values: `minimal`, `full`, `raw`, `metadata`. Default: `full`
```

**Output:**

```json
{
  "id": "18b1c2d3e4f5",
  "historyId": "123456",
  "messages": [ { "...": "message objects" } ]
}
```

</details>


<details>
<summary><code>list_drafts</code> — List draft messages</summary>

Returns a list of draft messages in the authenticated user's mailbox.

**Inputs:**
```
- `max_results` (integer, optional) — Maximum number of drafts to return, capped at 500. Default: `10`
```

**Output:**

```json
{
  "count": 2,
  "drafts": [
    { "id": "r123456", "message": { "id": "18b1c2d3e4f5", "threadId": "18b1c2d3e4f5" } }
  ]
}
```

</details>


<details>
<summary><code>create_draft</code> — Create a draft message</summary>

Creates a new draft email without sending it.

**Inputs:**
```
- `to` (string, required) — Recipient email address
- `subject` (string, required) — Draft subject
- `body` (string, required) — Draft body text
```

**Output:**

```json
{
  "message": "Draft created successfully",
  "id": "r123456"
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Common Parameters</strong></summary>

- `message_id` — Unique Gmail message identifier. Obtain from `search_messages`, `list_drafts`, or any message response.
- `thread_id` — Unique Gmail thread identifier. Present in every message object as `threadId`.
- `label_id` — Label identifier. Obtain from `list_labels`. System labels use names like `INBOX`, `SENT`, `TRASH`, `UNREAD`, `STARRED`.
- `max_results` — Limits the number of items returned. Always capped at 500.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Message `format` values:**

```
full      — Full message payload with body decoded (default)
minimal   — Only message IDs and labels, no payload
raw       — Full message as RFC 2822 base64url-encoded string
metadata  — Headers only, no body
```

**Gmail Search Query Syntax:**

```
from:user@example.com    — Messages from a sender
to:user@example.com      — Messages to a recipient
subject:invoice          — Messages with word in subject
is:unread                — Unread messages
is:starred               — Starred messages
has:attachment           — Messages with attachments
after:2024/01/01         — Messages after a date
label:Work               — Messages with a specific label
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Gmail credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Google account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Gmail API Error</strong></summary>

- **Cause:** Upstream Gmail API returned an error
- **Solution:**
  1. Check Google service status at [Google Workspace Status Page](https://www.google.com/appsstatus)
  2. Verify your credential has the required permissions
  3. Review the error message for specific details

</details>

---

### Resources

- **[Gmail API Documentation](https://developers.google.com/gmail/api/guides)** — Official API reference
- **[Gmail API Reference](https://developers.google.com/gmail/api/reference/rest)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling
