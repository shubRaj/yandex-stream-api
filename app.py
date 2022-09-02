from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from core.yandex import Yandex
from core.models import dal
import os
from urllib.parse import urlparse, quote_plus as urlquote
from datetime import datetime
from dotenv import load_dotenv
import pathlib
load_dotenv(pathlib.Path(__file__).resolve().parent/".env")
app = FastAPI()
dal.db_init(f"{os.getenv('DIALECT')}://{os.getenv('USER')}:{urlquote(os.getenv('PASSWORD'))}@{os.getenv('HOST')}/{os.getenv('DATABASE')}")


@app.get("/")
async def home(url: str):
    yandex_ins = Yandex()
    yandex_key = urlparse(url).path.split("/")[-1]
    s = dal.yandex.select().where(dal.yandex.c.yandex_key == yandex_key).limit(1)
    with dal.engine.connect() as conn:
        rp = conn.execute(s)
        result = rp.fetchone()
        if result:
            if (datetime.now() - result.updated).total_seconds() > 4*60*60:
                yandex_download_url = yandex_ins.get_download(url)
                s_update = dal.yandex.update().values(yandex_download_url=yandex_download_url).where(
                    dal.yandex.c.yandex_key == yandex_key)
                conn.execute(s_update)
            else:
                yandex_download_url = result.yandex_download_url
        else:
            yandex_download_url = yandex_ins.get_download(url)
            s_exc = dal.yandex.insert().values({
                "yandex_key": yandex_key,
                "yandex_download_url": yandex_download_url,
            })
            conn.execute(s_exc)
    return {"url": yandex_download_url}


@app.get("/watch/")
async def watch(url: str):
    download_url = await home(url)
    download_url = download_url.get("url")
    return RedirectResponse(url=download_url)
if __name__ == '__main__':
    os.system(
        "gunicorn -w 2 -b=127.0.0.1:8010 -k uvicorn.workers.UvicornWorker app:app --threads=2 --daemon")
