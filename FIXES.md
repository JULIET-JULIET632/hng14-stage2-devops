# FIXES.md

This document details every bug found in the application, including the file, line number, problem, and fix applied.

---

## Fix 1
**File:** `api/main.py`  
**Line:** 8  
**Problem:** Redis host hardcoded to `localhost`. This works locally but fails inside Docker containers because each container has its own network namespace and cannot resolve `localhost` to the Redis service.  
**Fix:** Replaced with `os.environ.get("REDIS_HOST", "redis")` to read the host from environment variables.

---

## Fix 2
**File:** `api/main.py`  
**Line:** 8  
**Problem:** Redis connection does not use a password. The application has a `REDIS_PASSWORD` environment variable defined but it was never passed to the Redis client, meaning the connection would be rejected by a password-protected Redis instance.  
**Fix:** Added `password=os.environ.get("REDIS_PASSWORD")` to the Redis client initialization.

---

## Fix 3
**File:** `api/main.py`  
**Line:** EOF  
**Problem:** No uvicorn startup entry point. The API had no command to actually start the server, and no host binding defined.  
**Fix:** Added `uvicorn.run(app, host="0.0.0.0", port=8000)` at the bottom of the file. `0.0.0.0` ensures the API is reachable from outside the container.

---

## Fix 4
**File:** `worker/worker.py`  
**Line:** 6  
**Problem:** Redis host hardcoded to `localhost`. Same container networking issue as the API — the worker cannot reach Redis via `localhost` inside Docker.  
**Fix:** Replaced with `os.environ.get("REDIS_HOST", "redis")` to read the host from environment variables.

---

## Fix 5
**File:** `worker/worker.py`  
**Line:** 6  
**Problem:** Redis connection does not use a password. Worker connects to Redis without authentication, which would fail against a password-protected Redis instance.  
**Fix:** Added `password=os.environ.get("REDIS_PASSWORD")` to the Redis client initialization.

---

## Fix 6
**File:** `worker/worker.py`  
**Line:** 4  
**Problem:** `signal` module is imported but never used. The worker has no graceful shutdown handling, meaning it will be forcefully killed when the container stops, potentially mid-job.  
**Fix:** Added `SIGTERM` and `SIGINT` signal handlers to allow the worker to shut down cleanly.

---

## Fix 7
**File:** `frontend/app.js`  
**Line:** 6  
**Problem:** API URL hardcoded to `http://localhost:8000`. The frontend cannot reach the API via `localhost` when running inside a Docker container.  
**Fix:** Replaced with `process.env.API_URL || "http://api:8000"` to read the API URL from environment variables.

---

## Fix 8
**File:** `frontend/app.js`  
**Line:** 27  
**Problem:** `app.listen(3000)` binds only to the loopback interface by default, making the frontend unreachable from outside the container.  
**Fix:** Changed to `app.listen(3000, '0.0.0.0')` to bind to all interfaces.

---

## Fix 9
**File:** `api/.env`  
**Line:** 1-2  
**Problem:** A `.env` file containing a real password (`REDIS_PASSWORD=supersecretpassword123`) was committed directly into the repository. This exposes credentials in version control.  
**Fix:** Deleted `api/.env`, added `.env` to `.gitignore`, and created a `.env.example` file in the root with placeholder values for all required environment variables.

---

## Fix 10
**File:** `api/requirements.txt`  
**Line:** 1-3  
**Problem:** No dependency versions are pinned. Unpinned dependencies can result in different versions being installed across environments, causing inconsistent or broken builds.  
**Fix:** Pinned all dependencies to specific stable versions.

---

## Fix 11
**File:** `README.md`  
**Line:** 1  
**Problem:** README is essentially empty — contains only the repo name. No setup instructions, prerequisites, or usage guide.  
**Fix:** Rewrote README.md with full setup instructions, prerequisites, all commands, and expected output for a successful startup.
