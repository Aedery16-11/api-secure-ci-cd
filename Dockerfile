FROM python:3.11-slim
# Source - https://stackoverflow.com/a/67262075
# Posted by Jonah C Rowlinson, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-16, License - CC BY-SA 4.0

# Add a new user "john" with user id 8877
RUN useradd -u 8877 john
# Change to non-root privilege
USER john

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
