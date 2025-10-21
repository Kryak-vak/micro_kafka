import asyncio
from asyncio import AbstractEventLoop

MAIN_LOOP: AbstractEventLoop | None = None


def set_main_loop() -> None:
    global MAIN_LOOP
    MAIN_LOOP = asyncio.get_running_loop()


def get_main_loop() -> AbstractEventLoop:
    if MAIN_LOOP is None:
        raise RuntimeError("No running event loop!")
    
    return MAIN_LOOP
