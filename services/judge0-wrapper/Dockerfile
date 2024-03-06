# should be run in the context of the base cybersword directory
FROM node:21.5.0-slim
WORKDIR /app
COPY ./services/judge0-wrapper/yarn.lock ./services/judge0-wrapper/package.json .
RUN yarn install --frozen-lockfile && yarn global add pm2
COPY ./services/judge0-wrapper  .
COPY ./challenges ./challenges
EXPOSE 8016
# the judge0 server is called `server` in its docker-compose.yml
ENV JUDGE0_URL=http://server:2358
ENV WRAPPER_HOST=judge0-wrapper
# we use pm2 to restart the server in case it goes down
ENTRYPOINT ["pm2-runtime", "index.js"]
