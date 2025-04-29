# Build stage
FROM node:20 AS build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
