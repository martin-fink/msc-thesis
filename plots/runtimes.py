import os
import json

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Directory containing JSON files
data_directory = './data'

# Function to read and extract data from a JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to process data from all JSON files in a directory
def process_data(directory):
    benchmark_names = []
    means_ref = []
    means_memsafe = []
    means_bounds = []
    stddevs_ref = []
    stddevs_memsafe = []
    stddevs_bounds = []

    # Iterate over all files in the directory
    files = os.listdir(directory)
    files.sort()
    for filename in files:
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            data = read_json(file_path)

            # Check if there are an equal number of benchmarks for both implementations
            if len(data['results']) >= 2:
                benchmark_names.append(filename.split('.')[0])
                # means_ref.append(data['results'][i]['mean'])
                # stddevs_ref.append(data['results'][i]['stddev'])
                # means_memsafe.append(data['results'][i+1]['mean'])
                # stddevs_memsafe.append(data['results'][i+1]['stddev'])
                mean_memsafe = data['results'][0]['mean']
                stddev_memsafe = data['results'][0]['stddev']
                mean_ref = data['results'][1]['mean']
                stddev_ref = data['results'][1]['stddev']
                if len(data['results']) == 3:
                    mean_bounds = data['results'][2]['mean']
                    stddev_bounds = data['results'][2]['stddev']
                else:
                    mean_bounds = 0
                    stddev_bounds = 0

                scale = mean_ref / 100

                means_ref.append(mean_ref / scale)
                means_memsafe.append(mean_memsafe / scale)
                means_bounds.append(mean_bounds / scale)
                stddevs_ref.append(stddev_ref / scale)
                stddevs_memsafe.append(stddev_memsafe / scale)
                stddevs_bounds.append(stddev_bounds / scale)

    return benchmark_names, means_ref, stddevs_ref, means_memsafe, stddevs_memsafe, means_bounds, stddevs_bounds

# Processing the data
benchmark_names, means_ref, stddevs_ref, means_memsafe, stddevs_memsafe, means_bounds, stddevs_bounds = process_data(data_directory)

print("memsafe overhead = ", np.median(means_memsafe))
print("memsafe min = ", np.min(means_memsafe))
print("memsafe max = ", np.max(means_memsafe))
print("bounds overhead = ", np.median(means_bounds))
print("bounds min = ", np.min(means_bounds))
print("bounds max = ", np.max(means_bounds))

# Check if the lists have the same length
if len(means_ref) != len(means_memsafe):
    print("Mismatch in the number of benchmarks for wasm64 and wasm64+memsafety.")
else:
    # mpl.use('pgf')

    # Creating the plot
    plt.figure(figsize=(12, 5))
    plt.axhline(y=1, linestyle='--')

    x = np.arange(len(benchmark_names))  # the label locations
    width = 0.28  # the width of the bars

    # Creating bars for the wasm64 and wasm64+memsafetys
    bars1 = plt.bar(x - width, means_ref, width, yerr=stddevs_ref, hatch='///', label='(a) wasm64')
    bars2 = plt.bar(x, means_memsafe, width, yerr=stddevs_memsafe, hatch='\\\\\\', label='(b) wasm64+memsafety')
    bars3 = plt.bar(x + width, means_bounds, width, yerr=stddevs_bounds, hatch='...', label='(c) wasm64+mte-bounds')

    # plt.axhline(y=np.median(means_memsafe), linestyle='--')
    # plt.axhline(y=np.median(means_bounds), linestyle='-.')

    ax = plt.gca()
    ax.set_ylim([0.0, 120])
    ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter())

    # Adding labels, title, and legend
    plt.ylabel('Runtime (normalized)')
    plt.title('Lower is better ↓')
    plt.xticks(x, benchmark_names, rotation=45, ha='right')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=3)

    # plt.rcParams['text.usetex'] = True
    pgf_with_rc_fonts = {
        "font.family": "serif",
    }
    mpl.rcParams.update(pgf_with_rc_fonts)

    # Adjusting the x-axis limits
    padding = 0.5  # You can adjust this value to suit your needs
    ax.set_xlim([-width - padding, len(benchmark_names) - 1 + width + padding])

    # Displaying the plot
    plt.tight_layout()
    plt.savefig('runtimes.pdf', format="pdf")
    plt.show()
