type MetadataType = 'Noark3'| 'Noark5' | 'Fagsystem'

export type MetadataFil = ({
    id: number,
    filnavn: string,
    type: MetadataType,
    innhold: string,
    opprettet: Date,
})

export type ParsedMetadataFil = ({
    obj_id: string,
    status: string, //'Under oppretting' | 'Invitert' | 'Under behandling' | 'Avvist' | 'Sendt til bevaring', //TODO: maybe not part of api
    type: string, //MetadataType,
    tittel: string,
    sjekksum_sha256: string,
    avgiver_navn: string,
    avgiver_epost: string,
    koordinator_epost: string,
    metadatafil_id: any,
    arkiv_startdato: string | null,
    arkiv_sluttdato: string | null,
    storrelse: string,
    avtalenummer: string,
})

export type ArkivUttrekk = ( ParsedMetadataFil & {
    id: number,
    opprettet: Date,
    endret: Date,
})

export type AlertContent = ({
    msg?: string,
    type?: 'success' | 'error' | 'warning' | 'info' | '',
})

