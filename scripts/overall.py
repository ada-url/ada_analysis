import pandas as pd
import matplotlib
import numpy as np
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
   answer = '{:g}'.format(float('{:.2g}'.format(x)))
   if len(answer) == 1:
      answer+=".0"
   return answer
excluded = {"node_files.json"} # excluded because curl does not support it and is messes our results.
#  ("BasicBench_AdaURL_href","ada::url"), for simpliciy
benchmarks=[ ("BasicBench_AdaURL_aggregator_href", "ada"), ("BasicBench_whatwg", "whatwg-url"), ("BasicBench_BoostURL", "Boost.URL"), ("BasicBench_ServoUrl", "rust-url"), ("BasicBench_CURL", "curl")]
datafiles = [datafile for datafile in os.listdir(rome_dir) if datafile.endswith('.json')]

datasets = []
speeds= {
    "ada": [],
    #"ada::url": [],
    "whatwg-url": [],
    "Boost.URL": [],
    "rust-url": [],
    "curl": []
}
for datafile in datafiles:
    if datafile in excluded:
        continue
    datasets.append(datafile.removesuffix(".json").replace("_", " "))
    with open(os.path.join(rome_dir, datafile)) as json_file:
      file_contents = json_file.read()
      print()
      print(datafile)
      print("{name} & {insperurl} & {cyclesperurl} & {inspercycle} \\\\".format(name = "name",insperurl= "instructions/url", cyclesperurl= "cycles/url", inspercycle = "instructions/cycle"))
      parsed_json = json.loads(file_contents)
      for benchmark_name in benchmarks:
         arr = parsed_json["benchmarks"]
         right_obj = None
         for obj in arr:
             if obj["name"] == benchmark_name[0]:
                 right_obj = obj
                 break
         obj = right_obj
         speeds[benchmark_name[1]].append(obj["url/s"]/1000000)
         print("{name} & {insperurl} & {cyclesperurl} & {inspercycle} \\\\".format(name = benchmark_name[1],insperurl= round(obj["instructions/url"]), cyclesperurl= round(obj["cycles/url"]), inspercycle = round(obj["instructions/cycle"])))


#ax.set_ylim(0, 250)

#plt.show()


matplotlib.rcParams['font.family'] = 'serif'
with PdfPages('rome.pdf') as pdf:
    x = np.arange(len(datasets))  # the label locations
    width = 0.15  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in speeds.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        #ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Millions of URLs per second')
    ax.set_xticks(x + width, datasets)
    ax.legend(loc='upper center', frameon=True, ncols=5, facecolor='white', framealpha=0.5, edgecolor='none',  bbox_to_anchor=(0.5, 1.05))
    ax.spines[['right', 'top']].set_visible(False)
    fig=ax.get_figure()
    pdf.savefig(fig)
