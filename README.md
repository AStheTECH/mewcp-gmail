**Full programmatic control of Gmail — messages, threads, drafts, labels, filters, and settings — through 41 tools.**

A Model Context Protocol (MCP) server that exposes Gmail's API for reading, sending, and organizing mail, and for managing the mailbox's labels, filters, drafts, and settings.


## Overview

The mewcp-gmail MCP Server provides:

- Full message and thread lifecycle management — list, get, send, modify labels, trash/untrash, and permanently delete
- Label, filter, forwarding-address, and send-as alias management for organizing and routing mail
- Draft creation, retrieval, updating, and sending
- Vacation responder and auto-forwarding settings management
- Incremental mailbox sync via the history API, so a client can track changes without re-listing everything

Perfect for:

- Building an AI email assistant that triages, drafts, and organizes a Gmail inbox
- Automating label-based mail filtering and forwarding rules
- Keeping an external system's copy of a mailbox in sync via incremental history polling


## Tools

### Profile

<details>
<summary><code>get_profile</code> — Get the authenticated user's Gmail profile</summary>

Gets the current user's Gmail profile, returning mailbox email address, message/thread totals, and current history ID.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
```

**Output `data` schema:**

```typescript
{
  emailAddress: string | null;
  messagesTotal: number | null;
  threadsTotal: number | null;
  historyId: string | null;
}
```

</details>


### Drafts

<details>
<summary><code>create_draft</code> — Create a new draft</summary>

Creates a draft with the DRAFT label.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `message` (object, optional) — The message content of the draft (object (Message)); send this to give the draft its content.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  message: object | null;
}
```

</details>


<details>
<summary><code>delete_draft</code> — Permanently delete a draft (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Immediately and permanently deletes the specified draft (does not simply trash it). This action is irreversible — the draft and its message content cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the draft to delete.
```

**Output `data` schema:**

```typescript
{}
```

</details>


<details>
<summary><code>get_draft</code> — Retrieve a draft</summary>

Gets the specified draft.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the draft to retrieve.
- `format` (string, optional) — The format to return the draft's message in: `minimal` (ID and labels only), `full` (full data, parsed into `payload`), `raw` (full data as a base64url string in `raw`; `payload` unused), `metadata` (ID, labels, and headers only). `full`/`raw` are unavailable when using the `gmail.metadata` scope.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  message: object | null;
}
```

</details>


<details>
<summary><code>list_drafts</code> — List drafts in the mailbox</summary>

Lists the drafts in the user's mailbox.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `maxResults` (integer, optional) — Maximum number of drafts to return. Defaults to 100, maximum allowed is 500.
- `pageToken` (string, optional) — Page token to retrieve a specific page of results.
- `q` (string, optional) — Only return drafts matching this query, in Gmail search-box syntax, e.g. `"from:someuser@example.com rfc822msgid:<somemsgid@example.com> is:unread"`.
- `includeSpamTrash` (boolean, optional) — Include drafts from `SPAM` and `TRASH` in the results.
```

**Output `data` schema:**

```typescript
{
  drafts: {
    id: string | null;
    message: object | null;
  }[] | null;
  nextPageToken: string | null;
  resultSizeEstimate: number | null;
}
```

</details>


<details>
<summary><code>send_draft</code> — Send an existing draft</summary>

Sends the specified, existing draft to the recipients in the To, Cc, and Bcc headers.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the existing draft to send.
- `message` (object, optional) — Optional — the draft's message content (object (Message)).
```

**Output `data` schema:**

```typescript
{}
```

</details>


<details>
<summary><code>update_draft</code> — Replace a draft's content</summary>

NOTE: this tool first fetches the draft's current state, then replaces it — the response includes both the `before` and `after` state so you have a full record of what changed. Replaces a draft's content entirely; since this is a full overwrite, any fields not included in `message` are lost.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the draft to update.
- `message` (object, optional) — The replacement message content of the draft (object (Message)); since this is a full replace, send this to give the draft its new content.
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string | null;
    message: object | null;
  };
  after: {
    id: string | null;
    message: object | null;
  };
}
```

</details>


### Labels

<details>
<summary><code>create_label</code> — Create a label</summary>

Creates a label.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `name` (string, required) — The display name of the label.
- `messageListVisibility` (enum: show, hide, optional) — Visibility of messages with this label in the Gmail web message list.
- `labelListVisibility` (enum: labelShow, labelShowIfUnread, labelHide, optional) — Visibility of the label itself in the Gmail web label list.
- `type` (enum: system, user, optional) — Owner type. `system` labels are internally created by Gmail and cannot be added/modified/deleted. `user` labels are created by the user/app.
- `color_text_color` (string, optional) — Text color hex string for the label, chosen from Gmail's fixed color palette. Only available for `type: user` labels; must be set together with `color_background_color`.
- `color_background_color` (string, optional) — Background color hex string for the label, chosen from Gmail's fixed color palette. Only available for `type: user` labels; must be set together with `color_text_color`.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  messageListVisibility: string | null;
  labelListVisibility: string | null;
  type: string | null;
  messagesTotal: number | null;
  messagesUnread: number | null;
  threadsTotal: number | null;
  threadsUnread: number | null;
  color: {
    textColor: string | null;
    backgroundColor: string | null;
  } | null;
}
```

</details>


<details>
<summary><code>delete_label</code> — Permanently delete a label (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Immediately and permanently deletes the specified label and removes it from any messages and threads it's applied to. This action is irreversible — the label and its associations with messages and threads cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the label to delete.
```

**Output `data` schema:**

```typescript
{}
```

</details>


<details>
<summary><code>get_label</code> — Retrieve a label</summary>

Gets the specified label.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the label to retrieve.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  messageListVisibility: string | null;
  labelListVisibility: string | null;
  type: string | null;
  messagesTotal: number | null;
  messagesUnread: number | null;
  threadsTotal: number | null;
  threadsUnread: number | null;
  color: {
    textColor: string | null;
    backgroundColor: string | null;
  } | null;
}
```

</details>


<details>
<summary><code>list_labels</code> — List all labels</summary>

Lists all labels in the user's mailbox.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
```

**Output `data` schema:**

```typescript
{
  labels: {
    id: string | null;
    name: string | null;
    messageListVisibility: string | null;
    labelListVisibility: string | null;
    type: string | null;
    messagesTotal: number | null;
    messagesUnread: number | null;
    threadsTotal: number | null;
    threadsUnread: number | null;
    color: {
      textColor: string | null;
      backgroundColor: string | null;
    } | null;
  }[] | null;
}
```

</details>


<details>
<summary><code>update_label</code> — Partially update a label</summary>

NOTE: this overwrites the current field values — the original state is not stored after the call. The response includes both the before and after state so you have a full record of what changed. Partially updates the specified label (only the fields provided are changed).

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the label to update.
- `name` (string, optional) — The display name of the label.
- `messageListVisibility` (enum: show, hide, optional) — Visibility of messages with this label in the Gmail web message list.
- `labelListVisibility` (enum: labelShow, labelShowIfUnread, labelHide, optional) — Visibility of the label itself in the Gmail web label list.
- `type` (enum: system, user, optional) — System labels cannot actually be renamed/recolored even though the field is present.
- `color_text_color` (string, optional) — Text color hex string, chosen from Gmail's fixed color palette; must be set together with `color_background_color`. Only applies to `type: user` labels.
- `color_background_color` (string, optional) — Background color hex string, chosen from Gmail's fixed color palette; must be set together with `color_text_color`. Only applies to `type: user` labels.
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string | null;
    name: string | null;
    messageListVisibility: string | null;
    labelListVisibility: string | null;
    type: string | null;
    messagesTotal: number | null;
    messagesUnread: number | null;
    threadsTotal: number | null;
    threadsUnread: number | null;
    color: { textColor: string | null; backgroundColor: string | null; } | null;
  };
  after: {
    id: string | null;
    name: string | null;
    messageListVisibility: string | null;
    labelListVisibility: string | null;
    type: string | null;
    messagesTotal: number | null;
    messagesUnread: number | null;
    threadsTotal: number | null;
    threadsUnread: number | null;
    color: { textColor: string | null; backgroundColor: string | null; } | null;
  };
}
```

</details>


### Messages

<details>
<summary><code>batch_delete_messages</code> — Permanently delete many messages (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes many messages by message ID in one call; provides no guarantee that a message was not already deleted or ever existed. This action is irreversible — deleted messages cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly how many messages (and their IDs, if the list is short) will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `ids` (string[], required) — The IDs of the messages to delete. No guarantee is given that a message wasn't already deleted or ever existed — this is a fire-and-forget bulk permanent delete, irreversible.
```

**Output `data` schema:**

```typescript
{}
```

</details>


<details>
<summary><code>batch_modify_messages</code> — Add/remove labels on many messages (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Adds or removes labels on the specified messages in a single bulk call. This action affects many messages at once and can change their visibility (e.g. removing INBOX or adding TRASH/SPAM) or accessibility. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly which messages and labels will be affected, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `ids` (string[], required) — The IDs of the messages to modify. Limit of 1000 IDs per request.
- `addLabelIds` (string[], optional) — Label IDs to add to all specified messages.
- `removeLabelIds` (string[], optional) — Label IDs to remove from all specified messages.
- `addClassificationLabels` (object[], optional) — Classification Label values to add (Google Workspace only). Limit of 20 per message.
- `removeClassificationLabelIds` (string[], optional) — Classification Label values to remove from the messages.
```

**Output `data` schema:**

```typescript
{}
```

</details>


<details>
<summary><code>delete_message</code> — Permanently delete a message (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Immediately and permanently deletes the specified message; this cannot be undone (prefer trashing instead). NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the message to delete.
```

**Output `data` schema:**

```typescript
{}
```

</details>


<details>
<summary><code>get_message_attachment</code> — Retrieve a message attachment</summary>

Gets the specified message attachment.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `messageId` (string, required) — The ID of the message containing the attachment.
- `id` (string, required) — The ID of the attachment (from the message's `payload` — see get_message).
```

**Output `data` schema:**

```typescript
{
  attachmentId: string | null;
  size: number | null;
  data: string | null;
}
```

</details>


<details>
<summary><code>get_message</code> — Retrieve a message</summary>

Gets the specified message.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the message to retrieve. Usually obtained from list_messages.
- `format` (string, optional) — `minimal` (ID and labels only), `full` (default; full data parsed into `payload`, `raw` unused), `raw` (full data as base64url in `raw`, `payload` unused), `metadata` (ID, labels, and headers only). `full`/`raw` are unavailable when using the `gmail.metadata` scope.
- `metadataHeaders` (string[], optional) — When `format=METADATA`, restricts the returned headers to only those named here.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  threadId: string | null;
  labelIds: string[] | null;
  snippet: string | null;
  historyId: string | null;
  internalDate: string | null;
  payload: object | null;
  sizeEstimate: number | null;
  raw: string | null;
  classificationLabelValues: object[] | null;
}
```

</details>


<details>
<summary><code>list_messages</code> — List messages in the mailbox</summary>

Lists the messages in the user's mailbox.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `maxResults` (integer, optional) — Maximum number of messages to return. Defaults to 100, maximum allowed is 500.
- `pageToken` (string, optional) — Page token to retrieve a specific page of results.
- `q` (string, optional) — Only return messages matching this query, in Gmail search-box syntax. Cannot be used with the `gmail.metadata` scope.
- `labelIds` (string[], optional) — Only return messages with labels matching all of the given label IDs.
- `includeSpamTrash` (boolean, optional) — Include messages from `SPAM` and `TRASH` in the results.
```

**Output `data` schema:**

```typescript
{
  messages: {
    id: string | null;
    threadId: string | null;
    labelIds: string[] | null;
    snippet: string | null;
    historyId: string | null;
    internalDate: string | null;
    payload: object | null;
    sizeEstimate: number | null;
    raw: string | null;
    classificationLabelValues: object[] | null;
  }[] | null;
  nextPageToken: string | null;
  resultSizeEstimate: number | null;
}
```

</details>


<details>
<summary><code>modify_message</code> — Add/remove labels on a message</summary>

Updates the specified message's labels. Only the label additions/removals you provide are applied — everything else about the message keeps its current value. NOTE: this overwrites the current label state — the original state is not stored after the call. The response includes both the before and after state of the message so you have a full record of what changed. Adds or removes labels on the specified message.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the message to modify.
- `addLabelIds` (string[], optional) — Label IDs to add to this message. Up to 100 per update.
- `removeLabelIds` (string[], optional) — Label IDs to remove from this message. Up to 100 per update.
- `addClassificationLabels` (object[], optional) — Classification Label values to add (Google Workspace only).
- `removeClassificationLabelIds` (string[], optional) — Classification Label values to remove from the message.
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string | null;
    threadId: string | null;
    labelIds: string[] | null;
    snippet: string | null;
    historyId: string | null;
    internalDate: string | null;
    payload: object | null;
    sizeEstimate: number | null;
    raw: string | null;
    classificationLabelValues: object[] | null;
  };
  after: {
    id: string | null;
    threadId: string | null;
    labelIds: string[] | null;
    snippet: string | null;
    historyId: string | null;
    internalDate: string | null;
    payload: object | null;
    sizeEstimate: number | null;
    raw: string | null;
    classificationLabelValues: object[] | null;
  };
}
```

</details>


<details>
<summary><code>send_message</code> — Send a raw RFC 2822 message</summary>

Sends the specified message to the recipients in the To, Cc, and Bcc headers.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `raw` (string, optional) — The entire RFC 2822 message (headers + body, with `To`/`Cc`/`Bcc`/`Subject` etc. as headers), base64url-encoded. Not explicitly marked required by the provider docs but practically necessary to send anything.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  threadId: string | null;
  labelIds: string[] | null;
  snippet: string | null;
  historyId: string | null;
  internalDate: string | null;
  payload: object | null;
  sizeEstimate: number | null;
  raw: string | null;
  classificationLabelValues: object[] | null;
}
```

</details>


<details>
<summary><code>trash_message</code> — Move a message to trash</summary>

Moves the specified message to the trash. This changes the message's labels (typically adding TRASH and removing INBOX) — everything else about the message keeps its current value. NOTE: this overwrites the current label state — the original state is not stored after the call. The response includes both the before and after state of the message so you have a full record of what changed. Moves the specified message to the trash.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the message to trash.
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string | null;
    threadId: string | null;
    labelIds: string[] | null;
    snippet: string | null;
    historyId: string | null;
    internalDate: string | null;
    payload: object | null;
    sizeEstimate: number | null;
    raw: string | null;
    classificationLabelValues: object[] | null;
  };
  after: {
    id: string | null;
    threadId: string | null;
    labelIds: string[] | null;
    snippet: string | null;
    historyId: string | null;
    internalDate: string | null;
    payload: object | null;
    sizeEstimate: number | null;
    raw: string | null;
    classificationLabelValues: object[] | null;
  };
}
```

</details>


<details>
<summary><code>untrash_message</code> — Remove a message from trash</summary>

Removes the specified message from the trash. This changes the message's labels (typically removing TRASH) — everything else about the message keeps its current value. NOTE: this overwrites the current label state — the original state is not stored after the call. The response includes both the before and after state of the message so you have a full record of what changed. Removes the specified message from the trash.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the message to remove from trash.
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string | null;
    threadId: string | null;
    labelIds: string[] | null;
    snippet: string | null;
    historyId: string | null;
    internalDate: string | null;
    payload: object | null;
    sizeEstimate: number | null;
    raw: string | null;
    classificationLabelValues: object[] | null;
  };
  after: {
    id: string | null;
    threadId: string | null;
    labelIds: string[] | null;
    snippet: string | null;
    historyId: string | null;
    internalDate: string | null;
    payload: object | null;
    sizeEstimate: number | null;
    raw: string | null;
    classificationLabelValues: object[] | null;
  };
}
```

</details>


### Threads

<details>
<summary><code>delete_thread</code> — Permanently delete a thread (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Immediately and permanently deletes the specified thread and all its messages; cannot be undone (prefer trashing instead). NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the thread to delete.
```

**Output `data` schema:**

```typescript
{}
```

</details>


<details>
<summary><code>get_thread</code> — Retrieve a thread</summary>

Gets the specified thread.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the thread to retrieve.
- `format` (string, optional) — The format to return the thread's messages in: `full` (full email data, `payload` parsed; unavailable with the `gmail.metadata` scope), `metadata` (IDs, labels, and headers only), `minimal` (IDs and labels only).
- `metadataHeaders` (string[], optional) — When `format=METADATA`, restricts the returned headers to only those named here.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  snippet: string | null;
  historyId: string | null;
  messages: object[] | null;
}
```

</details>


<details>
<summary><code>list_threads</code> — List threads in the mailbox</summary>

Lists the threads in the user's mailbox.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `maxResults` (integer, optional) — Maximum number of threads to return. Defaults to 100, maximum allowed is 500.
- `pageToken` (string, optional) — Page token to retrieve a specific page of results.
- `q` (string, optional) — Only return threads matching this query, in Gmail search-box syntax. Cannot be used with the `gmail.metadata` scope.
- `labelIds` (string[], optional) — Only return threads with labels matching all of the given label IDs.
- `includeSpamTrash` (boolean, optional) — Include threads from `SPAM` and `TRASH` in the results.
```

**Output `data` schema:**

```typescript
{
  threads: {
    id: string | null;
    snippet: string | null;
    historyId: string | null;
    messages: object[] | null;
  }[] | null;
  nextPageToken: string | null;
  resultSizeEstimate: number | null;
}
```

</details>


<details>
<summary><code>modify_thread</code> — Add/remove labels on a thread</summary>

NOTE: this changes label state on the thread (all its messages) immediately — the original label state is not stored after the call, so the response includes both the `before` and `after` thread state for a full record of what changed. Adds or removes labels applied to the thread; this affects all messages in the thread.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the thread to modify.
- `addLabelIds` (string[], optional) — Label IDs to add to this thread (all its messages). Up to 100 per update.
- `removeLabelIds` (string[], optional) — Label IDs to remove from this thread (all its messages). Up to 100 per update.
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string | null;
    snippet: string | null;
    historyId: string | null;
    messages: object[] | null;
  };
  after: {
    id: string | null;
    snippet: string | null;
    historyId: string | null;
    messages: object[] | null;
  };
}
```

</details>


<details>
<summary><code>trash_thread</code> — Move a thread to trash</summary>

NOTE: this moves the thread (all its messages) to trash immediately — the original, non-trashed state is not stored after the call, so the response includes both the `before` and `after` thread state for a full record of what changed. Moves the specified thread, and all its messages, to the trash.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the thread to trash.
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string | null;
    snippet: string | null;
    historyId: string | null;
    messages: object[] | null;
  };
  after: {
    id: string | null;
    snippet: string | null;
    historyId: string | null;
    messages: object[] | null;
  };
}
```

</details>


<details>
<summary><code>untrash_thread</code> — Remove a thread from trash</summary>

NOTE: this removes the thread (all its messages) from trash immediately — the prior, trashed state is not stored after the call, so the response includes both the `before` and `after` thread state for a full record of what changed. Removes the specified thread, and all its messages, from the trash.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the thread to remove from trash.
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string | null;
    snippet: string | null;
    historyId: string | null;
    messages: object[] | null;
  };
  after: {
    id: string | null;
    snippet: string | null;
    historyId: string | null;
    messages: object[] | null;
  };
}
```

</details>


### History

<details>
<summary><code>list_history</code> — List mailbox change history for sync</summary>

Lists the history of all changes to the mailbox in chronological order (increasing historyId), for syncing local client state with the server.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `startHistoryId` (string, required) — Return history records after this `historyId` (obtained from a message's/thread's `historyId`, or a previous `list` response). History IDs increase chronologically but are not contiguous. An invalid or stale `startHistoryId` typically returns `HTTP 404` — perform a full sync if that happens. A `historyId` is usually valid for at least a week (sometimes only a few hours). No `nextPageToken` in the response means there are no updates; store the returned `historyId` for the next request.
- `maxResults` (integer, optional) — Maximum number of history records to return. Defaults to 100, maximum allowed is 500.
- `pageToken` (string, optional) — Page token to retrieve a specific page of results.
- `labelId` (string, optional) — Only return messages with a label matching this ID.
- `historyTypes` (string[], optional) — Restrict to these history record types. Enum values (`HistoryType`): `messageAdded`, `messageDeleted`, `labelAdded`, `labelRemoved`.
```

**Output `data` schema:**

```typescript
{
  history: {
    id: string | null;
    messages: object[] | null;
    messagesAdded: object[] | null;
    messagesDeleted: object[] | null;
    labelsAdded: object[] | null;
    labelsRemoved: object[] | null;
  }[] | null;
  nextPageToken: string | null;
  historyId: string | null;
}
```

</details>


### Settings

<details>
<summary><code>get_auto_forwarding_settings</code> — Get the auto-forwarding setting</summary>

Gets the auto-forwarding setting for the account.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
```

**Output `data` schema:**

```typescript
{
  enabled: boolean | null;
  emailAddress: string | null;
  disposition: string | null;
}
```

</details>


<details>
<summary><code>get_vacation_settings</code> — Get the vacation responder settings</summary>

Gets the vacation responder settings.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
```

**Output `data` schema:**

```typescript
{
  enableAutoReply: boolean | null;
  responseSubject: string | null;
  responseBodyPlainText: string | null;
  responseBodyHtml: string | null;
  restrictToContacts: boolean | null;
  restrictToDomain: boolean | null;
  startTime: string | null;
  endTime: string | null;
}
```

</details>


<details>
<summary><code>update_vacation_settings</code> — Update the vacation responder settings</summary>

Updates the vacation responder settings. This first fetches the current settings so the response can report what changed. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the current field values — the original state is not stored after the call. The response includes both the before and after state (top-level fields are the post-update state, `data.before` holds the pre-update state) so you have a full record of what changed.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `enableAutoReply` (boolean, optional) — Whether Gmail automatically replies to messages.
- `responseSubject` (string, optional) — Text prepended to the subject line in vacation responses. Either this or the response body must be nonempty to enable auto-replies.
- `responseBodyPlainText` (string, optional) — Response body in plain text. If both plain-text and HTML bodies are set, HTML is used.
- `responseBodyHtml` (string, optional) — Response body in HTML (Gmail sanitizes it before storing). Used over plain text when both are set.
- `restrictToContacts` (boolean, optional) — Whether responses are limited to senders in the user's contacts.
- `restrictToDomain` (boolean, optional) — Whether responses are limited to senders in the user's domain. Google Workspace only.
- `startTime` (string, optional) — Optional start time for auto-replies (epoch ms). Replies only to messages received after this time. Must precede endTime if both are set.
- `endTime` (string, optional) — Optional end time for auto-replies (epoch ms). Replies only to messages received before this time. Must follow startTime if both are set.
```

**Output `data` schema:**

```typescript
{
  before: {
    enableAutoReply: boolean | null;
    responseSubject: string | null;
    responseBodyPlainText: string | null;
    responseBodyHtml: string | null;
    restrictToContacts: boolean | null;
    restrictToDomain: boolean | null;
    startTime: string | null;
    endTime: string | null;
  };
  after: {
    enableAutoReply: boolean | null;
    responseSubject: string | null;
    responseBodyPlainText: string | null;
    responseBodyHtml: string | null;
    restrictToContacts: boolean | null;
    restrictToDomain: boolean | null;
    startTime: string | null;
    endTime: string | null;
  };
}
```

</details>


### Filters

<details>
<summary><code>create_filter</code> — Create a mail filter</summary>

Creates a mail filter (an account can have a maximum of 1,000 filters).

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `from` (string, optional) — Sender's display name or email address. Maps to the filter's `criteria.from`.
- `to` (string, optional) — Recipient's display name or email address (matches To/Cc/Bcc). Maps to the filter's `criteria.to`.
- `subject` (string, optional) — Case-insensitive phrase in the subject; whitespace trimmed/collapsed. Maps to the filter's `criteria.subject`.
- `query` (string, optional) — Only match messages matching this query, in Gmail search-box syntax. Maps to the filter's `criteria.query`.
- `negatedQuery` (string, optional) — Only match messages NOT matching this query, same syntax. Maps to the filter's `criteria.negatedQuery`.
- `hasAttachment` (boolean, optional) — Whether the message has any attachment. Maps to the filter's `criteria.hasAttachment`.
- `excludeChats` (boolean, optional) — Whether to exclude chats from the match. Maps to the filter's `criteria.excludeChats`.
- `size` (integer, optional) — Size of the entire RFC822 message in bytes (headers + attachments), compared per `sizeComparison`. Maps to the filter's `criteria.size`.
- `sizeComparison` (string, optional) — How `size` should relate to the actual message size. Enum values (`SizeComparison`): `unspecified`, `smaller`, `larger`. Maps to the filter's `criteria.sizeComparison`.
- `addLabelIds` (string[], optional) — Labels to add to matching messages. Maps to the filter's `action.addLabelIds`.
- `removeLabelIds` (string[], optional) — Labels to remove from matching messages. Maps to the filter's `action.removeLabelIds`.
- `forward` (string, optional) — Email address to forward matching messages to, keeping the original sender in From. Maps to the filter's `action.forward`.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  criteria: {
    from: string | null;
    to: string | null;
    subject: string | null;
    query: string | null;
    negatedQuery: string | null;
    hasAttachment: boolean | null;
    excludeChats: boolean | null;
    size: number | null;
    sizeComparison: string | null;
  } | null;
  action: {
    addLabelIds: string[] | null;
    removeLabelIds: string[] | null;
    forward: string | null;
  } | null;
}
```

</details>


<details>
<summary><code>delete_filter</code> — Permanently delete a filter (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Immediately and permanently deletes the specified filter. This action is irreversible — the filter's criteria and actions cannot be recovered once deleted. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the filter to delete.
```

**Output `data` schema:**

```typescript
{}
```

</details>


<details>
<summary><code>get_filter</code> — Retrieve a filter</summary>

Gets the specified filter.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `id` (string, required) — The ID of the filter to fetch.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  criteria: {
    from: string | null;
    to: string | null;
    subject: string | null;
    query: string | null;
    negatedQuery: string | null;
    hasAttachment: boolean | null;
    excludeChats: boolean | null;
    size: number | null;
    sizeComparison: string | null;
  } | null;
  action: {
    addLabelIds: string[] | null;
    removeLabelIds: string[] | null;
    forward: string | null;
  } | null;
}
```

</details>


<details>
<summary><code>list_filters</code> — List mail filters</summary>

Lists the message filters of the Gmail user.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
```

**Output `data` schema:**

```typescript
{
  // Note: the Gmail API's list response field is named `filter` (singular), not `filters`.
  filter: {
    id: string | null;
    criteria: {
      from: string | null;
      to: string | null;
      subject: string | null;
      query: string | null;
      negatedQuery: string | null;
      hasAttachment: boolean | null;
      excludeChats: boolean | null;
      size: number | null;
      sizeComparison: string | null;
    } | null;
    action: {
      addLabelIds: string[] | null;
      removeLabelIds: string[] | null;
      forward: string | null;
    } | null;
  }[] | null;
}
```

</details>


### Forwarding Addresses

<details>
<summary><code>get_forwarding_address</code> — Retrieve a forwarding address</summary>

Gets the specified forwarding address.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `forwardingEmail` (string, required) — The forwarding address to retrieve.
```

**Output `data` schema:**

```typescript
{
  forwardingEmail: string | null;
  verificationStatus: string | null;
}
```

</details>


<details>
<summary><code>list_forwarding_addresses</code> — List forwarding addresses</summary>

Lists the forwarding addresses for the specified account.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
```

**Output `data` schema:**

```typescript
{
  forwardingAddresses: {
    forwardingEmail: string | null;
    verificationStatus: string | null;
  }[] | null;
}
```

</details>


### Send-As

<details>
<summary><code>get_send_as_alias</code> — Retrieve a send-as alias</summary>

Gets the specified send-as alias.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `sendAsEmail` (string, required) — The send-as alias to retrieve.
```

**Output `data` schema:**

```typescript
{
  sendAsEmail: string | null;
  displayName: string | null;
  replyToAddress: string | null;
  signature: string | null;
  isPrimary: boolean | null;
  isDefault: boolean | null;
  treatAsAlias: boolean | null;
  smtpMsa: {
    host: string | null;
    port: number | null;
    username: string | null;
    password: string | null;
    securityMode: string | null;
  } | null;
  verificationStatus: string | null;
}
```

</details>


<details>
<summary><code>list_send_as_aliases</code> — List send-as aliases</summary>

Lists the send-as aliases for the account, including the primary address and any custom "from" aliases.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
```

**Output `data` schema:**

```typescript
{
  sendAs: {
    sendAsEmail: string | null;
    displayName: string | null;
    replyToAddress: string | null;
    signature: string | null;
    isPrimary: boolean | null;
    isDefault: boolean | null;
    treatAsAlias: boolean | null;
    smtpMsa: {
      host: string | null;
      port: number | null;
      username: string | null;
      password: string | null;
      securityMode: string | null;
    } | null;
    verificationStatus: string | null;
  }[] | null;
}
```

</details>


<details>
<summary><code>update_send_as_alias</code> — Partially update a send-as alias</summary>

NOTE: this tool first fetches the alias's current state, then applies your changes — the response includes both the `before` and `after` state so you have a full record of what changed. Only the fields you provide are changed — others keep their current value. Partially updates the specified send-as alias.

**Inputs:**
```
- `userId` (string, required) — The user's email address. The special value `me` can be used to indicate the authenticated user.
- `sendAsEmail` (string, required) — The send-as alias to update.
- `displayName` (string, optional) — Name shown in the From: header.
- `replyToAddress` (string, optional) — Optional Reply-To: address. Empty means no Reply-To: header is generated.
- `signature` (string, optional) — Optional HTML signature added to new messages composed with this alias in the Gmail web UI.
- `isDefault` (boolean, optional) — Whether this is the default From: address for new messages/vacation replies.
- `treatAsAlias` (boolean, optional) — Whether Gmail should treat this address as an alias of the primary address. Custom "from" aliases only.
- `smtpMsa` (object, optional) — Optional outbound SMTP relay for mail sent with this alias (object (SmtpMsa)); custom aliases only. Keys: `host` (string, SMTP service hostname), `port` (integer, SMTP service port), `username` (string, write-only), `password` (string, write-only), `securityMode` (enum: `securityModeUnspecified`, `none`, `ssl`, `starttls`).
```

**Output `data` schema:**

```typescript
{
  before: {
    sendAsEmail: string | null;
    displayName: string | null;
    replyToAddress: string | null;
    signature: string | null;
    isPrimary: boolean | null;
    isDefault: boolean | null;
    treatAsAlias: boolean | null;
    smtpMsa: {
      host: string | null;
      port: number | null;
      username: string | null;
      password: string | null;
      securityMode: string | null;
    } | null;
    verificationStatus: string | null;
  };
  after: {
    sendAsEmail: string | null;
    displayName: string | null;
    replyToAddress: string | null;
    signature: string | null;
    isPrimary: boolean | null;
    isDefault: boolean | null;
    treatAsAlias: boolean | null;
    smtpMsa: {
      host: string | null;
      port: number | null;
      username: string | null;
      password: string | null;
      securityMode: string | null;
    } | null;
    verificationStatus: string | null;
  };
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "VALIDATION_ERROR", "message": "userId is required", "details": null },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Common Parameters</strong></summary>

- `userId` — The user's email address. The special value `me` can be used to indicate the authenticated user. Required on nearly every tool.
- `maxResults` — Maximum number of items to return on list-type tools (drafts, messages, threads, history). Defaults to 100, maximum allowed is 500.
- `pageToken` — Page token to retrieve a specific page of results, taken from a previous list-type tool's `nextPageToken`.
- `q` — Search-box query syntax (as used in the Gmail web UI) for filtering drafts, messages, and threads. Unavailable when only the `gmail.metadata` scope is granted.
- `includeSpamTrash` — Include items from `SPAM` and `TRASH` in list results (drafts, messages, threads).

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**User ID:**

```
me | {email address}
Example: me
```

**Resource IDs (message, thread, draft, label, filter):**

```
Opaque, API-assigned string
Example: 18abc2f3e4d5f678
```

**History ID:**

```
Numeric string, increases chronologically but not contiguously
Example: 1234567
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
  2. Connect your Gmail account (OAuth)
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
  1. Verify endpoint format: `mewcp-gmail/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Gmail API Error</strong></summary>

- **Cause:** Upstream Gmail API returned an error
- **Solution:**
  1. Check Gmail/Google Workspace service status at [Google Workspace Status Dashboard](https://www.google.com/appsstatus/dashboard/)
  2. Verify your credential has the required scopes (see `SCOPES` in `gmail_mcp/config.py`)
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Gmail API Documentation](https://developers.google.com/gmail/api/guides)** — Official API reference
- **[Gmail API Reference](https://developers.google.com/gmail/api/reference/rest)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling


</details>
