 # build the seed data to include the challenge's flags
FROM python:3.9-slim AS static-pages
WORKDIR /data
COPY ./services/static-web-challenges/create_html_comment.py \
     ./services/static-web-challenges/get_flag.py \
     ./services/static-web-challenges/requirements.txt \
     .
COPY ./challenges/web/hidden_html/challenge.yml ./hidden_html.yml
RUN pip install -r requirements.txt \
    && python3 create_html_comment.py

FROM nginx:alpine
WORKDIR /app
COPY --from=static-pages /data/page1.html /app/files/page1.html
COPY  ./services/static-web-challenges/style.css \
      ./services/static-web-challenges/barty.png \
      /app/files/
COPY ./services/static-web-challenges/nginx.conf /etc/nginx/nginx.conf

EXPOSE 8017
