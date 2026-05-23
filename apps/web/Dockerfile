FROM node:20-alpine AS base

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps 2>&1 | tail -20

# Copy application
COPY . .

# Create environment
RUN echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Build stage
FROM base AS builder

RUN npm run build 2>&1 | tail -20

# Production stage
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/.env.local ./.env.local

RUN npm install --legacy-peer-deps --only=production 2>&1 | tail -10

EXPOSE 3000

CMD ["npm", "start"]
