FROM node:18.18.0-alpine3.18 as build-stage

WORKDIR /app

COPY package*.json .
COPY vite.config.js .
COPY README.md .
COPY . .

RUN npm install

RUN npm run build


FROM nginx:1.17-alpine as production-stage

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]
