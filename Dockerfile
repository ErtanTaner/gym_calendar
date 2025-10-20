FROM python:3.11.2-alpine 
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./ 
EXPOSE 8080

ENTRYPOINT ["waitress-serve", "--call", "gym_calendar:create_app"]
