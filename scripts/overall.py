import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.preprocessing import normalize
from sklearn import metrics
import sys
from pathlib import Path
import os
import json

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir = script_dir.parent

overall_dir = os.path.join(root_dir, "overall")

rome_dir = os.path.join(overall_dir, "rome")

def round(x):
   return '{:g}'.format(float('{:.2g}'.format(x)))

benchmarks=[ ("BasicBench_AdaURL_aggregator_href", "ada::url_aggregator"), ("BasicBench_AdaURL_href","ada::url"), ("BasicBench_CURL", "curl"), ("BasicBench_BoostURL", "Boost.URL"), ("BasicBench_ServoUrl", "rust-url"), ("BasicBench_whatwg", "whatwg-url")]
datafiles = [datafile for datafile in os.listdir(rome_dir) if datafile.endswith('.json')]
for datafile in datafiles:
    with open(os.path.join(rome_dir, datafile)) as json_file:
      print(datafile.removesuffix(".json"), json_file)
      file_contents = json_file.read()
      parsed_json = json.loads(file_contents)
      for benchmark_name in benchmarks:
         arr = parsed_json["benchmarks"]
         right_obj = None
         for obj in arr:
             if obj["name"] == benchmark_name[0]:
                 right_obj = obj
                 break
         obj = right_obj
         print("{name} & {insperurl} & {cyclesperurl} & {inspercycle} \\\\".format(name = benchmark_name[1],insperurl= round(obj["instructions/url"]), cyclesperurl= round(obj["cycles/url"]), inspercycle = round(obj["instructions/cycle"])))

