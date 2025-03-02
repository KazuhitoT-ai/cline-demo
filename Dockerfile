# Docker-in-Docker環境をベースとして使用
FROM ghcr.io/astral-sh/uv:latest as uv 

# 必要なパッケージをインストール（Python、uv、Gitなど）
FROM debian:12.8-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        git \
        clang \
        curl \
        gcc \
        vim

# https://github.com/cli/cli/blob/960f533234dcf327e1e9456c417f0b81ad09647c/docs/install_linux.md
RUN (type -p wget >/dev/null || (apt update && apt-get install wget -y)) \
    && mkdir -p -m 755 /etc/apt/keyrings \
        && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        && cat $out | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt update \
    && apt install gh -y

# 作業ディレクトリの設定
WORKDIR /app
COPY . . 

COPY --from=uv /uv /bin/uv 
RUN --mount=type=cache,target=/root/.cache/uv \
    uv python install 3.12 
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# uvを使ってPython環境をセットアップ
RUN uv venv /app/.venv

# 仮想環境のPATHを設定
ENV PATH="/app/.venv/bin:${PATH}"


# Dockerデーモンのポートを公開（任意、必要に応じて調整）
EXPOSE 2375

# デフォルトコマンドでDockerデーモン起動
CMD ["bash", "./docker-entrypoint.sh"]

