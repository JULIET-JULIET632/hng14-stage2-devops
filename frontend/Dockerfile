# Build stage
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm install --omit=dev

# Final stage
FROM node:22-alpine
WORKDIR /app
RUN apk add --no-cache curl
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN adduser -D appuser
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:3000 || exit 1
CMD ["node", "app.js"]
