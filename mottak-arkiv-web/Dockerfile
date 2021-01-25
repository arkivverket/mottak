# build environment
FROM node:alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
COPY yarn.lock ./
RUN yarn install --frozen-lockfile

# Only copy required files
COPY src /app/src
COPY public /app/public
COPY env.sh /app
COPY tsconfig.json /app
# For some reason "create-react-app build" requires ESlint config
COPY .eslintrc.json /app
RUN yarn build

# production environment
FROM nginx:stable-alpine
WORKDIR /app

COPY --from=build /app/build /app/public

COPY env.sh .
COPY default.conf /etc/nginx/conf.d/default.conf

# Make our shell script executable
RUN chmod +x env.sh

EXPOSE 80
# Start Nginx server
CMD ["/bin/sh", "-c", "/app/env.sh && nginx -g 'daemon off;'"]
