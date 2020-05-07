
FROM node:lts-alpine as build-stage

ARG VUE_APP_DATABASE_ADRESS
ARG VUE_APP_WORKER_ADRESS

COPY . /app

WORKDIR /app/provoli

RUN npm install

RUN npm run build

# étape de production
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/provoli/dist /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/provoli/conf /etc/nginx/conf.d

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]