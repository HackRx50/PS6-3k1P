import asyncio
from functions import *
from dotenv import load_dotenv  # Correct import
import os
import time

load_dotenv()


async def wait(t):
    await asyncio.sleep(t)
    print(t, 'done')


async def main():
    s = time.time()
    await asyncio.gather(
        gen_and_save_image("4 balls in water", "temp_imgs/a"),
        gen_and_save_image("3 balls in water", "temp_imgs/b"),
        # gen_and_save_audio("A boat driving on mars", "temp_imgs/b")
    )
    e = time.time()
    print(e-s)

if __name__ == "__main__":
    asyncio.run(main())
