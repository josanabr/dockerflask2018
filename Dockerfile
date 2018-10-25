FROM josanabr/flask:latest
COPY gtd.py /myhome/gtd.py
ENTRYPOINT [ "python3" ]
CMD [ "/myhome/gtd.py" ]
