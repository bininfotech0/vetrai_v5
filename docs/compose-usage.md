# Docker Compose usage notes (Windows / Linux)

This short note explains which `compose` command to use when running the project locally.

Summary
- On Windows with Docker Desktop: use the `docker-compose` (hyphen) binary included with Docker Desktop.
- On Linux systems that have the Docker CLI Compose plugin installed: use `docker compose` (no hyphen).

Why this matters
- `docker compose` is the newer Compose V2 plugin that integrates with the `docker` CLI.
- Some environments (especially Windows/older installs) ship the standalone `docker-compose` binary instead.
- Passing flags in the wrong place will produce errors (PowerShell may treat `-f` as a `docker` flag if `docker compose` isn't available).

Recommended commands (cross-platform safe)
- Start services (dev):

```powershell
# Works on most Windows setups that include the docker-compose binary
docker-compose -f docker-compose.yml up -d
```

```bash
# Works on Linux setups with the compose plugin
docker compose -f docker-compose.yml up -d
```

- Restart services (example):

```powershell
# Windows (hyphen)
docker-compose -f docker-compose.yml restart
```

```bash
# Linux (plugin)
docker compose -f docker-compose.yml restart
```

Notes and troubleshooting
- If `docker compose` returns "unknown command", your Docker installation does not expose the compose plugin. Use `docker-compose` instead.
- If `docker-compose` is missing, install it or enable the Docker Compose plugin for your Docker installation.
- When using `--project-name`/`-p`, place the option before the subcommand:
  - Correct: `docker-compose -p myproj up -d`
  - Incorrect: `docker-compose up -d --project-name myproj`

Want me to update README.md or other docs to include this note?