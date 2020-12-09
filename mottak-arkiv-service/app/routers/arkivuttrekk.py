from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.connectors.mailgun.mailgun_client import MailgunClient
from app.connectors.sas_generator.sas_generator_client import SASGeneratorClient
from app.domain import arkivuttrekk_service
from app.domain.models.Invitasjon import InvitasjonStatus
from app.exceptions import ArkivuttrekkNotFound
from app.routers.dto.Arkivuttrekk import Arkivuttrekk, ArkivuttrekkBase
from app.routers.dto.Invitasjon import Invitasjon
from app.routers.dto.SASToken import SASToken
from app.routers.router_dependencies import get_db_session, get_mailgun_domain, get_mailgun_secret, get_tusd_url, get_sas_url

router = APIRouter()


@router.post("",
             status_code=status.HTTP_201_CREATED,
             response_model=Arkivuttrekk,
             summary="Lagre et arkivuttrekk ut fra redigerbare felter")
async def router_create_arkivuttrekk(arkivuttrekk: ArkivuttrekkBase, db: Session = Depends(get_db_session)):
    return arkivuttrekk_service.create(arkivuttrekk.to_domain(), db)


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=Arkivuttrekk,
            summary="Hent arkivuttrekk basert på id")
async def router_get_by_id(id: int, db: Session = Depends(get_db_session)):
    try:
        return arkivuttrekk_service.get_by_id(id, db)
    except ArkivuttrekkNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[Arkivuttrekk],
            summary="Hent alle arkivuttrekk")
async def router_get_all(db: Session = Depends(get_db_session), skip: int = 0, limit: int = 10):
    return arkivuttrekk_service.get_all(db, skip, limit)


@router.post('/{id}/invitasjon',
             status_code=status.HTTP_200_OK,
             response_model=Invitasjon,
             summary='Lager en invitasjon og sender den over epost')
async def router_send_email(id: int, db: Session = Depends(get_db_session)):
    async with MailgunClient(get_mailgun_domain(), get_mailgun_secret(), get_tusd_url()) as client:
        try:
            result = await arkivuttrekk_service.create_invitasjon(id, db, client)
        except ArkivuttrekkNotFound as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)
        if result.status == InvitasjonStatus.FEILET:
            raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,
                                detail='Utsending av invitasjon feilet, venligst prøv igjen senere')
        else:
            return result

@router.post('/{id}/bestill_nedlasting',
             status_code=status.HTTP_200_OK,
             response_model=SASToken,
             summary='Bestiller en nedlastning fra arkiv downloader')
async def request_download(id: int, db: Session = Depends(get_db_session)):
    async with SASGeneratorClient(get_sas_url()) as client:
        try:
            result = await arkivuttrekk_service.request_download(id, db, client)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)
        return result
