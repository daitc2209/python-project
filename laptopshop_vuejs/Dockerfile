FROM node:18.18.0-alpine3.18

WORKDIR /app

COPY package*.json .
COPY vite.config.js .
COPY README.md .
COPY . .

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev"]