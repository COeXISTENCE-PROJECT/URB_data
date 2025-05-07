import os
import pandas as pd

def unify_results_to_one_df(files):
    """
    Unify multiple CSV files into a single DataFrame.
    
    Args:
        files (list): List of file paths to CSV files that have the same columns.

    Returns:
        pd.DataFrame: A single DataFrame containing all the data from the input files.
    """

    # Initialize an empty list to store DataFrames
    dfs = []

    # Loop through each file and read it into a DataFrame
    for file in files:
        # find file "BenchmarkMetrics.csv" in the folder, there can be multiple files
        if os.path.isfile(file):
            if file.endswith("BenchmarkMetrics.csv"):
                # Read the CSV file into a DataFrame
                df = pd.read_csv(file)
                # Append the DataFrame to the list
                dfs.append(df)

    if len(dfs) == 0:
        print("No CSV files found in the specified directory:", files)
        return pd.DataFrame()
    unified_df = pd.concat(dfs, ignore_index=True)
    
    return unified_df

def find_multiple_runs(path, save_path=None):
    """
    Given directory consists of multiple runs of several experiments.

    Runs are represented by folders named exp_1_<run_id>, exp_2_<run_id>, etc.
    Each folder contains a CSV file with the results of that run in dir metrics.

    Args:
        path (str): Path to the directory containing the experiment folders.

    Returns:
        None: Prints the unified DataFrame for each experiment.
    
    """

    # iterate over all folders in the given path
    experiments = {}
    for folder in os.listdir(path):
        if os.path.isdir(os.path.join(path, folder)):
            # add to the dictionary by the experiment name (everything before the last _)
            experiment_name = folder.rsplit('_', 1)[0]
            print(experiment_name)
            if experiment_name not in experiments:
                experiments[experiment_name] = [folder]
            else:
                experiments[experiment_name].append(folder)

    for experiment_name, folders in experiments.items():
        # iterate over all folders in the experiment
        files = []
        for folder in folders:
            # iterate over all files in the metrics folder
            metrics_folder = os.path.join(path, folder, 'metrics')
            if os.path.isdir(metrics_folder):
                for file in os.listdir(metrics_folder):
                    if file.endswith('.csv'):
                        files.append(os.path.join(metrics_folder, file))

        # unify the results into one dataframe
        if experiment_name == "pro_ipp":
            print(files)
        unified_df = unify_results_to_one_df(files)
        # print(f"Unified DataFrame for {experiment_name}:\n", unified_df)
        # mean over columns
        unified_df = unified_df.mean(axis=0)

        # save the dataframe to a csv file
        if save_path is not None:
            unified_df.to_csv(os.path.join(save_path, f'{experiment_name}.csv'), index=False)
        
        # print(f"Unified DataFrame for {experiment_name}:\n", unified_df)

if __name__ == "__main__":
    path = "./results/scenario1"
    save_path = "./results/res_scenario1"
    find_multiple_runs(path, save_path)