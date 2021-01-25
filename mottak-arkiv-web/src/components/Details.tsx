import React, { useContext, useEffect } from 'react'
import { Divider, Grid, List, ListItem, CircularProgress, Typography } from '@material-ui/core'
import { Link } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'
import { useParams } from 'react-router'

import { AlertContext } from './WorkArea'
import { ArkivUttrekk } from '../types/sharedTypes'
import useGetOnMount from '../hooks/useGetOnMount'

const useStyles = makeStyles((theme) => ({
	list: {
		marginBottom: '1rem',
	},
	label: {
		color: theme.palette.primary.main,
		fontWeight: 'bold',
	},
}))

const Details: React.FC = (): JSX.Element => {
	const classes = useStyles()
	const { setAlertContent } = useContext(AlertContext)

	const { id } = useParams<{ id: string }>()

	const { data, loading, error } = useGetOnMount<ArkivUttrekk>(`/arkivuttrekk/${id}`)

	useEffect(() => {
		setAlertContent &&
			error &&
			setAlertContent({
				msg: error?.response?.data?.detail || 'Det skjedde en feil under henting av arkivuttrekk.',
				type: 'error',
			})
	}, [error, setAlertContent])

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
				</>
			)}
		</>
	)
}

export default Details
