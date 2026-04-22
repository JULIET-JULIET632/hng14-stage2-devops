# Build stage
FROM node:18-slim AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci --only=production

# Final stage
FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN useradd -m appuser
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000 || exit 1
CMD ["node", "app.js"]
