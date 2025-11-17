> Create a new Devin session. You can optionally specify parameters like snapshot ID and session visibility.

# Create a new session

## OpenAPI

````yaml post /v1/sessions
paths:
  path: /v1/sessions
  method: post
  servers:
    - url: https://api.devin.ai
      description: Devin Production Server
  request:
    security:
      - title: bearerAuth
        parameters:
          query: {}
          header:
            Authorization:
              type: http
              scheme: bearer
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              prompt:
                allOf:
                  - type: string
                    description: The task description for Devin
              snapshot_id:
                allOf:
                  - type: string
                    nullable: true
                    description: ID of a machine snapshot to use
              unlisted:
                allOf:
                  - type: boolean
                    nullable: true
                    description: Whether the session should be unlisted
              idempotent:
                allOf:
                  - type: boolean
                    nullable: true
                    description: Enable idempotent session creation
              max_acu_limit:
                allOf:
                  - type: integer
                    nullable: true
                    description: Maximum ACU limit for the session
              secret_ids:
                allOf:
                  - type: array
                    nullable: true
                    items:
                      type: string
                    description: >-
                      List of secret IDs to use. If None, use all secrets. If
                      empty list, use no secrets.
              knowledge_ids:
                allOf:
                  - type: array
                    nullable: true
                    items:
                      type: string
                    description: >-
                      List of knowledge IDs to use. If None, use all knowledge.
                      If empty list, use no knowledge.
              tags:
                allOf:
                  - type: array
                    nullable: true
                    items:
                      type: string
                    description: List of tags to add to the session.
              title:
                allOf:
                  - type: string
                    nullable: true
                    description: >-
                      Custom title for the session. If None, a title will be
                      generated automatically.
            required: true
            description: Request body for creating a new Devin session
            refIdentifier: '#/components/schemas/CreateSessionRequest'
            requiredProperties:
              - prompt
        examples:
          create-session-example:
            summary: Example request for creating a session
            value:
              prompt: >-
                Review the pull request at
                https://github.com/example/repo/pull/123
              idempotent: true
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              session_id:
                allOf:
                  - type: string
                    description: Unique identifier for the session
              url:
                allOf:
                  - type: string
                    description: URL to view the session in the web interface
              is_new_session:
                allOf:
                  - type: boolean
                    description: >-
                      Indicates if a new session was created (only present if
                      idempotent=true)
            description: Response body returned when a session is successfully created
            refIdentifier: '#/components/schemas/CreateSessionResponse'
            requiredProperties:
              - session_id
              - url
        examples:
          create-session-response:
            summary: Example response for creating a session
            value:
              session_id: devin-xxx
              url: https://app.devin.ai/sessions/xxx
              is_new_session: true
        description: Session created
    '400':
      application/json:
        schemaArray:
          - type: object
            properties:
              detail:
                allOf:
                  - type: string
                    example: Invalid input or request
        examples:
          example:
            value:
              detail: Invalid input or request
        description: Bad Request
    '401':
      application/json:
        schemaArray:
          - type: object
            properties:
              detail:
                allOf:
                  - type: string
                    example: Missing or invalid Authorization header
        examples:
          example:
            value:
              detail: Missing or invalid Authorization header
        description: Unauthorized - Invalid or missing API key
    '500':
      application/json:
        schemaArray:
          - type: object
            properties:
              detail:
                allOf:
                  - type: string
                    example: Something went wrong
        examples:
          example:
            value:
              detail: Something went wrong
        description: Internal Server Error
  deprecated: false
  type: path
components:
  schemas: {}

````