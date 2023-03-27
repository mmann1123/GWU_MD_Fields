# GWU_MD_Fields

Codebase for yield predicitions at the Wye Research & Education Center

## Setup and Installation

Two main services (GitHub & Google Drive) as well as a virtual environment handler (Mamba) are necessary to operate this repository locally.

### GitHub

Clone this the GitHub repository this README is housed in (found [here](https://github.com/mmann1123/GWU_MD_Fields)) into a location of your choosing.

### Google Drive

Navigate to this [link](https://drive.google.com/drive/folders/1AQizUtf8_RJ6uRiuUR4BkrSK1pkSzoJp?usp=sharing) and copy that folder (marked "raw") into the GWU_MD_Fields/data/ folder. For reference, it should be in the same spot as the file named "RAW GOES HERE". This imported folder is quite large, so downloading it will take a while. It contains all raw data for this project.

### Mamba

Navigate to this [link](https://mamba.readthedocs.io/en/latest/installation.html) and use the installation method of your choice to download Mamba.

Once Mamba has been installed, run `mamba env create --file=env.yml` from the root of this repository. This command references a prepared YML file with the list of all necessary packages for this project to function. If there any dependency or priviledge issues, you will have to sort them out manually, as each machine is different. Once the environment has been created, however, each machine should be running under similar, if not identitical, environments, and so actions that work on one machine should work on all others.

In order to activate (and use) this new environment, run `mamba activate wye_research`. There should be a clear indication on your command line that this new environment is active. To exit this environment, run `mamba deactivate`. If new packages need to be installed, it is greatly preferred to use the Mamba package manager, rather than another. Refer to the docs below on how to do this. If packages are added to the necessary list, make it clear in an individual commit that the `env.yml` file has been updated.

For further documentation for Mamba, head to the main [Mamba Docs](https://mamba.readthedocs.io/en/latest/index.html#) and/or the [docs of its parent package, Conda](https://docs.conda.io/projects/conda/en/stable/commands.html).
