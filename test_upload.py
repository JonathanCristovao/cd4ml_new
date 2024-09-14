import boto3
from botocore.client import Config

# Configuração das credenciais do MinIO
s3 = boto3.resource(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minio',
    aws_secret_access_key='minio123',
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

# Nome do bucket e do arquivo
bucket_name = 'cd4ml-ml-flow-bucket'
file_name = 'test_file.txt'

# Criar um arquivo de teste
with open(file_name, 'w') as f:
    f.write('Este é um teste de upload para o MinIO.')

# Fazer upload do arquivo no MinIO
try:
    s3.Bucket(bucket_name).upload_file(file_name, file_name)
    print(f"Arquivo {file_name} enviado com sucesso para o bucket {bucket_name}.")
except Exception as e:
    print(f"Erro ao enviar o arquivo: {e}")
