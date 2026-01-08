# Gmail MCP Server

A Model Context Protocol (MCP) server that provides access to Gmail API endpoints.

## Features

This MCP server provides the following Gmail operations:

### Profile & Account
- **get_profile**: Get Gmail profile information

### Message Operations
- **list_messages**: List messages with optional filters
- **get_message**: Get specific message details
- **send_message**: Send an email
- **send_message_with_attachment**: Send email with file attachments
- **reply_to_message**: Reply to an existing email
- **search_messages**: Search using Gmail query syntax
- **delete_message**: Permanently delete a message
- **trash_message**: Move message to trash
- **untrash_message**: Restore message from trash
- **mark_as_read**: Mark message as read
- **mark_as_unread**: Mark message as unread

### Thread Operations
- **get_thread**: Get entire email thread

### Label Operations
- **list_labels**: Get all labels
- **create_label**: Create new label
- **delete_label**: Delete a label
- **modify_message_labels**: Add/remove labels from message

### Draft Operations
- **list_drafts**: List draft messages
- **create_draft**: Create a draft message

## Setup

### 1. Install Dependencies

```bash
cd gmail
pip install -r requirements.txt
```

### 2. Configure Google OAuth

You need to create OAuth credentials with the following scopes:
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.compose`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.labels`

Save your OAuth credentials as `secret.json` in this directory.

### 3. Authenticate

Run the authentication script:

```bash
python authenticate.py
```

This will:
1. Open a browser window for authentication
2. Create a `token.json` file to store your credentials
3. Reuse the token on subsequent runs

### 4. Configure Your MCP Client

#### For Claude Desktop (stdio mode - default)

Add this to your Claude Desktop MCP settings file:

**Location**: `~/.config/Claude/claude_desktop_config.json` (Linux)

```json
{
  "mcpServers": {
    "gmail": {
      "command": "python3",
      "args": ["/home/shadyskies/Desktop/mcp-tools/gmail/gmail_mcp_server.py"],
      "cwd": "/home/shadyskies/Desktop/mcp-tools/gmail"
    }
  }
}
```

#### For HTTP/SSE Transport

**SSE (Server-Sent Events)**:
```bash
python gmail_mcp_server.py --transport sse --host 0.0.0.0 --port 8002
```

**Streamable HTTP**:
```bash
python gmail_mcp_server.py --transport streamable-http --host 0.0.0.0 --port 8002
```

## Usage Examples

### Get Profile
```json
{
  "tool": "get_profile"
}
```

### List Messages
```json
{
  "tool": "list_messages",
  "arguments": {
    "max_results": 10,
    "label_ids": ["INBOX"]
  }
}
```

### Send Email
```json
{
  "tool": "send_message",
  "arguments": {
    "to": "recipient@example.com",
    "subject": "Hello from MCP",
    "body": "This is a test email sent via the Gmail MCP server."
  }
}
```

### Send Email with Attachment
```json
{
  "tool": "send_message_with_attachment",
  "arguments": {
    "to": "recipient@example.com",
    "subject": "File attached",
    "body": "Please find the attachment.",
    "attachment_path": "/path/to/file.pdf"
  }
}
```

### Search Messages
```json
{
  "tool": "search_messages",
  "arguments": {
    "query": "from:sender@example.com subject:important",
    "max_results": 20
  }
}
```

### Reply to Message
```json
{
  "tool": "reply_to_message",
  "arguments": {
    "message_id": "18d4f2c3a1b2c3d4",
    "body": "Thank you for your email!"
  }
}
```

### Create Label
```json
{
  "tool": "create_label",
  "arguments": {
    "name": "Important Projects"
  }
}
```

### Modify Labels
```json
{
  "tool": "modify_message_labels",
  "arguments": {
    "message_id": "18d4f2c3a1b2c3d4",
    "add_labels": ["STARRED"],
    "remove_labels": ["UNREAD"]
  }
}
```

## Gmail Search Query Syntax

Common search operators for `search_messages`:

- `from:sender@example.com` - From specific sender
- `to:recipient@example.com` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `has:attachment` - Has attachments
- `is:unread` - Unread messages
- `is:starred` - Starred messages
- `after:2024/01/01` - After date
- `before:2024/12/31` - Before date
- `larger:10M` - Larger than 10MB
- `filename:pdf` - Specific file type

Combine with AND/OR:
- `from:sender@example.com AND has:attachment`
- `subject:invoice OR subject:receipt`

## Standard Label IDs

Common Gmail label IDs:
- `INBOX` - Inbox
- `SENT` - Sent
- `DRAFT` - Drafts
- `SPAM` - Spam
- `TRASH` - Trash
- `UNREAD` - Unread
- `STARRED` - Starred
- `IMPORTANT` - Important
- `CATEGORY_PERSONAL` - Personal category
- `CATEGORY_SOCIAL` - Social category
- `CATEGORY_PROMOTIONS` - Promotions category
- `CATEGORY_UPDATES` - Updates category
- `CATEGORY_FORUMS` - Forums category

## Message Format Options

When using `get_message` or `get_thread`:
- `minimal` - Returns only email message ID and labels
- `full` - Returns full email message data (default)
- `raw` - Returns raw MIME message
- `metadata` - Returns only email message metadata

## Troubleshooting

### "token.json not found" Error
Run the authentication script:
```bash
python authenticate.py
```

### Authentication Issues
If you get authentication errors:
1. Delete `token.json`
2. Run `python authenticate.py` again
3. Complete the OAuth flow in your browser

### Permission Denied
Make sure your OAuth credentials have the correct scopes enabled in the Google Cloud Console:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to APIs & Services → Credentials
3. Edit your OAuth 2.0 Client ID
4. Ensure all required scopes are enabled
5. Add `http://localhost:8080` to authorized redirect URIs

### Rate Limits
Gmail API has usage quotas. If you exceed them, you'll get quota errors. Check your quota usage in the Google Cloud Console.

## Security Notes

- Keep `secret.json` and `token.json` secure and never commit them to version control
- The server uses OAuth 2.0 for secure authentication
- Access tokens are refreshed automatically when they expire
- All operations are performed with the authenticated user's permissions
- Be careful with delete operations - they are permanent

## Logging

The server logs all operations to:
- Console/stderr (for real-time monitoring)
- `gmail_mcp_server.log` (for persistent records)

Log levels:
- `INFO`: Normal operations and key events
- `DEBUG`: Detailed information
- `WARNING`: Warnings
- `ERROR`: Authentication failures, API errors
