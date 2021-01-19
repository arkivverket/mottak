export type Status = 'Opprettet' | 'Under behandling' | 'Avvist' | 'Sendt til bevaring'

export type ArchiveType = 'Noark3' | 'Noark5' | 'Fagsystem' | 'SIARD'

export type MetadataFil = {
	id: number
	filnavn: string
	type: 'xml/mets'
	innhold: string
	opprettet: Date
}

export type ParsedMetadataFil = {
	obj_id: string
	status: Status
	type: ArchiveType
	tittel: string
	sjekksum_sha256: string
	avgiver_navn: string
	avgiver_epost: string
	koordinator_epost: string
	metadatafil_id: any
	arkiv_startdato: string | null
	arkiv_sluttdato: string | null
	storrelse: string
	avtalenummer: string
}

export type ArkivUttrekk = ParsedMetadataFil & {
	id: number
	opprettet: Date
	endret: Date
}

export type Invitation = {
	id: number
	ekstern_id: string
	arkivuttrekk_id: number
	status: 'Sendt' | 'Feilet'
	avgiver_epost: string
	opprettet: Date
}

export type AlertContent = {
	msg?: string
	type?: 'success' | 'error' | 'warning' | 'info' | ''
}
