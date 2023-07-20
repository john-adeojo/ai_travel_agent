# Flight Demo Environment Setup

## Step 1: Download the environment.yml file

## Step 2: Create Conda Environment

Open your Anaconda Powershell and run the following command:

```bash
conda env create -f environment.yml


This will create a new Conda environment based on the `environment.yml` file.

## Step 3: Clone the GitHub Repo

Navigate to the environment folder which should be at `../anaconda3/envs/flight_demo_env/` and clone the GitHub repository into this environment.

## Step 4: Activate the Conda Environment

In your Anaconda Powershell, navigate to the cloned environment and activate it with the following command:

```bash
conda activate flight_demo_env


## Step 5: Update utils.py

Once the environment is activated, you need to update the `utils.py` to navigate to the `apikeys.yml` file. Do this by typing `jupyter-lab` in your Anaconda Powershell. 

Once the session is open, navigate to `utils.py` and change the `scrip_dir` on line 26 to your own directory. 

**Important: Make sure you have entered your own Amadeus API Key and Secret in the `apikeys.yml` file.**

Save the `utils.py` file after making these changes.

## Step 6: Run the Application

You can open a terminal from within Jupyter Labs and run the following command:

```bash
streamlit run front_end.py


This will start the Streamlit application. Enjoy exploring!
