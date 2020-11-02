import React, { useContext, useEffect, useState } from 'react'
import {
	Button,
	Grid,
	MenuItem,
	TextField,
	CircularProgress,
	Typography
} from '@material-ui/core'
import { KeyboardDatePicker, MuiPickersUtilsProvider } from '@material-ui/pickers'
import MomentUtils from '@date-io/moment'

import { ParsedMetadataFil } from '../types/sharedTypes'
import { useSharedStyles } from '../styles/sharedStyles'
import { WorkflowContext } from './workflow/InvitationWorkflowContainer'
import { StepperContext } from './workflow/WorkflowStepper'
import { AlertContext } from './WorkArea'
import useGetOnMount from '../hooks/useGetOnMount'
import useRequest from '../hooks/useRequest'
import { number } from 'yargs'

/**
 * Step component for displaying parsed metadata file for user edit and approval.
 */
const QualityCheck: React.FC = ():JSX.Element => {
	const { handleNext, handleCancel } = useContext(StepperContext)
	const { metadataId } = useContext(WorkflowContext)
	const { setAlertContent } = useContext(AlertContext)
	const sharedClasses = useSharedStyles()

	const { data, loading, error } = useGetOnMount<ParsedMetadataFil>(`/metadatafil/${metadataId}/parsed`)

	const { data: dataAU, loading: loadingAU, error: errorAU, performRequest } = useRequest<ParsedMetadataFil>()

	const initalvalues = {
		tittel: '',
		obj_id: '',
		status: '',
		type: '',
		sjekksum_sha256: '',
		avgiver_navn: '',
		avgiver_epost: '',
		koordinator_epost: '',
		metadatafil_id: number,
		arkiv_startdato: null,
		arkiv_sluttdato: null,
		storrelse: '',
		avtalenummer: '',
	}

	const validation = {
		tittel: {
			hasError: false,
			errorMsg: 'Tittel er påkrevd.',
			validator: (tittel: string) => tittel !== null && tittel != ''
		},
	}

	const archiveTypes = ['Noark3', 'Noark5', 'Fagsystem']
	const statusTypes = ['Under oppretting', 'Invitert', 'Under behandling', 'Avvist', 'Sendt til bevaring']

	const [values, setValues] = useState<ParsedMetadataFil>(initalvalues)

	const handleSubmit = ( event: React.FormEvent) => {
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

	const handleDateChange = (event: any | null) => {
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
		<MuiPickersUtilsProvider utils={MomentUtils}>
			<form style={{ margin: '2rem' }} onSubmit={handleSubmit}>
				<Typography variant='h6' style={{ marginBottom: '1.5rem' }}>
					Registrerte verdier
				</Typography>
				{loading ?
					<CircularProgress /> :
					<Grid container spacing={4}>
						<Grid item xs={12}>
							<TextField
								id='tittel'
								name='tittel'
								label='Tittel'
								value={values.tittel}
								onChange={handleValueChange}
								fullWidth
								helperText={error ? 'Tittel må være fylt ut.' : ''}
								error={values.tittel === null || values.tittel === ''}
							/>
						</Grid>
						<Grid item xs={12} sm={6}>
							<TextField
								id='obj_id'
								name='obj_id'
								label='Objektid'
								value={values.obj_id}
								onChange={handleValueChange}
								fullWidth
							/>
						</Grid>
						<Grid item xs={12} sm={6}>
							<TextField
								select
								id='status'
								name='status'
								label='Status'
								value={values.status}
								onChange={handleValueChange}
								fullWidth
							>
						 		{statusTypes.map(option => (
									<MenuItem key={option} value={option}>
										{option}
									</MenuItem>
								))}
		 		 			</TextField>
						</Grid>
						<Grid item xs={12} sm={6}>
							<TextField
								select
								id='type'
								name='type'
								label='Arkivtype'
								value={values.type}
								onChange={handleValueChange}
								fullWidth
							>
						 		{archiveTypes.map(option => (
									<MenuItem key={option} value={option}>
										{option}
									</MenuItem>
								))}
		 		 			</TextField>
						</Grid>
						<Grid item xs={12} sm={6}>
							<TextField
								id='sjekksum_sha256'
								name='sjekksum_sha256'
								label='Sjekksum'
								value={values.sjekksum_sha256}
								onChange={handleValueChange}
								fullWidth
							/>
						</Grid>
						<Grid item xs={12} sm={6}>
							<TextField
								id='avgiver_navn'
								name='avgiver_navn'
								label='Avgivers navn'
								value={values.avgiver_navn}
								onChange={handleValueChange}
								fullWidth
							/>
						</Grid>
						<Grid item xs={12} sm={6}>
							<TextField
								required
								type='email'
								id='avgiver_epost'
								name='avgiver_epost'
								label='Avgivers epost'
								value={values.avgiver_epost}
								onChange={handleValueChange}
								fullWidth
							/>
						</Grid>
						<Grid item xs={12} sm={6}>
							<TextField
								required
								type='email'
								id='koordinator_epost'
								name='koordinator_epost'
								label={'Koordinators epost'}
								value={values.koordinator_epost}
								onChange={handleValueChange}
								fullWidth
							/>
						</Grid>
						<Grid item xs={12} sm={6}>
							<KeyboardDatePicker
								disableToolbar
								variant='inline'
								autoOk
								emptyLabel={''}
								format='YYYY-MM-DD'
								id='arkiv_startdato'
								label='Arkiv startdato'
								minDate={'1600-01-01'}
								value={values.arkiv_startdato}
								onChange={(date, value) => {
									handleDateChange({ 'target': { 'name': 'arkiv_startdato', 'value': value } })
								}}
								KeyboardButtonProps={{
									'aria-label': 'bytt dato',
								}}
								fullWidth
							/>
						</Grid>
						<Grid item xs={12} sm={6}>
							<KeyboardDatePicker
								disableToolbar
								variant='inline'
								autoOk
								emptyLabel={''}
								format='YYYY-MM-DD'
								id='arkiv_sluttdato'
								label='Arkiv sluttdato'
								minDate={'1600-01-01'}
								value={values.arkiv_sluttdato}
								onChange={(date, value) => {
									handleDateChange({ 'target': { name: 'arkiv_sluttdato', value } })
								}}
								KeyboardButtonProps={{
									'aria-label': 'bytt dato',
								}}
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
								id='avtalenummer'
								name='avtalenummer'
								label='Avtalenummer'
								value={values.avtalenummer}
								onChange={handleValueChange}
								fullWidth
							/>
						</Grid>
					</Grid>
				}
				<Grid
					container
					item
					alignItems='center'
					justify='center'
					spacing={2}
					style={{ margin: '2rem auto' }}
					xs={12}
					sm={6}
				>
					<Grid item xs={12} sm={6}>
						<Button
							variant='outlined'
							type='button'
							color='primary'
							className={sharedClasses.fullWidth}
							onClick={handleCancel}
						>
							Avbryt
						</Button>
					</Grid>
					<Grid item xs={12} sm={6}>
						<Button
							variant='outlined'
							type='submit'
							className={sharedClasses.fullWidth}
							disabled={loadingAU}
						>
							 {loadingAU ? <CircularProgress size={14} /> : 'Godkjenn data'}
						</Button>
					</Grid>
				</Grid>
			</form>
		</MuiPickersUtilsProvider>
	)
}

export default QualityCheck
