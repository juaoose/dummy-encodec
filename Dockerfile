FROM nvidia/cuda:11.3.1-runtime-ubuntu20.04
CMD nvidia-smi

# Install python
RUN apt-get update
RUN apt-get install -y git python3 python3-pip --fix-missing

WORKDIR /encodec

COPY ./requirements.txt /encodec/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /encodec/requirements.txt

COPY ./app /encodec/app

RUN python3 -c "import encodec; encodec.EncodecModel.encodec_model_48khz()"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]