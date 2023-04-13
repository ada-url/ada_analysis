import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sklearn
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.preprocessing import normalize
from sklearn import metrics
import sys
from pathlib import Path


if(len(sys.argv) == 1):
    print("Please provide a filename")
    sys.exit(-1)

filename = sys.argv[1]


print("Reading file: " + filename)
base = Path(filename).stem
dirname = base+"_plots/"
Path(dirname).mkdir(parents=True, exist_ok=True)

data = pd.read_csv(filename, sep=",", comment='#')
data.columns = data.columns.str.lower().str.strip()

plots = True



def explain_r2(r2):
    if r2 > 0.75:
        return "Significant amount of variance explained"
    if r2 > 0.5:
        return "Good amount of variance explained"
    if r2 > 0.25:
        return "Small amount of variance explained"
    return "Little to no variance explained"

protocols = ["http", "not_special", "https", "ws", "ftp", "wss", "file"]

predictors = ["hash_size", "search_size",  "path_size", "port_size", "host_size", "credential"]
predicted_attribute = "mean_instr"

for predicted_attribute,name in [("best_instr", "instructions"), ("best_cycles", "cycles")]:
    print("=====================================")
    print("predicting ", predicted_attribute, " (", name, ")" )
    regressor = LinearRegression(fit_intercept=False, positive=True) 
    for protocol in range(8):
        print()
        thisframe = data[data["protocol"]==protocol]
        if thisframe.empty:
            continue
        print("protocol = ", protocol, " ", protocols[protocol])
        print("number of entries: ", len(thisframe.index))
        x = thisframe[predictors]
        y = thisframe[[predicted_attribute]]
        regressor.fit(x, y)
        r2 = regressor.score(x,y)
        print("R2 = ", r2, " (", explain_r2(r2), ")")
        print("Coefficients = ", regressor.coef_)
        for i in zip(predictors, regressor.coef_[0]):
            if i[1] > 0.000001:
                print("weight for ", i[0], " = ", i[1])
        print("Intercept = ", regressor.intercept_)

        with PdfPages(dirname+protocols[protocol]+'_predicted_'+name+'.pdf') as pdf:
                fig,ax = plt.subplots()
                ax.plot(thisframe['input_size'], thisframe[predicted_attribute], label="measured", linestyle='none', marker='.', markerfacecolor='blue', markersize=4)
                ax.plot(thisframe['input_size'], regressor.predict(x), label="predicted", linestyle='none', marker='x', markerfacecolor='red', markersize=4)

                ax.set_xlabel("URL size (bytes)")
                ax.set_ylabel(name)
                ax.spines[['right', 'top']].set_visible(False)
                ax.legend(loc='best', frameon=False)
                pdf.savefig(fig)



if plots:
    print ("Plotting...")
    data["best_instructions_per_cycle"] = data["best_instr"]/data["best_cycles"]
    matplotlib.rcParams['font.family'] = 'serif'
    with PdfPages(dirname+'instructions_per_cycle.pdf') as pdf:
        p=data.plot(x='input_size', y='best_instructions_per_cycle', linestyle='none',legend=False, marker='.', markerfacecolor='blue', markersize=4)
        p.set_xlabel("URL size (bytes)")
        p.set_ylabel("instructions per cycle")
        p.spines[['right', 'top']].set_visible(False)
        fig=p.get_figure()
        pdf.savefig(fig)

    data["best_instructions_per_byte"] = data["best_instr"]/data["input_size"]

    with PdfPages(dirname+'instructions_per_byte.pdf') as pdf:
        p=data.plot(x='input_size', y='best_instructions_per_byte', linestyle='none',legend=False, marker='.', markerfacecolor='blue', markersize=4)
        p.set_xlabel("URL size (bytes)")
        p.set_ylabel("instructions per byte")
        p.spines[['right', 'top']].set_visible(False)
        fig=p.get_figure()
        pdf.savefig(fig)

    data["best_cycles_per_cycle"] = data["best_cycles"]/data["input_size"]

    with PdfPages(dirname+'cycles_per_byte.pdf') as pdf:
        p=data.plot(x='input_size', y='best_cycles_per_cycle', linestyle='none',legend=False, marker='.', markerfacecolor='blue', markersize=4)
        p.set_xlabel("URL size (bytes)")
        p.set_ylabel("cycles per byte")
        p.spines[['right', 'top']].set_visible(False)
        fig=p.get_figure()
        pdf.savefig(fig)

print("plots in ", dirname)
