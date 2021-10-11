
<a href="url"><img src="https://github.com/mihirbhaskar/save-the-pandas-intpython/blob/main/assets/savethepandas_logo.png" align="left" height="80" width="80" ></a>

# Steel City Services App - Team Save the Pandas

## About this app
This app allows users to search for nearby community services and upload their own information about such services.

## How to run this app
**Step 1:** Clone this repository

**Step 2:** Below is a list of packages used in the app. If you do not have any installed already, please install them:
- **Dash**, installed in conda by typing `conda install -c conda-forge dash` into Anaconda Prompt
- **geopy**, installed in conda by typing `conda install -c conda-forge geopy` into Anaconda Prompt
- **tkinter** (this should be default installed with conda)
- **tkinter.messagebox** (this should be default installed with conda)
- **csv** (this should be default installed with conda)
- **time** (a link to the library is [here](https://docs.python.org/3/library/time.html))
- **BeautifulSoup** (this should be default installed with conda)
- Other standard libraries: **pandas, numpy, json, requests**

**Step 3:** Run the script `app.py`. Before running it, make sure your working directory is at the root of the git repository you cloned. This way, there will be no path issues.

**Step 4:** If the app runs successfully, the Console should display *'Dash is running on http://{...}'*. Copy and paste the full http address in your browser and you should see the app running! 

## User instructions for the app
A video demonstrating how to use the app is [**here**](https://www.youtube.com/watch?v=dIFTxsJhcF8)

1. Enter your street address and click 'Submit'. A table should appear on the right panel of the screen. If the error message 'Invalid address' appears instead, this means your entered address did not find a location match using Google's API. Try entering it in a more standardised format, or just enter the name of the area you stay in.

2. Editing the maximum travel distance in miles and selecting/de-selecting the relevant categories will update the table dynamically (live). If you want to try with a new address, you will need to type in the address and click 'Submit' for it to register and update the table accordingly. Note that the travel distance in miles is calculated as the geodesic distance; that is, the length of the shortest path between your address' lat-long and the service's lat-long.

3. If you would like to add data, click the 'Submit Your Own Data' button. This will open a pop-up window titled 'Upload UI', with relevant fields to fill. The `name` and `vicinity` (i.e. street address ideally, or area name at the minimum) options are mandatory. Enter the data, and click `Upload`. If the address entered in `vicinity` cannot match to a location using Google's API, a warning message will pop-up asking you to enter a valid address. If you have entered a proper address and filled out the fields correctly, a prompt will ask if you want to upload the data. Clicking `OK' will add this data to the main database, and show a window saying 'Uploaded Successfully'. You can now close the data entry box.

4. Any data that was added using the Upload UI should automatically update and reflect in the live table displayed.

## Resources used
- [Dash Clinical Analytics App](https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-clinical-analytics/app.py) used as a template for styling; CSS style sheets cloned directly, and a similar design template used

---
---
 

## Contributor team instructions - setting up GitHub and using the repository

### Step 1: Install Git

You can browse through any of the many excellent online guides to Git to get a basic sense of what it's all about, such as this one [here](https://docs.github.com/en/get-started/quickstart).

Then, (a) Create a user account on the GitHub site, and (b) Install the latest version of Git from [here](https://git-scm.com/downloads). You can just use all the default installation options.

### Step 2 (optional, but recommended): Install SourceTree

[SourceTree](https://www.sourcetreeapp.com/) is a really nice visual representation of Git, so you don't have to use the ugly/hardcore black terminal screen to do things. During the set-up, it may ask you to also create a BitBucket account, but once that's done, you can link it to the GitHub account you created in Step 1 by clicking `Remote -> Add an account -> Refresh OAuth Token`, which will take you to a website to give SourceTree permission to interact with your account.

### Step 3: Create a local clone of the save-the-pandas repository
On SourceTree, under `Clone`, you can specify the Source Path / URL as `https://github.com/mihirbhaskar/save-the-pandas-intpython.git` (for future reference, you get this link from the top of this page on GitHub, under `Code -> HTTPS link`, your destination path as where you want the folder to sit on your Desktop (can be anywhere).

If you want to do this through code, you can also open Git Bash, change the directory to where you want the local clone using `cd {file path}` and then type `git clone https://github.com/mihirbhaskar/save-the-pandas-intpython.git`

This step should have created a physical folder with all the contents of the repository on your computer.

## Working on the repository

1. Pull changes from the remote everytime before you start working. I do this inside SourceTree, but you can also write `git pull origin master` in Git Bash

2. Work on the code or other files, saving changes normally

3. When you're done with your current session of work, under `File Status` in SourceTree, stage and commit the changes you made to the file. This lets you select the files you want to commit. Make the commit message nice and descriptive, but not too long.

4. Push the change. This will send your local changes to the master, up-to-date copy hosted on GitHub.

5. **If Step 4 does not work seamlessly, then it is likely that someone has made and pushed edits simultaneously, leading to a conflict**. In this case, you should first pull changes from the origin-master and **rebase** your changes on top. This can also be done within SourceTree, which will guide you through any conflicts you have to resolve. The workflow is best described in this [link](https://www.atlassian.com/git/tutorials/comparing-workflows) as the 'Centralized Workflow'.

