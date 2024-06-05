CONDA_ENV_NAME = poap
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh && conda activate
FLASK_APP_NAME = app 
CONDA_ENV_EXISTS := $(shell conda info --envs | grep $(CONDA_ENV_NAME))

REQUIREMENTS_FILE = requirements.txt

create_env:
	@if [ -z "$(CONDA_ENV_EXISTS)" ]; then \
		conda create -y -n $(CONDA_ENV_NAME) python=3.10; \
	fi

install:
	$(CONDA_ACTIVATE) $(CONDA_ENV_NAME) && pip install -r $(REQUIREMENTS_FILE)

start_app:
	$(CONDA_ACTIVATE) $(CONDA_ENV_NAME) && streamlit run $($(FLASK_APP_NAME)).py

run: create_env install start_app