FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy application
COPY . .

# Create .env.local
RUN echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Build
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
