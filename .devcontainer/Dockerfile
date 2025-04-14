# Use a jupyter base image
FROM quay.io/pangeo/base-image AS base

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

# To use examples, add ipykernel to base env
RUN conda install -n base -c conda-forge ipykernel

# Install the repo using pip from the base environment
RUN conda run -n base pip install https://github.com/cal-adapt/climakitae/archive/refs/tags/1.2.3.zip

# Keep container alive
CMD ["tail", "-f", "/dev/null"]