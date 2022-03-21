"""
Copyright (C) Microsoft Corporation. All rights reserved.​
 ​
Microsoft Corporation (“Microsoft”) grants you a nonexclusive, perpetual,
royalty-free right to use, copy, and modify the software code provided by us
("Software Code"). You may not sublicense the Software Code or any use of it
(except to your affiliates and to vendors to perform work on your behalf)
through distribution, network access, service agreement, lease, rental, or
otherwise. This license does not purport to express any claim of ownership over
data you may have shared with Microsoft in the creation of the Software Code.
Unless applicable law gives you more rights, Microsoft reserves all other
rights not expressly granted herein, whether by implication, estoppel or
otherwise. ​
 ​
THE SOFTWARE CODE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
MICROSOFT OR ITS LICENSORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THE SOFTWARE CODE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
# Importing all the required packages
from logging import exception
import os, json, datetime, sys, argparse
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice
from azureml.core.authentication import AzureCliAuthentication,InteractiveLoginAuthentication


cli_auth = AzureCliAuthentication()


# Get workspace
ws = Workspace.from_config('aml_config/aml_config.json',auth=cli_auth)


# Get the latest image details

try: 
    images = Image.list(workspace=ws)
    image = images[0]
except BaseException:
    print('No image to deploy')
    sys.exit(0)

print(
    "From image.json, Image used to deploy webservice on ACI: {}\nImage Version: {}\nImage Location = {}".format(
        image.name, image.version, image.image_location
    )
)


# Creating a container for ACI deployment
aciconfig = AciWebservice.deploy_configuration(
    cpu_cores=2,
    memory_gb=2,
    tags={"Problem": "image_noise_resolution", "Type": "image_classification"},
    description="Conatiner Image with image quality classification model",
    auth_enabled=True
)

# Defining ACI deployment name based on time
aci_service_name = "aciwebservice" + datetime.datetime.now().strftime("%m%d%H")


# Deploying the ACI service
service = Webservice.deploy_from_image(
    deployment_config=aciconfig, image=image, name=aci_service_name, workspace=ws, overwrite=True
)
service.wait_for_deployment(True)
print(
    "Deployed ACI Webservice: {} \nWebservice Uri: {}".format(
        service.name, service.scoring_uri
    )
)


# Saving the aci details
aci_webservice = {}
aci_webservice["aci_name"] = service.name
aci_webservice["aci_url"] = service.scoring_uri

with open("aml_config/aci_webservice.json", "w") as outfile:
    json.dump(aci_webservice, outfile)

print("Deploy on ACI Executed Successfully")