# save-the-pandas-intpython :panda_face:
## Setting up the repository

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

