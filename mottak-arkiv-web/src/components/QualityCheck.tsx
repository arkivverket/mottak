import React, { useContext, useEffect, useState } from 'react'
import { Button, Grid, TextField, Typography } from '@material-ui/core'
import { ParsedMetadataFil } from '../types/sharedTypes'
import { useSharedStyles } from '../styles/sharedStyles'
import { WorkflowContext } from './workflow/InvitationWorkflowContainer'
import { StepperContext } from './workflow/WorkflowStepper'
import { AlertContext } from './WorkArea'
import useGetOnMount from '../hooks/useGetOnMount'
import useRequest from '../hooks/useRequest'

const QualityCheck: React.FC = ():JSX.Element => {
	const { handleNext, handleCancel } = useContext(StepperContext)
	const { metadataId } = useContext(WorkflowContext)
	const { setAlertContent } = useContext(AlertContext)
	const sharedClasses = useSharedStyles()

	const { data, loading, error } = useGetOnMount<ParsedMetadataFil>(`/metadatafil/${metadataId}/parsed`)

	const { data: dataAU, loading: loadingAU, error: errorAU, performRequest } = useRequest<ParsedMetadataFil>()

	const initalvalues = {
		tittel: '',
		endret: '',
		kontaktperson: '',
		arkivtype: '',
		objekt_id: '',
		storrelse: '',
		tidsspenn: '',
		avtalenummer: '',
	}

	const [values, setValues] = useState<ParsedMetadataFil>(initalvalues)

	const handleSubmit = ( event: React.FormEvent) => {
		console.warn('postvalues');

		if (event) {
			event.preventDefault()
		}
		performRequest({
			url: '/arkivuttrekk',
			method: 'POST',
			data: values,
		})
	}

	const handleValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		event.persist()
		setValues(values => ({ ...values, [event.target.name]: event.target.value }))
	}

	useEffect(() => {
		data && setValues(data)
	}, [data])

	useEffect(() => {
		setAlertContent && error && setAlertContent({ msg: 'Det skjedde en feil under henting av metadata.', type: 'error' })
	}, [error])

	useEffect(() => {
		setAlertContent && dataAU && setAlertContent({ msg: 'Arkivuttrekk er opprettet.', type: 'info' })
	}, [dataAU])

	useEffect(() => {
		setAlertContent && errorAU && setAlertContent({ msg: 'Det skjedde en feil under oppretting av arkivuttrekk.', type: 'error' })
	}, [errorAU])

	return (
		<form style={{ margin: '0 2rem 2rem 2rem' }} onSubmit={handleSubmit}>
			<Typography variant='h6' gutterBottom>
				Registrerte verdier
			</Typography>
			<Grid container spacing={4}>
				<Grid item xs={12}>
					<TextField
						required
						id='tittel'
						name='tittel'
						label='Tittel'
						value={values.tittel}
						onChange={handleValueChange}
						fullWidth
					/>
				</Grid>
				<Grid item xs={12} sm={6}>
					<TextField
						id='endret'
						name='endret'
						label='Endret'
						value={values.endret}
						onChange={handleValueChange}
						fullWidth
					/>
				</Grid>
				<Grid item xs={12} sm={6}>
					<TextField
						required
						id='kontaktperson'
						name='kontaktperson'
						label='Kontaktperson'
						value={values.kontaktperson}
						onChange={handleValueChange}
						fullWidth
					/>
				</Grid>
				<Grid item xs={12} sm={6}>
					<TextField
						id='arkivtype'
						name='arkivtype'
						label='Arkivtype'
						value={values.arkivtype}
						onChange={handleValueChange}
						fullWidth
					/>
				</Grid>
				<Grid item xs={12} sm={6}>
					<TextField
						id='objekt_id'
						name='objekt_id'
						label='Objektid'
						value={values.objekt_id}
						onChange={handleValueChange}
						fullWidth
					/>
				</Grid>
				<Grid item xs={12} sm={6}>
					<TextField
						id='storrelse'
						name='storrelse'
						label='Størrelse'
						value={values.storrelse}
						onChange={handleValueChange}
						fullWidth
					/>
				</Grid>
				<Grid item xs={12} sm={6}>
					<TextField
						id='tidsspenn'
						name='tidsspenn'
						label='Tidsspenn'
						value={values.tidsspenn}
						onChange={handleValueChange}
						fullWidth
					/>
				</Grid>
				<Grid item xs={12} sm={6}>
					<TextField
						id='avtalenummer'
						name='avtalenummer'
						label='Avtalenummer'
						value={values.avtalenummer}
						onChange={handleValueChange}
						fullWidth
					/>
				</Grid>
				<Grid
					container
					item
					alignItems='center'
					justify='center'
					spacing={2}
				>
					<Grid item>
						<Button
							variant='outlined'
							type='button'
							className={sharedClasses.buttonDA}
							onClick={handleCancel}
						>
							Avbryt
						</Button>
					</Grid>
					<Grid item>
						<Button
							variant='outlined'
							type='submit'
							className={sharedClasses.buttonDA}
						>
							Godkjenn data
						</Button>
					</Grid>
				</Grid>
			</Grid>
		</form>
	)
}

export default QualityCheck
