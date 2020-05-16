FROM node:latest as build-stage
WORKDIR /usr/src/app
COPY ./guest-app/package*.json ./

RUN npm install
COPY ./guest-app .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /usr/src/app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf