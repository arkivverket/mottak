import React, { useContext, useEffect } from 'react'
import { Button, Grid, CircularProgress, Typography } from '@material-ui/core'

import { Invitation } from '../types/sharedTypes'
import { useSharedStyles } from '../styles/sharedStyles'
import { WorkflowContext } from './workflow/InvitationWorkflowContainer'
import { StepperContext } from './workflow/WorkflowStepper'
import { AlertContext } from './WorkArea'
import useRequest from '../hooks/useRequest'

/**
 * Step component for providing ui to send invitation.
 */
const SendInvitation: React.FC = ():JSX.Element => {
	const { handleNext, handleCancel } = useContext(StepperContext)
	const { arkivUttrekk } = useContext(WorkflowContext)
	const { setAlertContent } = useContext(AlertContext)
	const sharedClasses = useSharedStyles()

	const { data, loading, error, performRequest } = useRequest<Invitation>()


	const handleSubmit = ( event: React.FormEvent) => {
		if (event) {
			event.preventDefault()
		}
		//TODO: update when endpoint is ready
		//if (arkivUttrekk?.id) {
		performRequest({
			//url: `/arkivuttrekk/${arkivUttrekk.id}/invitasjon`,
			url: '/arkivuttrekk/1/invitasjon',
			method: 'POST',
		})
		//}
	}

	useEffect(() => {
		setAlertContent && setAlertContent({ msg: `Invitasjon er sendt til ${arkivUttrekk?.avgiver_epost}`, type: 'info' })
	}, [data])

	useEffect(() => {
		setAlertContent && error && setAlertContent({ msg: error?.response?.data?.detail || 'Det skjedde en feil under sending av epost.', type: 'error' })
	}, [error])


	return (
		<form style={{ margin: '2rem' }} onSubmit={handleSubmit}>
			<Typography variant='subtitle1' style={{ marginBottom: '1.5rem' }}>
				{`Send opplastings-invitasjon for arkivet ${arkivUttrekk?.tittel} til ${arkivUttrekk?.avgiver_epost}.`}
			</Typography>
			<Grid
				container
				item
				alignItems='center'
				justify='center'
				spacing={2}
				style={{ margin: '2rem auto' }}
				xs={12}
				sm={10}
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
						disabled={loading}
					>
						{loading ? <CircularProgress size={14} /> : 'Send Invitasjon'}
					</Button>
				</Grid>
			</Grid>
		</form>
	)
}

export default SendInvitation
