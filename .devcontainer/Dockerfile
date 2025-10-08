# Use a mabbaforge image with conda pre-installed
FROM quay.io/condaforge/mambaforge:24.9.2-0

# Install the conda lock into the base environment
RUN conda install -y \
    conda-lock \
    && conda clean -tipy

# Install dependencies from conda-lock file into notebook environment
COPY conda-linux-64.lock conda-linux-64.lock
RUN conda update --all --solver=classic -n base -c conda-forge conda && \
    conda install -n notebook --file conda-linux-64.lock && \
    conda clean -tipy

# To use examples, add ipykernel and jupyterlab to notebook env
RUN conda install -n notebook -c conda-forge ipykernel jupyterlab

# Install the repo using pip from the notebook environment
RUN conda run -n notebook pip install https://github.com/cal-adapt/climakitae/archive/refs/tags/1.4.0.zip

# Keep container alive
CMD ["tail", "-f", "/dev/null"]