import { useCallback, useContext, useEffect } from 'react'
import { Divider, Grid, List, ListItem, CircularProgress, Typography, Button } from '@material-ui/core'
import { Link } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'
import { useParams } from 'react-router'

import type { ArkivUttrekk, DownloadStatusState } from 'src/types/sharedTypes'
import { ArkivkopiStatus } from 'src/types/sharedTypes'

import { AlertContext } from 'src/components/WorkArea'
import { useGetOnMount, useArkivkopi } from 'src/hooks'

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
		margin: 0,
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

	const statusInterval = 10 * 1000

	const { data, loading, error } = useGetOnMount<ArkivUttrekk>(`/arkivuttrekk/${id}`)

	// const {
	// 	status: downloadStatus,
	// 	loading: loadingArkivkopi,
	// 	disable: disableBestillingButton,
	// 	error: errorArkivkopi,
	// 	performRequest: requestArkivkopi,
	// } = useArkivkopi({
	// 	url: `/arkivuttrekk/${id}/bestill_nedlasting`,
	// 	statusInterval,
	// })

	const {
		status: overforingspakkeStatus,
		loading: loadingOverforingspakke,
		disable: disableOverforingspakkeButton,
		error: errorOverforingspakke,
		performRequest: requestOverforingspakke,
	} = useArkivkopi({
		url: `/arkivuttrekk/${id}/overforingspakke/bestill_nedlasting`,
		statusInterval,
	})

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

		// if (errorArkivkopi) {
		// 	setAlertContent({
		// 		msg: errorArkivkopi?.response?.data?.detail || 'Det skjedde en feil under bestilling av arkivkopi.',
		// 		type: 'error',
		// 	})
		// }

		if (errorOverforingspakke) {
			setAlertContent({
				msg:
					errorOverforingspakke?.response?.data?.detail ||
					'Det skjedde en feil under nedlastning av overføringspakke.',
				type: 'error',
			})
		}
	}, [error, setAlertContent, errorOverforingspakke])

	const showDownloadLocation = useCallback((type: string, download: DownloadStatusState): null | JSX.Element => {
		const { status, target_name } = download
		let text = ''

		switch (status) {
			case ArkivkopiStatus.OK:
				text = `${type} ble lastet ned til`
				break

			case ArkivkopiStatus.BESTILT:
				text = `${type} vil bli tilgjengelig her`
				break
		}

		return !text ? null : (
			<p>
				{text}:
				<br />
				{target_name}
			</p>
		)
	}, [])

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
						{/* <Grid item xs={4}>
							<Typography variant="h6" color="primary" gutterBottom style={{ marginBottom: '1rem' }}>
								Nedlastnings status:{' '}
								<span style={{ fontWeight: 400 }}>
									{loadingArkivkopi ? <CircularProgress size="1rem" /> : downloadStatus.status.toLowerCase()}
								</span>
							</Typography>

							<div className={classes.loadingButtonWrapper}>
								<Button
									variant="contained"
									color="primary"
									disabled={disableBestillingButton}
									onClick={requestArkivkopi}
								>
									Bestill nedlastning
								</Button>
								{loadingArkivkopi && <CircularProgress className={classes.buttonProgress} size={22} />}
							</div>

							{showDownloadLocation('Arkiv', downloadStatus)}
						</Grid> */}

						<Grid item xs={4}>
							<Typography variant="h6" color="primary" gutterBottom style={{ marginBottom: '1rem' }}>
								Overføringspakke:{' '}
								<span style={{ fontWeight: 400 }}>
									{loadingOverforingspakke ? (
										<CircularProgress size="1rem" />
									) : (
										overforingspakkeStatus.status.toLowerCase()
									)}
								</span>
							</Typography>

							<div className={classes.loadingButtonWrapper}>
								<Button
									variant="contained"
									color="primary"
									disabled={disableOverforingspakkeButton}
									onClick={requestOverforingspakke}
								>
									Last ned overføringspakke
								</Button>
								{loadingOverforingspakke && <CircularProgress className={classes.buttonProgress} size={22} />}
							</div>

							{showDownloadLocation('Overføringspakke', overforingspakkeStatus)}
						</Grid>
					</Grid>
				</>
			)}
		</>
	)
}

export default Details
