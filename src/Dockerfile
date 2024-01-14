FROM coady/pylucene

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# COPY . .

# CMD [ "python", "./main.py" ]
CMD [ "python", "./app.py" ]
