# ada_analysis
Repository to do data analysis

The file follow the CSV format. For each URL in a set, on a given system, we include the number of cycles and instructions 
needed to process the URL as well as many other attributes of the URL, including its protocol type, length of the path and so forth.
You can open CSV files in a spreadsheet tool.

The big_url_set is our default (github//ada-url/url-dataset/out.txt).

We process each URL 30 times, but not in sequence. We record the time needed to generate the normalized URL (href).

The benchmark done using `model_bench`. It only works under Linux because only under Linux can we get the fine grained precision we need to benchmark individual URL.

We do not need report the timings (ns) for precision reasons. Only the number of cycles and the number of instructions are reported.

## Systems

The rome machine refers to an AMD Rome server (AMD EPYC 7262 8-Core Processor) running Ubuntu with GCC 11.3. The m2 machine refers to a MacBook Air 2022 with LLVM 14.

## Python scripts


We require a recent Python 3 interpreter. The Python scripts require pandas, numpy, sklearn, seaborn and matplotlib. 
You may be able to install these dependencies with `pip` or `pip3` as follows:

```
pip install pandas matplotlib scikit-learn numpy seaborn
```

(Replace `pip` with `pip3` if needed.)


### Overall data (Google benchmark)


The overall data comes from various datasets and is produced by the google-benchmark executable `benchdata` from the main `ada-url/ada` repository.

You can process the overall data and generate the tables and figures.

```
python scripts/overall.py
```
(replace python by `python3` if needed)


### jsurl

The jsurl data refers to https://github.com/ada-url/js_url_benchmark



```
python scripts/jsurl.py
```
(replace python by `python3` if needed)