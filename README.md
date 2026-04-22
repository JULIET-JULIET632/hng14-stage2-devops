
All containers should be healthy before the frontend and API start accepting traffic.

---

## Stopping the Stack

```bash
docker compose down
```

To also remove volumes:

```bash
docker compose down -v
```

---

## Running Tests

```bash
docker compose run api pytest --cov=. --cov-report=term
```

---

## CI/CD Pipeline

The GitHub Actions pipeline runs on every push and pull request with the following stages in strict order:

1. **Lint** — flake8 (Python), eslint (JavaScript), hadolint (Dockerfiles)
2. **Test** — pytest with Redis mocked, coverage report uploaded as artifact
3. **Build** — builds and tags all three images, pushes to local registry
4. **Security Scan** — Trivy scans all images, fails on CRITICAL findings
5. **Integration Test** — brings full stack up, submits a job, asserts completion
6. **Deploy** — rolling update on push to `main` only

---

## Environment Variables

See `.env.example` for all required variables with descriptions.

---

## Bug Fixes

See [FIXES.md](./FIXES.md) for a full list of bugs found and fixed in the original source code.