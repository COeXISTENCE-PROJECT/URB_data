import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import glob
from collections import defaultdict
from collections import OrderedDict, defaultdict
import warnings
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
warnings.filterwarnings("ignore", category=RuntimeWarning, message="Mean of empty slice")

def smooth_series(series, window=3, valid_start_index=0):
    series = np.array(series, dtype='float')
    series[:valid_start_index] = np.nan
    smoothed = pd.Series(series).rolling(window=window, min_periods=1, center=False).mean()
    return smoothed.to_numpy()

def extract_episode_number(filename):
    match = re.search(r'ep(\d+)\.csv', os.path.basename(filename))
    return int(match.group(1)) if match else float('inf')

def get_travel_times_by_kind(folder_path, agent_kind, baselines=False):
    times = []
    episode_folder = os.path.join(folder_path, 'episodes')
    csv_files = sorted(
        glob.glob(os.path.join(episode_folder, 'ep*.csv')),
        key=extract_episode_number
    )
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            if 'kind' in df.columns and 'travel_time' in df.columns:
                subset = df[df['kind'] == agent_kind]
                avg_travel_time = subset['travel_time'].mean()
                if baselines == False:
                    times.append(avg_travel_time)
                elif not pd.isna(avg_travel_time):
                    times.append(avg_travel_time)
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
    return times

def compute_asymmetric_stats(all_runs, max_len):
    # Pad with NaN for unequal lengths
    padded = [run + [np.nan] * (max_len - len(run)) for run in all_runs]
    data = np.array(padded)

    # Compute mean across folders
    with np.errstate(invalid='ignore'):
        mean = np.nanmean(data, axis=0)

    # Compute std dev above and below mean
    upper_std = np.full_like(mean, np.nan)
    lower_std = np.full_like(mean, np.nan)
    for i in range(data.shape[1]):
        col = data[:, i]
        col = col[~np.isnan(col)]
        above = col[col > mean[i]]
        below = col[col < mean[i]]
        upper_std[i] = np.std(above) if len(above) > 0 else 0
        lower_std[i] = np.std(below) if len(below) > 0 else 0

    return mean, lower_std, upper_std

def calculate_extravaganza(folder_path):
    # Use glob to find and sort files matching 'ep*.csv'
    csv_files = sorted(glob.glob(os.path.join(folder_path, 'ep*.csv')),
                       key=lambda x: int(os.path.splitext(os.path.basename(x))[0][2:]))  # extract number after 'ep'
    
    # Take the last 100 files
    last_100_files = csv_files[-100:]
    
    av_travel_times = []

    for file_path in last_100_files:
        try:
            df = pd.read_csv(file_path)
            if 'kind' in df.columns and 'travel_time' in df.columns:
                av_rows = df[df['kind'] == 'AV']
                av_travel_times.extend(av_rows['travel_time'].dropna().tolist())
            else:
                print(f"Missing required columns in {file_path}")
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")
    
    # Compute and return the average travel time of AVs
    if av_travel_times:
        return sum(av_travel_times) / len(av_travel_times)
    else:
        print("No AV travel time data found.")
        return None

from matplotlib import rcParams
from statistics import mean, stdev
import numpy as np

rcParams['font.family'] = 'Times New Roman'

# Set your actual parent directory here
parent_dir = os.path.abspath('results/scenario2')

# Define suffixes and their readable labels
group_suffixes = ['_ipp', '_iql', '_map', '_qmi']
suffix_labels = {
    '_ipp': 'IPPO',
    '_iql': 'IQL',
    '_map': 'MAPPO',
    '_qmi': 'QMIX'
}

# Define city prefixes and their readable names
city_prefixes = OrderedDict([
    ('sai', 'Saint Arnoult (89 AVs)'),
])


# Define known baselines and labels
baseline_suffixes = ['_aon', '_ran']
baseline_labels = {
    '_aon': 'All-Or-Nothing',
    '_ran': 'Random'
}
baseline_styles = {
    '_aon': {'color': 'slategray', 'linestyle': '--'},
    '_ran': {'color': 'black', 'linestyle': '--'}
}

# Define color palette for algorithms
colors = ["firebrick", "teal", "peru", "navy", "salmon", "slategray", "darkviolet"]
color_map = {suffix: colors[i] for i, suffix in enumerate(group_suffixes)}

# Group folders by city and algorithm
city_groups = OrderedDict()
for city_prefix in city_prefixes:
    city_groups[city_prefix] = defaultdict(list)

for folder in os.listdir(parent_dir):
    folder_path = os.path.abspath(os.path.join(parent_dir, folder))
    if os.path.isdir(folder_path):
        for city_prefix in city_prefixes:
            if folder.startswith(f'{city_prefix}_'):
                for suffix in group_suffixes:
                    if suffix in folder:
                        city_groups[city_prefix][suffix].append(folder_path)
                        break

# Collect baseline folders separately
baseline_groups = defaultdict(dict)
for folder in os.listdir(parent_dir):
    folder_path = os.path.abspath(os.path.join(parent_dir, folder))
    if os.path.isdir(folder_path):
        for city_prefix in city_prefixes:
            for baseline_suffix in baseline_suffixes:
                if folder == f'{city_prefix}{baseline_suffix}':
                    baseline_groups[city_prefix][baseline_suffix] = folder_path

# Create subplots (3 cities)
fig, ax = plt.subplots(figsize=(5, 4))
plt.subplots_adjust(wspace=0.1)

for i, (city_prefix, alg_groups) in enumerate(city_groups.items()):
    city_name = city_prefixes[city_prefix]
    avg_human_tt_list = []
    print(city_prefix)
    for suffix, folders in alg_groups.items():
        color = color_map.get(suffix, None)
        label = suffix_labels.get(suffix, suffix.upper())

        # Store all normalized AV runs for the current algorithm
        av_normalized_runs = []

        for idx, folder in enumerate(folders):
            print(idx, folder)
            
            ## Humans 
            #human_run = get_travel_times_by_kind(folder, 'Human')
            #human_slice = human_run[30:39]
            #avg_human_tt = sum(human_slice) / len(human_slice)
            #avg_human_tt_list.append(avg_human_tt)
            
            ## AVs 
            av_run = get_travel_times_by_kind(folder, 'AV')
            start_index = 0  # AVs appear after episode 40
            av_run = [val if idx >= start_index else np.nan for idx, val in enumerate(av_run)]
            #av_run = [val / avg_human_tt for val in av_run]
            
            if not av_run:
                continue

            av_smoothed = smooth_series(av_run, window=35, valid_start_index=0)
            x = [i * 5 for i in range(len(av_smoothed))]

            if idx == 1:
                ax.plot(x, av_smoothed, label=f'{label} (AV)', color=color, linewidth=2)
            #else:
            #    ax.plot(x, av_smoothed, color=color, linewidth=1, alpha=0.5)


    # Plot the last human agent with dashed line
    #human_travel_times = [val / avg_human_tt for val in human_run]
    #smooothed_humans = smooth_series(human_travel_times, window=35, valid_start_index=0)
    #x_humans = [i * 5 for i in range(len(smooothed_humans))]
    #ax.plot(x_humans, smooothed_humans, label='Humans', color='salmon', linestyle='-', linewidth=2)

    # Compute the avg human tt for all the algorithms
    #avg_all_algos_humans_tt = sum(avg_human_tt_list) / len(avg_human_tt_list) 
            
    ### Calculate the baseline lines        
    if city_prefix in baseline_groups:
        for baseline_suffix, folder_path in baseline_groups[city_prefix].items():
            av_times = get_travel_times_by_kind(folder_path, 'AV', baselines=True)
            if not av_times:
                continue

            ## Normalize with the avg human travel time of the last episodes folder 
            #av_times = [val / avg_all_algos_humans_tt for val in av_times]

            ## Find the average"""
            average = sum(av_times) / len(av_times) if av_times else float('nan')
            x = [average] * 6100

            label = baseline_labels.get(baseline_suffix, baseline_suffix.upper())
            style = baseline_styles.get(baseline_suffix, {'color': 'black', 'linestyle': '--'})

            ax.plot(x, label=f'{label} (AV)', **style, linewidth=3)

    ##S Add a horizontal line at y=1 
    #ax.axhline(y=1, color='black', linestyle='-', linewidth=2)

    #S# Add background colour
    #ax.axvspan(0, 200, color='lightgrey', alpha=0.4, label='Human Leaning', zorder=0)
    ax.axvspan(0, 6000, color='white', alpha=0.4, label='Machine Leaning', zorder=0)
    ax.axvspan(6000, 6100, color='lightblue', alpha=0.4, label='Testing phase', zorder=0)

    ### Calculate extravaganze points
    if city_prefix == "ing":
        folder = "results/scenario2_long/" + city_prefix + "_qm2_xl_1/episodes"
    elif city_prefix == "pro":
        folder = "results/scenario2_long/" + city_prefix + "_qm2_xl_0/episodes"
    else:
        folder = "results/scenario2_long/" + city_prefix + "_qm2_xl_2/episodes"

    #extravaganza = calculate_extravaganza(folder)
    #normalized_extravaganze = extravaganza / avg_all_algos_humans_tt

    ### Add extravaganze points
    #ax.plot(6300, normalized_extravaganze, marker='v', color='navy', label='Qmix longer training', markersize=10)

    ### Ticks params and titles
    ax.tick_params(axis='both', labelsize=14)
    #ax.set_yticks([1, 1.1, 1.2])
    ax.set_title(f"{city_name}", fontsize=20)
    if idx == 1:
        ax.set_xlabel("episodes", fontsize=20)


    #ax.set_xticks([0, 1000, 2000, 3000, 4000, 5000, 6000, 6800])
    ax.set_xlim(0, 6100)
    #ax.set_xticklabels(['0', '1000', '2000', '3000', '4000', '5000', '6000', '...20300'])

    ### Adjust grid params
    ax.minorticks_on()
    ax.grid(axis='y', which='minor', color='gray', linestyle=(0,(1,1)), linewidth=0.6, alpha=0.8, zorder=100)
    ax.grid(axis='y', color='gray', linewidth=1.0, alpha=0.8, zorder=100)


    ### Set y axis label only on the rightest plot
    if i == 0:
        ax.set_ylabel("Mean travel time", fontsize=20)
        """phases_legend = [
            Patch(facecolor='none', edgecolor='none', label='Phases:'),  # header
            Patch(facecolor='lightgrey', alpha=0.4, label='   Human learning'),
            Patch(facecolor='white', edgecolor='black', alpha=0.4, label='   Machine learning'),
            Patch(facecolor='lightblue', alpha=0.4, label='   Testing phase'),
        ]"""
        #ax.legend(handles=phases_legend, loc='upper left', ncol = 2, frameon=False, fontsize=14)

    """if i == 1:

        legend1 = [
            Patch(facecolor='none', edgecolor='none', label='MARL algorithms:'),
            Line2D([0], [0], color='firebrick', lw=2, label='IPPO'),
            Line2D([0], [0], color='teal', lw=2, label='IQL'),
            Patch(facecolor='none', edgecolor='none', label=' '),
            Line2D([0], [0], color='peru', lw=2, label='MAPPO'),
            Line2D([0], [0], color='navy', lw=2, label='QMIX'),
            Line2D([0], [0], marker='v', color='navy', linestyle='None', markersize=10, label='Qmix longer training')
        ]
        #ax.legend(handles=legend1, loc='upper left', ncol=2, frameon=False, fontsize=14)
        
    if i == 2:

        # Create a header (invisible patch, used just for labeling the group)
        legend2 = [
            Patch(facecolor='none', edgecolor='none', label='Baselines:'),
            Line2D([0], [0], color='slategray', linestyle = '--', lw=2, label='All-Or-Nothing'),
            Patch(facecolor='none', edgecolor='none', label=' '),
            Line2D([0], [0], color='black', lw=2, linestyle = '--', label='Random'),
            Line2D([0], [0], color='salmon', lw=2, label='Humans'),
        ]"""
        #ax.legend(handles=legend2, loc='upper left', ncol = 2, frameon=False, fontsize=14)
        

### Add a central legend for the whole plot
plt.subplots_adjust(top=0.7) 
handles, labels = ax.get_legend_handles_labels()

legend_elements = [
    # Column 1: MARL algorithms
    Patch(facecolor='none', edgecolor='none', label=r'$\mathbf{MARL\ algorithms}$'),
    Line2D([0], [0], color='firebrick', lw=2, label='IPPO'),
    Line2D([0], [0], color='teal', lw=2, label='IQL'),
    Line2D([0], [0], color='peru', lw=2, label='MAPPO'),
    Patch(facecolor='none', edgecolor='none', label=' '),
    Line2D([0], [0], color='navy', lw=2, label='QMIX'),
    Line2D([0], [0], marker='v', color='navy', linestyle='None', markersize=10, label='Qmix longer training'),
    Patch(facecolor='none', edgecolor='none', label=' '),

    # Column 2: Baselines
    Patch(facecolor='none', edgecolor='none', label=r'$\mathbf{Baselines}$'),
    Line2D([0], [0], color='slategray', linestyle='--', lw=2, label='All-Or-Nothing'),
    Line2D([0], [0], color='black', linestyle='--', lw=2, label='Random'),
    Line2D([0], [0], color='salmon', lw=2, label='Humans'),

    # Column 3: Phases
    Patch(facecolor='none', edgecolor='none', label=r'$\mathbf{Phases}$'),
    Patch(facecolor='lightgrey', alpha=0.4, label='Human learning'),
    Patch(facecolor='white', edgecolor='black', alpha=0.4, label='Machine learning'),
    Patch(facecolor='lightblue', alpha=0.4, label='Testing phase'),
]

#fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=4, fontsize=12, frameon=False)
#fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4, fontsize=12, frameon=False)

## Add the legend on top
"""legend_elements = [
    Patch(facecolor='none', edgecolor='none', label='Baselines:'),
    Line2D([0], [0], color='slategray', linestyle = '--', lw=2, label='All-Or-Nothing'),
    Line2D([0], [0], color='black', lw=2, linestyle = '--', label='Random'),
    Patch(facecolor='none', edgecolor='none', label='MARL algorithms:'),
    Line2D([0], [0], color='firebrick', lw=2, label='IPPO'),
    Line2D([0], [0], color='teal', lw=2, label='IQL'),
    Line2D([0], [0], color='peru', lw=2, label='MAPPO'),
    Line2D([0], [0], color='navy', lw=2, label='QMIX')
]"""

fig.savefig('images/100_per_avs.png', dpi=300, bbox_inches='tight')  # Change filename and format as needed