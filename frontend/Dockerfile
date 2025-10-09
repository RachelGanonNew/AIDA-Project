FROM node:18-alpine

# Set working directory
WORKDIR /app

# Ensure CA certificates are installed (fixes SSL verification errors)
RUN apk add --no-cache ca-certificates && update-ca-certificates

# Copy package files first for better caching
COPY package*.json ./

# Set npm config to reduce install issues in container environments
# (legacy peer deps avoids some React/CRA peer issues; strict-ssl=false bypasses problematic certs)
RUN npm config set legacy-peer-deps true \
    && npm config set audit false \
    && npm config set fund false \
    && npm config set strict-ssl false

# Install dependencies (include dev deps for build)
RUN npm install

# Copy the rest of the project
COPY . .

# Build the app
RUN npm run build

# Install serve globally to serve the build
RUN npm install -g serve

# Expose the app port
EXPOSE 3000

# Start the app
CMD ["serve", "-s", "build", "-l", "3000"]
