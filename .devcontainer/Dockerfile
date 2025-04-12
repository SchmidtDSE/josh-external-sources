# Use a jupyter base image
FROM quay.io/jupyter/minimal-notebook:ubuntu-24.04 AS base

# Install the conda lock into the base environment
RUN conda install -y \
    conda-lock \
    && conda clean -tipy

# Install dependencies from conda-lock file into base environment
COPY conda-linux-64.lock conda-linux-64.lock
COPY environment.yml environment.yml
RUN conda update --all --solver=classic -n base -c conda-forge conda && \
    conda env update --file environment.yml && \
    conda clean -tipy

# According to docs (https://github.com/cal-adapt/climakitae/wiki/Installing-climakitae-(1.2.2)-locally-using-conda-environment),
# install a few pip dependencies into conda environment
RUN conda run -n base pip install \
    xarray==2024.11.0 \
    xclim==0.54.0

# Finally, pip install the repo itself at 1.2.2
RUN pip install https://github.com/cal-adapt/climakitae/archive/refs/tags/1.2.3.zip

# Keep container alive
CMD ["tail", "-f", "/dev/null"]