FROM python:3.12.11-slim-bookworm

ARG user=retail_crm_integration
ARG user_dir=/home/${user}

RUN set -e && apt update -y && apt install -y curl && rm -rf /var/lib/apt/lists/*

RUN set -e && adduser --system --group --disabled-password --home ${user_dir} ${user}
RUN set -e && mkdir -p ${user_dir} ${user_dir}/src && chown -R ${user} ${user_dir}

RUN set -e && pip install poetry==2.1.4

ENV PATH="${user_dir}/.local/bin:$PATH"

COPY ./pyproject.toml ./poetry.lock ${user_dir}/

WORKDIR ${user_dir}/src

RUN set -e && poetry config virtualenvs.create false && poetry install --no-interaction --only main --no-root

COPY --chown=${user} ./src ${user_dir}/src

USER ${user}

CMD ["python", "main.py"]
