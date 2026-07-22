FROM ghcr.io/zephyrproject-rtos/ci:v0.27.4

ARG ZEPHYR_SDK_VERSION=0.16.8
ARG ZEPHYR_VERSION=v4.1.0

ENV ZEPHYR_SDK_INSTALL_DIR=/opt/zephyr-sdk-${ZEPHYR_SDK_VERSION}
ENV BSIM_OUT_PATH=/opt/bsim

# Initialize Zephyr workspace (CI image has toolchain but no source)
RUN mkdir -p /opt/zephyrproject && \
    cd /opt/zephyrproject && \
    west init -m https://github.com/zephyrproject-rtos/zephyr --mr ${ZEPHYR_VERSION} && \
    west update --narrow -o=--depth=1 && \
    west blobs fetch hal_nordic 2>/dev/null || true

ENV ZEPHYR_BASE=/opt/zephyrproject/zephyr
ENV PATH="${ZEPHYR_BASE}/scripts:${PATH}"

# Install Python tooling
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Managed Python must NOT live in /root (unreadable by the non-root runtime
# user) — pin it to a world-readable location before the first uv invocation.
ENV UV_PYTHON_INSTALL_DIR=/opt/uv/python

# Copy dependency files and source for install
COPY pyproject.toml .python-version uv.lock README.md ./
COPY src/ ./src/
ENV PATH="/root/.local/bin:${PATH}"
# Full sync (dev deps included): at runtime `uv run` then only audits the
# venv, so the container can run as ANY uid (compose sets user: to the
# host uid — root-owned files on the results/ mount break git on the host).
RUN uv python install 3.12 && \
    uv sync --frozen 2>/dev/null || uv sync

# Copy remaining project files
COPY . .

ENV EMBEDEVAL_ENABLE_BUILD=1
# Arbitrary-uid support: the runtime user has no /etc/passwd entry, so HOME
# and the uv cache must point at a world-writable location; UV_NO_SYNC keeps
# `uv run` from ever writing the root-owned venv.
ENV HOME=/tmp
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV UV_NO_SYNC=1

ENTRYPOINT ["uv", "run", "embedeval"]
