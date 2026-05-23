FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Create .env.local for build
RUN echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

RUN npm run build

FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules/.next/static ./node_modules/.next/static

# Create runtime .env.local
RUN echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

EXPOSE 3000

USER node

CMD ["npm", "start"]
