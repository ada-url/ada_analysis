#import pandas as pd
import matplotlib
import numpy as np
#import matplotlib.pyplot as plt
#import sklearn
#import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LinearRegression
#from sklearn.linear_model import Ridge
#from sklearn.linear_model import Lasso
#from sklearn.preprocessing import normalize
#from sklearn import metrics
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import os
import re
#import json
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i]//2, y[i], ha = 'center')

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir = script_dir.parent
jsurl_dir = os.path.join(root_dir, "jsurl")

def round(x):
   answer = '{:g}'.format(float('{:.2g}'.format(x)))
   if len(answer) == 1:
      answer+=".0"
   return answer

datasets = [("top100", 100031)]#, ("wikipedia_100k", 100000), ("linux_files", 169312), ("userbait", 11430), ("kasztp", 48009)]

def parse_file(lines):
    results = {}
    for line in lines:
        if line.startswith("runtime: "):
            runtime = (" ".join(line.split(" ")[1:3]))
            results[runtime] = {}
        elif line.startswith("fixtures"):
            tag = re.findall("/(.*)\.txt", line)[0]
            numbers = [float(x) for x in re.findall("[0-9]+\.[0-9]+",line)]
            results[runtime][tag]=numbers
    return results

for datafile in os.listdir(jsurl_dir):
    print("datafile:", datafile)
    print("=====================================")
    mainf = os.path.join(jsurl_dir, datafile)
    print(mainf)

    with open(mainf) as data_file:
        file_contents = data_file.read()
        print()
        print(datafile)
        results = parse_file(file_contents.split("\n"))
        #print(results)
        speeds= {}
        runtimes = ["node v20.1.0", "bun 0.5.9", "deno 1.32.5", "node v18.15.0"]
        for runtime in runtimes:
            print(runtime)
            speeds[runtime] = []
            for key,volume in datasets:
                time_in_ms_per_url = results[runtime][key][0]/volume
                millions_per_second = (1000/time_in_ms_per_url)/1000000
                speeds[runtime].append(millions_per_second)
                #print(key, millions_per_second)

        matplotlib.rcParams['font.family'] = 'serif'
        matplotlib.rcParams.update({'font.size': 13})

        with PdfPages("runtime"+datafile.split('.')[0]+'.pdf') as pdf:
            x = np.arange(len(datasets))  # the label locations
            width = 0.05  # the width of the bars
            multiplier = 0

            fig, ax = plt.subplots(layout='constrained')
            
            for attribute, measurement in speeds.items():
                print(attribute, measurement)
                offset = width * multiplier
                rects = ax.bar(x + offset, measurement, width, label=attribute)
                print(x[0] + offset, measurement[0])
                ax.text(x[0] + offset, measurement[0] + 0.05, attribute, ha = 'center')
                multiplier += 1
            ax.set_ylabel('Millions of URLs per second')
            ax.set_xticks(x + width, ['' for x in datasets])
            #ax.legend(loc='upper center', frameon=True, ncols=5, facecolor='white', framealpha=0.5, edgecolor='none',  bbox_to_anchor=(0.5, 1.05))
            ax.spines[['right', 'top']].set_visible(False)
            fig=ax.get_figure()
            pdf.savefig(fig)
#"node v18.15.0"
#rsion (20.0) with our parser is four times faster than the
#last version with the legacy URL parser (18.15)