import logging
from uuid import uuid1
from arkiv_downloader.main import ArkivuttrekkTransferInfo, TransferStatus
from arkiv_downloader.main import download_blob

logging.disable(logging.CRITICAL)


def arkivuttrekk_sample():
    return ArkivuttrekkTransferInfo(uuid1(), 'https://some.containser.sas.url/something')


def test_download_blob_missing_azcopy():
    response = download_blob(arkivuttrekk_sample(), 'random_string')
    assert TransferStatus.FAILED == response, 'FileNotFoundError should be handled gracefully'
