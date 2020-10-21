type MetadataType = 'Noark3'| 'Noark5' | 'Fagsystem'

export type MetadataFil = ({
    id: number,
    filnavn: string,
    type: MetadataType,
    innhold: string,
    opprettet: Date,
})

export type ArkivUttrekk = ({
    obj_id: string,
    status: 'Under oppretting' | 'Invitert' | 'Under behandling' | 'Avvist' | 'Sendt til bevaring', //TODO: maybe not part of api
    type: MetadataType,
    tittel: string,
    sjekksum_sha256: string,
    avgiver_navn: string,
    avgiver_epost: string,
    koordinator_epost: string,
    metadatafil_id: number,
    arkiv_startdato: string,
    arkiv_sluttdato: string,
    storrelse: number,
    avtalenummer: string,
    id: number,
    opprettet: Date,
    endret: Date,
})

export type ParsedMetadataFil = ({
    tittel: string,
    endret: string,
    kontaktperson: string,
    arkivtype: string,
    objekt_id: string,
    storrelse: string,
    tidsspenn: string,
    avtalenummer: string,
})

export type AlertContent = ({
    msg?: string,
    type?: 'success' | 'error' | 'warning' | 'info' | '',
})

