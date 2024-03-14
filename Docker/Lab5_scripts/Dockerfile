FROM python:3-alpine

# criar um repositório do app
WORKDIR /app

# instalação das dependências do app
COPY requirements.txt ./

RUN pip install -r requirements.txt

# copia todos os arquivos
COPY . .

# executa o app
EXPOSE 3000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "3000"]