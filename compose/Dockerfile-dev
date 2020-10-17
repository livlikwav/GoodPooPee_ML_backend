FROM    python:3

WORKDIR /gppserver/

COPY    requirements.txt    ./
RUN     pip install --no-cache-dir -r requirements.txt
 # remove python log buffering
ENV     PYTHONUNBUFFERED=0
ADD     https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN     chmod +x /wait-for-it.sh
ENTRYPOINT ["bash","-c","/wait-for-it.sh mysql:3306 -t 30 -- python manage.py run"]