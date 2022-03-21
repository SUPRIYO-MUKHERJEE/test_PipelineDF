import re
import subprocess
import os

#from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
#from azure.containerregistry import ContainerRegistryClient
from configparser import ConfigParser
file = 'config.ini'
config = ConfigParser()
config.read(file)
os.environ["AZURE_CLIENT_ID"]=config['azure_cred']['CLIENT_ID']
os.environ["AZURE_TENANT_ID"]=config['azure_cred']['TENANT_ID']
os.environ["AZURE_CLIENT_SECRET"]=config['azure_cred']['CLIENT_SECRET']
#keyVaultName = config['azure_cred']['KEY_VAULT_NAME']
#KVUri = f"https://{keyVaultName}.vault.azure.net"
credential = DefaultAzureCredential()
#global client
account_url = "https://3107e6123ca042ca8691f618af7d5dd2.azurecr.io"
#client = ContainerRegistryClient(account_url, DefaultAzureCredential())
#subprocess.run(["sudo chmod +x shell.sh"])
#subprocess.run(["./mlshell.sh"],shell=True)
print("sandhya")
