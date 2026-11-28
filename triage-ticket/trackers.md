# Tracker recipes

Use the recipe for the ticket's tracker. Pass the repository or project explicitly on every call.

## GitHub (`gh`)

- Read: `gh issue view <n> --repo <owner>/<repo> --json number,url,title,body,comments,labels,issueType,milestone,updatedAt`
- Edit title and body: `gh issue edit <n> --repo <owner>/<repo> --title "<title>" --body-file <file>`
- Labels: `gh issue edit <n> --repo <owner>/<repo> --add-label <label>` (or `--remove-label`)
- Comment: `gh issue comment <n> --repo <owner>/<repo> --body-file <file>`
- Close as won't fix: add the `wontfix` label, then `gh issue close <n> --repo <owner>/<repo> --reason "not planned" --comment "<reason>"`

## Forgejo (`fj`)

`fj` infers the repository from the git remote when run inside a clone, so run it in the clone.

- Read: `fj issue view <n>` and `fj issue view <n> comments`
- Edit: `fj issue edit <n> title "<title>"` and `fj issue edit <n> body` with the new text
- Labels: `fj issue edit <n> labels --add <label>` (or `--rm`)
- Comment: `fj issue comment <n> "<text>"`
- Close as won't fix: add the `wontfix` label, then `fj issue close <n> --with-msg "<reason>"`

`fj` can't create a label. If one is missing, skip it and tell the user.

## Jira (Atlassian MCP)

Use the Atlassian MCP tools: get the issue, search with JQL, edit the issue, add a comment, and transition it. Call `getAccessibleAtlassianResources` once for the `cloudId`.

- Read: the issue with its comments, issue type, priority, components, affects versions and labels.
- Edit: title (`summary`), description and the fields in the proposal only.
- Comment: add a comment.
- Close as won't fix: add the comment, then transition to **Rejected**. A ticket can be rejected at any time.
- Never set Fixed in version here: closing as done is the user's call.
- Jira keeps its own workflow rules. If a transition or field isn't available, say so and stop; don't work around it.
