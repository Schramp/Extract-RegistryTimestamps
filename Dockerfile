FROM nexus.dev.holmes.nl:5000/hansken/python:3.8-slim AS base

FROM base AS builder

ARG PIP_INDEX_URL="https://nexus.dev.holmes.nl/repository/pypi-all/simple"

RUN mkdir -p /install
COPY dist distribution

RUN pip install --prefix='/install' --no-warn-script-location --index-url=${PIP_INDEX_URL} distribution/*.whl


FROM base

LABEL maintainer="r.schramp@nfi.nl"
# plugin discovery aid
LABEL hansken.extraction.plugin.image="hansken-extraction-plugin-registryTS"
LABEL hansken.extraction.plugin.name="RegistryFiletimePlugin"

COPY --from=builder /install /usr/local
COPY /plugin /

EXPOSE 8999

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["serve_plugin 'registry_filetime_plugin.py' 8999"]
