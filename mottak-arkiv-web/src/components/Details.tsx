import { useCallback, useContext, useEffect, useLayoutEffect, useState } from 'react'
import { Divider, Grid, List, ListItem, CircularProgress, Typography, Button } from '@material-ui/core'
import { Link } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'
import { useParams } from 'react-router'

import { AlertContext } from './WorkArea'
import { ArkivUttrekk, ArkivkopiStatus, ArkivkopiStatusRequest } from '../types/sharedTypes'
import { useGetOnMount, useRequest } from 'src/hooks'
import { validateArkivopiStatus } from 'src/utils'

type DownloadStatusState = ArkivkopiStatus | 'Ukjent status' | 'Ikke bestilt'

const useStyles = makeStyles((theme) => ({
	list: {
		marginBottom: '1rem',
	},
	dividerSpace: {
		marginBottom: '1rem',
	},
	label: {
		color: theme.palette.primary.main,
		fontWeight: 'bold',
	},
	loadingButtonWrapper: {
		margin: theme.spacing(1),
		position: 'relative',
		display: 'inline-block',
	},
	buttonProgress: {
		position: 'absolute',
		top: '50%',
		left: '50%',
		marginTop: -11,
		marginLeft: -11,
	},
}))

const Details: React.FC = (): JSX.Element => {
	const classes = useStyles()
	const { setAlertContent } = useContext(AlertContext)
	const { id } = useParams<{ id: string }>()

	const [downloadStatus, setDownloadStatus] = useState<DownloadStatusState>('Ikke bestilt')
	const [disableBestillingButton, setDisableBestillingButton] = useState<boolean>(false)

	const { data, loading, error } = useGetOnMount<ArkivUttrekk>(`/arkivuttrekk/${id}`)

	const {
		data: arkivkopiStatusResponse,
		loading: loadingArkivkopiStatus,
		performRequest: getArkivkopiStatus,
	} = useRequest<ArkivkopiStatusRequest>()

	const {
		data: arkivkopiRequestReponse,
		loading: loadingArkivkopiRequest,
		error: errorArkivkopiRequest,
		performRequest: requestArkivkopi,
	} = useRequest<true>()

	// Disabled the "Bestill nedlastning" button, and send a request to the backend
	const bestillNedlastning = useCallback(async () => {
		// If someone re-enables the button manually, return early
		if (disableBestillingButton) return

		setDisableBestillingButton(true)
		await requestArkivkopi({
			url: `/arkivuttrekk/${id}/bestill_nedlasting`,
			method: 'POST',
		})
	}, [disableBestillingButton, id, requestArkivkopi])

	/**
	 * Collective error handling
	 */
	useEffect(() => {
		if (!setAlertContent) return

		if (error) {
			setAlertContent({
				msg: error?.response?.data?.detail || 'Det skjedde en feil under henting av arkivuttrekk.',
				type: 'error',
			})
		}

		if (errorArkivkopiRequest) {
			setAlertContent({
				msg: errorArkivkopiRequest?.response?.data?.detail || 'Det skjedde en feil under bestilling av arkivkopi.',
				type: 'error',
			})

			// Reset order button
			setDisableBestillingButton(false)
		}
	}, [error, errorArkivkopiRequest, setAlertContent])

	useLayoutEffect(() => {
		getArkivkopiStatus({
			url: `/arkivuttrekk/${id}/bestill_nedlasting/status`,
		})

		// @TODO: Figure out why useRequest causes infinte requests
	}, [])

	useLayoutEffect(() => {
		if (!arkivkopiStatusResponse) return
		const { status } = arkivkopiStatusResponse

		// Validate the incoming status. We'll set it to "Ukjent status" if the status is not yet implemented in ArkivkopiStatus
		setDownloadStatus(validateArkivopiStatus(status) ? status : 'Ukjent status')

		switch (status) {
			case ArkivkopiStatus.FEILET:
				setDisableBestillingButton(false)
				break

			default:
				setDisableBestillingButton(true)
				break
		}
	}, [arkivkopiStatusResponse])

	/**
	 * This is triggered after pressing the Bestill Nedlastning button.
	 * arkivkopiRequestReponse is true if the request went through nicely, otherwise it is null
	 */
	useLayoutEffect(() => {
		if (!arkivkopiRequestReponse) return
		setDownloadStatus(ArkivkopiStatus.BESTILT)
	}, [arkivkopiRequestReponse])

	return (
		<>
			{loading ? (
				<CircularProgress />
			) : (
				<>
					<Grid container alignItems="center" justify="space-between">
						<Typography variant="h6" color="primary" gutterBottom>
							{data?.tittel || 'Ingen tittel'}
						</Typography>
						<Link style={{ color: '#034c6b' }} to={'/'}>
							Til oversikten
						</Link>
					</Grid>

					<Divider />

					<List component="div" className={classes.list}>
						<ListItem>
							<Grid className={classes.label} item xs={12} sm={3}>
								<div>Koordinators epost:</div>
							</Grid>
							<Grid item xs={12} sm={6}>
								<div>{data?.koordinator_epost}</div>
							</Grid>
						</ListItem>
						<Divider light={true} variant="middle" />
						<ListItem>
							<Grid className={classes.label} item xs={12} sm={3}>
								<div>Objektid:</div>
							</Grid>
							<Grid item xs={12} sm={6}>
								<div>{data?.obj_id}</div>
							</Grid>
						</ListItem>
						<Divider light={true} variant="middle" />
						<ListItem>
							<Grid className={classes.label} item xs={12} sm={3}>
								<div>Arkivtype:</div>
							</Grid>
							<Grid item xs={12} sm={6}>
								<div>{data?.type}</div>
							</Grid>
						</ListItem>
						<Divider light={true} variant="middle" />
						<ListItem>
							<Grid className={classes.label} item xs={12} sm={3}>
								<div>Størrelse:</div>
							</Grid>
							<Grid item xs={12} sm={6}>
								<div>{data?.storrelse}</div>
							</Grid>
						</ListItem>
						<Divider light={true} variant="middle" />
						<ListItem>
							<Grid className={classes.label} item xs={12} sm={3}>
								<div>Tidsspenn:</div>
							</Grid>
							<Grid item xs={12} sm={6}>
								<div>{`${data?.arkiv_startdato} - ${data?.arkiv_sluttdato}`}</div>
							</Grid>
						</ListItem>
						<Divider light={true} variant="middle" />
						<ListItem>
							<Divider />
							<Grid className={classes.label} item xs={12} sm={3}>
								<div>Avtalenummer:</div>
							</Grid>
							<Grid item xs={12} sm={6}>
								<div>{data?.avtalenummer}</div>
							</Grid>
						</ListItem>
						<Divider light={true} variant="middle" />
					</List>

					<Grid container>
						<Grid item xs={4}>
							<Typography variant="h6" color="primary" gutterBottom style={{ marginBottom: '1rem' }}>
								Nedlastnings status:{' '}
								<span style={{ fontWeight: 400 }}>
									{loadingArkivkopiStatus ? <CircularProgress size="1rem" /> : downloadStatus.toLowerCase()}
								</span>
							</Typography>

							<div className={classes.loadingButtonWrapper}>
								<Button
									variant="contained"
									color="primary"
									disabled={disableBestillingButton}
									onClick={bestillNedlastning}
								>
									Bestill nedlastning
								</Button>
								{loadingArkivkopiRequest && <CircularProgress className={classes.buttonProgress} size={22} />}
							</div>
						</Grid>
					</Grid>
				</>
			)}
		</>
	)
}

export default Details
