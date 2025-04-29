# Frontend Dockerfile (React)
FROM node:16-slim

WORKDIR /app

COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json

RUN npm install

COPY ./src /app/src
COPY ./public /app/public

RUN npm run build

EXPOSE 80

CMD ["npm", "start"]
