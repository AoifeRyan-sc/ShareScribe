
#Using python
FROM python:3.10
# Using Layered approach for the installation of requirements
COPY app/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
#Copy files to your container
COPY app/ ./
#Running your APP and doing some PORT Forwarding
# CMD gunicorn -b 0.0.0.0:8000 app:server
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8000", "--timeout", "120", "--keep-alive", "120"]



