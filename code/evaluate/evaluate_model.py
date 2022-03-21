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
import os, json
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core.model import Model
import azureml.core
from azureml.core import Run
import argparse
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
# from sklearn.metrics import ConfusionMatrixDisplay
# Get workspace
# ws = Workspace.from_config()
run = Run.get_context()
exp = run.experiment
ws = run.experiment.workspace

parser = argparse.ArgumentParser("evaluate")
parser.add_argument(
    "--config_suffix", type=str, help="Datetime suffix for json config files"
)
parser.add_argument(
    "--json_config",
    type=str,
    help="Directory to write all the intermediate json configs",
)
args = parser.parse_args()

print("Argument 1: %s" % args.config_suffix)
print("Argument 2: %s" % args.json_config)

if not (args.json_config is None):
    os.makedirs(args.json_config, exist_ok=True)
    print("%s created" % args.json_config)

train_run_id_json = "run_id_{}.json".format(args.config_suffix)
train_output_path = os.path.join(args.json_config, train_run_id_json)
with open(train_output_path) as f:
    config = json.load(f)



new_model_run_id = config["run_id"]  # args.train_run_id
experiment_name = config["experiment_name"]
# exp = Experiment(workspace=ws, name=experiment_name)


try:
    model_list = Model.list(ws)
    production_model = next(
        filter(
            lambda x: x.created_time == max(model.created_time for model in model_list),
            model_list,
        )
    )
    production_model_run_id = production_model.tags.get("run_id")
    run_list = exp.get_runs()

    production_model_run = Run(exp, run_id=production_model_run_id)
    new_model_run = Run(exp, run_id=new_model_run_id)

    # ACCURACY
    accuracy_old = production_model_run.get_metrics().get("accuracy")
    accuracy_new = new_model_run.get_metrics().get("accuracy")
    print(f'accuracy of old model = {accuracy_old}')
    print(f'accuracy of new model = {accuracy_new}')
    
    # plot_data = {'old_model' : accuracy_old, 
    #              'new_model' : accuracy_new}
    # plt.bar(list(plot_data.keys()), list(plot_data.values()), width=0.2)
    
    print(f'The old model can be accurate {(accuracy_old)*100:.5} times out of 100')
    print(f'The new model can be accurate {(accuracy_new)*100:.5} times out of 100')
    
    # CONFUSION MATRIX
    confusion_matrix_old = production_model_run.get_metrics().get("confusion_matrix")
    confusion_matrix_new = new_model_run.get_metrics().get("confusion_matrix")
    print(confusion_matrix_old)
    # print(f'Old confusion matrix')
    # ConfusionMatrixDisplay(confusion_matrix_old).plot()
    
    print(f'The old model predicted class 0 correctly {confusion_matrix_old[0][0]} times')
    print(f'The old model predicted class 0 wrong {confusion_matrix_old[0][1]} times')
    print()
    print(f'The old model predicted class 1 wrong {confusion_matrix_old[1][0]} times')
    print(f'The old model predicted class 1 correctly {confusion_matrix_old[1][1]} times')
    print(confusion_matrix_new)
    # print(f'New confusion matrix')
    # ConfusionMatrixDisplay(confusion_matrix_new).plot()
    
    print(f'The new model predicted class 0 correctly {confusion_matrix_new[0][0]} times')
    print(f'The new model predicted class 0 wrong {confusion_matrix_new[0][1]} times')
    print()
    print(f'The new model predicted class 1 wrong {confusion_matrix_new[1][0]} times')
    print(f'The new model predicted class 1 correctly {confusion_matrix_new[1][1]} times')
    
    # RECALL
    recall_old_0 = production_model_run.get_metrics().get("recall_0")
    recall_old_1 = production_model_run.get_metrics().get("recall_1")
    recall_new_0 = new_model_run.get_metrics().get("recall_0")
    recall_new_1 = new_model_run.get_metrics().get("recall_1")
    
    print(f'recall old class 0 =  {recall_old_0*100:.5}')
    print(f'The old model is able to identify {recall_old_0*100:.5}% of all the class 0s in the dataset')
    print(f'recall old class 1 =  {recall_old_1*100:.5}')
    print(f'The old model is able to identify {recall_old_1*100:.5}% of all the class 1s in the dataset')
    
    print(f'recall new class 0 =  {recall_new_0*100:.5}')
    print(f'The old model is able to identify {recall_new_0*100:.5}% of all the class 0s in the dataset')
    print(f'recall new class 1 =  {recall_new_1*100:.5}')
    print(f'The old model is able to identify {recall_new_1*100:.5}% of all the class 1s in the dataset')
    
    # PRECISION
    precision_old_0 = production_model_run.get_metrics().get("precision_0")
    precision_old_1 = production_model_run.get_metrics().get("precision_1")
    precision_new_0 = new_model_run.get_metrics().get("precision_0")
    precision_new_1 = new_model_run.get_metrics().get("precision_1")
    
    print(f'precision class 0 =  {precision_old_0*100:.5}')
    print(f'The old model has been {precision_old_0*100:.5}% whenever it predicted class 0')
    print(f'precision class 1 =  {precision_old_1*100:.5}')
    print(f'The old model has been {precision_old_1*100:.5}% whenever it predicted class 1')
    
    print(f'precision class 0 =  {precision_old_0*100:.5}')
    print(f'The old model has been {precision_old_0*100:.5}% whenever it predicted class 0')
    print(f'precision class 1 =  {precision_new_1*100:.5}')
    print(f'The old model has been {precision_new_1*100:.5}% whenever it predicted class 1')

    promote_new_model = False
    if accuracy_new < accuracy_old:
        promote_new_model = True
        print("New trained model performs better, thus it will be registered")
except:
    promote_new_model = True
    print("This is the first model to be trained, thus nothing to evaluate for now")

run_id = {}
run_id["run_id"] = ""

if promote_new_model:
    run_id["run_id"] = new_model_run_id

run_id["experiment_name"] = experiment_name
filename = "run_id_{}.json".format(args.config_suffix)
output_path = os.path.join(args.json_config, filename)
with open(output_path, "w") as outfile:
    json.dump(run_id, outfile)