FROM skinnypigeon/serums-start
EXPOSE 2021:2021
COPY /code /code/
COPY /code/config/config.json /etc/config.json
COPY /code/entrypoint/start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh
ENV MJ_APIKEY_PUBLIC=b6e4af446eee605f158df43ad3ac1845
ENV MJ_APIKEY_PRIVATE=ba4cf2f5d7b3d2aea50ff3cc6a3d48bb
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENTRYPOINT ["/usr/local/bin/start.sh"]