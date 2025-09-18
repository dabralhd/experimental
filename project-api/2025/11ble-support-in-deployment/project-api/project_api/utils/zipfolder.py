import tarfile
from asyncio import sleep, to_thread
from concurrent.futures import ThreadPoolExecutor
from typing import IO, Any
from zipfile import ZipFile

from more_itertools import chunked

from project_api.globals import EXTRACT_THREAD_POOL_MAX_SIZE
import logging
import os
import shutil
import errno

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# We need a large number of threads because most will be blocking on EFS io
_ex = ThreadPoolExecutor(EXTRACT_THREAD_POOL_MAX_SIZE)

async def unzip_folder(target_dir: str, tar_file_path: str):

    with tarfile.open(tar_file_path) as archive:
        return await to_thread(lambda: archive.extractall(target_dir))


def _extract_single_entry_sync(
    target_dir: str, archive: ZipFile, name: str
) -> Any:
    while True:
        try:
            archive.extract(name, target_dir)
            break
        # archive.extract may error out while creating parent folders;
        # in that case, we simply retry
        except FileExistsError as e:
            if e.filename == name:
                # In this case, we have a real (though strange) error
                raise e


async def unzip_folder_file(target_dir: str, archive_file: IO[bytes]) -> Any:
    archive = ZipFile(archive_file, "r")

    names_chunks = chunked(archive.namelist(), config.EXTRACT_THREAD_POOL_MAX_SIZE)

    for chunk in names_chunks:

        tasks = []

        for name in chunk:
            tasks.append(_ex.submit(
                _extract_single_entry_sync,
                target_dir,
                archive,
                name
            ))


        while not all((task.done() for task in tasks)):
            await sleep(0.1)


def zip_directory(out_zip_archive, in_dir_path):
    """
    Compresses the specified directory into a zip archive.

    Args:
        in_dir_path (str): The path to the input directory that needs to be compressed.
        out_zip_archive (str): The path where the output zip archive will be saved.

    Returns:
        int: Returns 0 if the directory was successfully compressed, 1 if an error occurred.

    Raises:
        Exception: If the input directory does not exist.
    """    
    logger.debug('Compressing directory into zip archive')
    if not os.path.exists(in_dir_path):
        logger.error(f'Directory {in_dir_path} does not exist')
        return errno.ENOENT
    
    try:
        shutil.make_archive(out_zip_archive, 'zip', in_dir_path)
        logger.debug(f'Directory {in_dir_path} compressed into zip archive {out_zip_archive}')
        return 0
    except Exception as e:
        # Handle specific error codes based on the type of failure
        logger.exception(f'Failed to compress directory {in_dir_path} into zip archive {out_zip_archive}. Error: {e}')
        raise e            