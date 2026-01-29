FROM node:20-alpine

WORKDIR /app
COPY package.json /app/package.json
RUN npm install --silent

COPY src /app/src
COPY public /app/public

CMD ["node", "src/server.js"]
