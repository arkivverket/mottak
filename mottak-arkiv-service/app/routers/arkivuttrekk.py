from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.arkivuttrekk_service import get_by_id, get_all, create_invitasjon
from app.domain.models.Invitasjon import InvitasjonStatus
from app.routers.dto.Arkivuttrekk import Arkivuttrekk
from app.routers.dto.Invitasjon import Invitasjon
from app.routers.router_dependencies import get_db_session,get_mailgun_domain, get_mailgun_secret, get_tusd_url
from app.connectors.mailgun.mailgun_client import MailgunClient

router = APIRouter()


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=Arkivuttrekk,
            summary="Hent arkivuttrekk basert på id")
async def router_get_by_id(id_: int, db: Session = Depends(get_db_session)):
    result = get_by_id(id_, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fant ikke Arkivuttrekk med id={id_}")
    return result


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[Arkivuttrekk],
            summary="Hent alle arkivuttrekk")
async def router_get_all(db: Session = Depends(get_db_session), skip: int = 0, limit: int = 10):
    return get_all(db, skip, limit)


@router.post('/{id_}/invitasjon',
             status_code=status.HTTP_200_OK,
             response_model=Invitasjon,
             summary='Lager en invitasjon og sender den over epost')
async def router_send_email(id_: int, db: Session = Depends(get_db_session)):
    async with MailgunClient(get_mailgun_domain(), get_mailgun_secret(), get_tusd_url()) as client:
        result = await create_invitasjon(id_, db, client)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fant ikke Arkivuttrekk med id={id_}")
        elif result.status == InvitasjonStatus.FEILET:
            raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=f'Utsending av invitasjon feilet, venligst prøv igjen senere')
        else:
            return result
