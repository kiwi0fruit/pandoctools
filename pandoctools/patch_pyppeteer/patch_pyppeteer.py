"""
Usage (in this particular order):

from pandotools.patch_pyppeteer import patch_pyppeteer
patch_pyppeteer()
from pyppeteer import launch
"""
from pyppeteer.chromium_downloader import *
import certifi


NO_PROGRESS_BAR = os.environ.get('PYPPETEER_NO_PROGRESS_BAR', '')
if NO_PROGRESS_BAR.lower() in ('1', 'true'):
    NO_PROGRESS_BAR = True  # type: ignore


def download_zip(url: str) -> BytesIO:
    """Download data from url."""
    logger.warning('start patched secure https chromium download.\n'
                   'Download may take a few minutes.')

    with urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()) as https:
        # Get data from url.
        # set preload_content=False means using stream later.
        data = https.request('GET', url, preload_content=False)

        try:
            total_length = int(data.headers['content-length'])
        except (KeyError, ValueError, AttributeError):
            total_length = 0

        process_bar = tqdm(
            total=total_length,
            file=os.devnull if NO_PROGRESS_BAR else None,
        )

        # 10 * 1024
        _data = BytesIO()
        for chunk in data.stream(10240):
            _data.write(chunk)
            process_bar.update(len(chunk))
        process_bar.close()

    logger.warning('\nchromium download done.')
    return _data


def patch_pyppeteer():
    import pyppeteer.chromium_downloader
    pyppeteer.chromium_downloader.download_zip = download_zip

    import pyppeteer.connection
    _connect = pyppeteer.connection.websockets.client.connect

    def connect(*args, ping_interval=None, ping_timeout=None, **kwargs):
        return _connect(*args, ping_interval=ping_interval, 
                        ping_timeout=ping_timeout, **kwargs)

    pyppeteer.connection.websockets.client.connect = connect
