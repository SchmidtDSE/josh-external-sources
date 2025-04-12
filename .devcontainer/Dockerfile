# Use a jupyter base image
FROM quay.io/jupyter/minimal-notebook:ubuntu-24.04 AS base

## Grant user sudoer privileges
USER root
RUN groupadd -f jovyan && \
    usermod -g jovyan ${NB_USER} && \
    adduser ${NB_USER} sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >>/etc/sudoers

# Create directories with correct ownership
RUN mkdir -p /opt/share /workspace && \
    chown -R ${NB_USER}:jovyan /opt/share /workspace

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

# Install pip dependencies into conda environment
RUN conda run -n base pip install \
    xarray==2024.11.0 \
    xclim==0.54.0

# Install the repo
RUN pip install https://github.com/cal-adapt/climakitae/archive/refs/tags/1.2.3.zip

# Switch back to jovyan for normal operation
USER ${NB_USER}

# Keep container alive
CMD ["tail", "-f", "/dev/null"]