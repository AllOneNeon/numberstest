
FROM python:3-alpine

RUN python -m pip install --upgrade pip

RUN pip3 install requests paho-mqtt

COPY NumSide.py /home/mehdi/Download/spreadsheet.py

CMD ["python","/home/mehdi/Download/spreadsheet.py"]