FROM public.ecr.aws/lambda/python:3.9

COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["app.lambda_handler"]