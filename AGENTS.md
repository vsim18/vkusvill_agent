# AGENTS.md

- Use Python 3.12+.
- Keep application code async and typed.
- Use the official OpenAI Python SDK and Responses API.
- Use remote MCP configuration directly; do not add a local MCP proxy or server.
- Keep secrets in `.env` only and never commit them.
- Run Ruff and pytest after code changes.
- Do not make real OpenAI or MCP calls in unit tests.
- Run integration tests only when `RUN_INTEGRATION_TESTS=1`.
- Do not change the VkusVill MCP contract without checking official documentation.

