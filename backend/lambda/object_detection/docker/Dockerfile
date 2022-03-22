FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y git
RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY model/model_yolov5s.pkl ./model/model_yolov5s.pkl
RUN git clone https://github.com/ultralytics/yolov5
RUN pip install -r yolov5/requirements.txt
# RUN yum update && yum upgrade -y
RUN yum install -y mesa-libGL
COPY ./api.py .
CMD ["handler.handler"]