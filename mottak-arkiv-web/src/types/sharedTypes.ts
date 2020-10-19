type MetadataType = 'Noark3'| 'Noark5' | 'Fagsystem'

export type MetadataFil = ({
    id: number,
    filnavn: string,
    type: MetadataType,
    innhold: string,
    opprettet: Date,
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
