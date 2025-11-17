# Structured Output

> Learn how to effectively use structured output and interact with Devin sessions via API

<Note>
  Structured output is like Devin's notepad - it updates its notes as it works, and you can check these notes anytime. Currently, you can't force Devin to update its notes, but you can request to see what it has written so far.
</Note>

<CardGroup cols={2}>
  <Card title="Progress Updates" icon="chart-line">
    Get updates on Devin's progress during long-running tasks
  </Card>

  <Card title="Application Integration" icon="puzzle-piece">
    Pipe Devin's analysis and outputs into your applications with consistent JSON.
  </Card>
</CardGroup>

## Requesting Structured Output

To use structured output, include your desired JSON schema in the prompt when [creating a session](/api-reference/sessions/create-a-new-devin-session).
Make sure to tell Devin to update the structured output whenever something relevant happens.

<Tabs>
  <Tab title="PR Review">
    ```json  theme={null}
    {
      "prompt": "Review this PR and provide updates in this format. Please update the structured output immediately whenever you find new issues, have suggestions, or change your approval status:\n{
        "issues": [
          {
            "file": "src/App.tsx",
            "line": 42,
            "type": "bug",
            "description": "Memory leak in useEffect cleanup"
          }
        ],
        "suggestions": [
          "Add error handling for API calls",
          "Split component into smaller parts"
        ],
        "approved": false
      }"
    }
    ```

    Simple format for PR reviews and code analysis.
  </Tab>

  <Tab title="Progress Updates">
    ```json  theme={null}
    {
      "prompt": "As you work, provide updates in this format. Please update the structured output immediately whenever you start a new task, complete a task, or plan your next task:\n{
        "status": "in_progress",
        "current_task": "Adding authentication to login page",
        "completed_tasks": [
          "Set up project structure",
          "Added routing"
        ],
        "next_task": "Implement form validation"
      }"
    }
    ```

    Track what Devin is currently working on and what's next.
  </Tab>

  <Tab title="Test Results">
    ```json  theme={null}
    {
      "prompt": "When running tests, report results in this format. Please update the structured output immediately after each test run and whenever coverage changes:\n{
        "tests_passed": 25,
        "tests_failed": 2,
        "failing_tests": [
          {
            "name": "login_validation",
            "error": "Expected error message to be shown"
          }
        ],
        "coverage": 85
      }"
    }
    ```

    Simple overview of test execution results.
  </Tab>

  <Tab title="Feature Implementation">
    ```json  theme={null}
    {
      "prompt": "Build a user settings page and track progress in this format. Please update the structured output immediately whenever you complete a requirement, create new files, identify review items, or change testing status:\n{
        "requirements_met": {
          "can_change_password": true,
          "can_update_email": false,
          "dark_mode_toggle": true
        },
        "files_created": [
          "UserSettings.tsx",
          "useUpdateProfile.ts"
        ],
        "needs_review": [
          "Email update flow needs security review"
        ],
        "ready_for_testing": false
      }"
    }
    ```

    Track feature implementation against specific requirements.
  </Tab>
</Tabs>

## Retrieving Structured Output

Use [this endpoint](/api-reference/sessions/retrieve-details-about-an-existing-session) to retrieve the structured output from a session.
The structured output is returned in the `structured_output` field.

<Tip>
  When using the Devin web app, you can quickly view the structured output at any time by pressing `⌘ + I` (Command+I).
</Tip>

## Best Practices

* Include schema definition in initial prompt
* Define expected update frequency (e.g., "Please update structured output after you add each new component to the website")
* Document value types and formats clearly
* Use clear, descriptive field names so Devin knows what to write
* Include example values in your schema
* Use 10-30 second intervals for polling to avoid overwhelming the Devin API
* Stop polling when session completes or errors out

<Note>
  Remember that Devin updates structured output on its own schedule - you can't force an update, but you can request to see the latest notes at any time.
</Note>

For questions about using structured output or to report issues, email [support@cognition.ai](mailto:support@cognition.ai).