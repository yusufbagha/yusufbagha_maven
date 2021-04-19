### To Test
- Run application with docker
- Use PostMan to send GET and POST requests
- Send `user_id` and `timestamp` as using query paramaters

Example: `127.0.0.1:5000?user_id=1&timestamp=1645946483`


### Build & Run Dockerfile

```docker build -t yusufbagha_maven:latest .```

<br>

```docker run -p 5000:5000 yusufbagha_maven```