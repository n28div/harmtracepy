FROM haskell:7.10

WORKDIR /

COPY ./harmtrace ./harmtrace

WORKDIR /harmtrace

RUN stack build

ENTRYPOINT ["tail", "-f", "/dev/null"]