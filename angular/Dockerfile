FROM node:latest
WORKDIR /code
COPY package*.json /code/
RUN npm install
ADD . /code
EXPOSE 9124
CMD ["npm", "start"]