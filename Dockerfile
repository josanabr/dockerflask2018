FROM josanabr/flask
COPY gtd.py /myhome/gtd.py
ENTRYPOINT [ "python3" ]
CMD [ "/myhome/gtd.py" ]
