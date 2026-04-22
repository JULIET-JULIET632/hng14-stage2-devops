# Build stage
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json .
RUN npm install --omit=dev

# Final stage
FROM node:20-slim
WORKDIR /app
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN useradd -m appuser
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:3000 || exit 1
CMD ["node", "app.js"]
