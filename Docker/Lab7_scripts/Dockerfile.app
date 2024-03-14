# cria a imagem a partir da imagem do Python
FROM python:3.9-alpine

# pasta de trabalho
WORKDIR /code

# variável de ambiente - arquivo do app
ENV FLASK_APP=app.py

# variável de ambiente - ip do app
ENV FLASK_RUN_HOST=0.0.0.0

# pacotes adicionais no SO
RUN apk add --no-cache gcc musl-dev linux-headers

# copia o arquivo requirements
COPY requirements.txt requirements.txt

# instala as dependências
RUN pip install -r requirements.txt

# exposição da porta 5000
EXPOSE 5000

# copia os arquivos do host para o container
COPY . .

# execução do app
CMD [ "flask", "run" ]