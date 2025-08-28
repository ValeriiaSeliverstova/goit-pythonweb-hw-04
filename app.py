import asyncio
import argparse
from pathlib import Path
from aiopath import AsyncPath
from aioshutil import copyfile
from logger import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


def parsing_args():
    parser = argparse.ArgumentParser(description="Directory Sorting Script")
    parser.add_argument("-s", "--source", help="Source folder")
    parser.add_argument("-o", "--output", help="Destination folder")
    args = parser.parse_args()

    if not args.source:
        args.source = input("Enter path to source folder: ").strip()
    if not args.output:
        args.output = input("Enter path to destination folder: ").strip()

    return args


async def read_folder(path: AsyncPath) -> list[AsyncPath]:
    tasks = []
    async for el in path.iterdir():
        if await el.is_dir():
            tasks.extend(await read_folder(el))
        else:
            tasks.append(el)

    return tasks


async def copy_file(file_path: AsyncPath, dst: AsyncPath):
    ext = file_path.suffix[1:].lower() or "no_extension"
    dest_dir = dst / ext
    if not await dest_dir.exists():
        await dest_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dest_dir}")

    dest_file = dest_dir / file_path.name
    await copyfile(file_path, dest_file)
    logger.info(f"Copied '{file_path}' → '{dest_file}'")


async def main():
    args = parsing_args()
    src = AsyncPath(Path(args.source).expanduser().resolve())
    dst = AsyncPath(Path(args.output).expanduser().resolve())

    if not await src.exists() or not await src.is_dir():
        print(f"Source directory '{src}' does not exist or is not a directory.")
        return

    if not await dst.exists():
        print(f"Destination directory '{dst}' does not exist. Creating it.")
        await dst.mkdir(parents=True)

    print(f"Source folder: {src}")
    print(f"Destination folder: {dst}")

    all_files = await read_folder(src)

    # Обробка копіювання файлів паралельно
    await asyncio.gather(*(copy_file(file_path, dst) for file_path in all_files))


if __name__ == "__main__":
    asyncio.run(main())
