FROM python:3.10
ENV PYTHONUNBUFFERED = 1
COPY requirements.txt /
COPY diningcoach /diningcoach
RUN pip install --upgrade pip \
  && pip install -r requirements.txt
# Executed by Docker Compose
# WORKDIR /diningcoach
# EXPOSE 8000
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "diningcoach.wsgi:application"]