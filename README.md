#### Dev container

Due to annoying `jovyan` usergroup issues that continue to confuse me, this works only in a dev container on `codespaces` and will not work on your local machine, since you will not be able to create files or commit to the repo. 

#### Downloading CalAdapt data

1. `conda init` 
2. `conda activate base` in a new terminal
3. `python exploratory/download_caladapt.py` - you can also modify the download script to your liking, but I assume we will make this more of a CLI tool in the future so we should focus on the projection issues for now
4. Download the data from the repo to your local (should be relatively small). 