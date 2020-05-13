FROM python:3.6-alpine

RUN adduser -D finance

WORKDIR /home/finance

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY finance.py config.py setup.py boot.sh app.db ./
RUN chmod +x boot.sh

ENV FLASK_APP finance.py

#RUN chown -R finance:finance ./
RUN chown -R finance:finance finance.py config.py setup.py boot.sh app.db

USER finance

#EXPOSE 5000

ENTRYPOINT ["./boot.sh"]

#ENTRYPOINT ["python"]
#CMD ["finance.py"]
