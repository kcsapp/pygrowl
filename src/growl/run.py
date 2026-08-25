import logging
import shutil
import subprocess as sp
from enum import Enum, auto
from pathlib import Path

import docker
from docker.errors import ImageNotFound
from docker.types import Mount

from .config import CompasOptions

logger = logging.getLogger(__name__)

_INPUT_FILE_ARGS = ("grid", "logfile_definitions", "timesteps_filename")
_OUTPUT_FILE_ARGS = ("output_path",)


def run_compas_binary(
    options: CompasOptions,
    input_dir: str = "data/input",
    logs_dir: str = "data/logs",
) -> bytes:
    """Run the COMPAS command in a local shell with the specified options.

    Args:
        options (CompasOptions | None): Non-default arguments to pass to the command (default: None)
        input_dir (str, optional) : Name of the input directory (default: "data/input")
        logs_dir (str, optional): Name of the logs directory (default: "data/logs")

    Returns:
        bytes: stdout of the command
    """
    # Construct absolute paths for input_dir and logs_dir, then localize the path-like options
    # If absolute path values are provided, the `pwd / ` prefix will be ignored
    local_pwd = Path.cwd()
    local_inputs, local_logs = local_pwd / input_dir, local_pwd / logs_dir
    local_inputs.mkdir(parents=True, exist_ok=True)
    local_logs.mkdir(parents=True, exist_ok=True)

    localized_options = options.localize(str(local_inputs), _INPUT_FILE_ARGS).localize(
        str(local_logs), _OUTPUT_FILE_ARGS, as_default=True
    )

    # Prepare the command to run inside the container
    cmd = localized_options.to_argv(remove_defaults=True)

    # Run the command
    cp = sp.run(cmd, capture_output=True, check=True)
    return cp.stdout


def run_compas_docker(
    options: CompasOptions,
    input_dir: str = "data/input",
    logs_dir: str = "data/logs",
    repo: str = "teamcompas/compas",
    tag: str = "latest",
) -> bytes:
    """Run the COMPAS command in a Docker container with the specified options.

    Mimics this docker run command:

    docker run --rm -it -v $PWD/input:/app/input -v $PWD/logs:/app/logs teamcompas/compas compas {args}

    Args:
        input_dir (str, optional) : Name of the input directory (default: "data/input")
        logs_dir (str, optional): Name of the logs directory (default: "data/logs")
        args (MutableMapping[str, Any] | None, optional): Arguments to pass to the command (default: None)
        repo (str, optional): Docker image repository to use (default: "teamcompas/compas")
        tag (str | None, optional): Image tag from the above repository to use (default: "latest")

    Returns:
        bytes: Container logs returned
    """
    client: docker.DockerClient = docker.from_env()
    image: str = f"{repo}:{tag}"

    try:
        client.images.get(image)
    except ImageNotFound:
        logger.warning(f"Image {image} not found locally; pulling it from docker hub")
        client.images.pull(image)

    # Construct absolute paths for input_dir and logs_dir.
    # If absolute path values are provided, the `pwd / ` prefix will be ignored
    local_pwd, docker_pwd = Path.cwd(), Path("/app")
    local_inputs, local_logs = local_pwd / input_dir, local_pwd / logs_dir
    docker_inputs, docker_logs = docker_pwd / input_dir, docker_pwd / logs_dir

    # Create mounts for the inputs & logs paths
    local_inputs.mkdir(parents=True, exist_ok=True)
    local_logs.mkdir(parents=True, exist_ok=True)
    mounts = [
        Mount(source=str(local_inputs), target=str(docker_inputs), type="bind"),
        Mount(source=str(local_logs), target=str(docker_logs), type="bind"),
    ]

    # Ensure the inputs & logs paths are reflected in the appropriate arguments
    localized_options = options.localize(str(docker_inputs), _INPUT_FILE_ARGS).localize(
        str(docker_logs), _OUTPUT_FILE_ARGS, as_default=True
    )

    # Prepare the command to run inside the container
    cmd = localized_options.to_argv(remove_defaults=True)

    # Run the container
    container: bytes = client.containers.run(
        image=image,
        command=cmd,
        mounts=mounts,
        remove=True,
        stdout=True,
        stderr=True,
        detach=False,
    )
    return container


class RunMode(Enum):
    BINARY = auto()
    DOCKER = auto()
    DEFAULT = auto()


def run_compas(
    options: CompasOptions,
    input_dir: str = "data/input",
    logs_dir: str = "data/logs",
    mode: RunMode = RunMode.DEFAULT,
) -> bytes:
    """Run the COMPAS command with the specified options.

    Args:
        options (CompasOptions | None): Non-default arguments to pass to the command (default: None)
        input_dir (str, optional) : Name of the input directory (default: "input")
        logs_dir (str, optional): Name of the logs directory (default: "logs")

    Returns:
        bytes: Output of the command
    """
    match mode:
        case RunMode.BINARY:
            return run_compas_binary(options, input_dir, logs_dir)
        case RunMode.DOCKER:
            return run_compas_docker(options, input_dir, logs_dir)
        case RunMode.DEFAULT:
            return (
                run_compas_binary(options, input_dir, logs_dir)
                if shutil.which("COMPAS")
                else run_compas_docker(options, input_dir, logs_dir)
            )
