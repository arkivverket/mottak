import React from 'react'
import {
	Divider,
	Grid,
	List,
	ListItem,
	Typography } from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'
import { useParams } from 'react-router'
import { ArkivUttrekk } from '../types/sharedTypes'
import { useSharedStyles } from '../styles/sharedStyles'

import useGetOnMount from '../hooks/useGetOnMount'

const useStyles = makeStyles(theme => ({
	label: {
		color: theme.palette.primary.main,
		fontWeight: 'bold'
	},
}))

const Details: React.FC = ():JSX.Element => {
	const sharedClasses = useSharedStyles()
	const classes = useStyles()

	const { id } = useParams<{id: string}>()

	const { data, loading, error } = useGetOnMount<ArkivUttrekk>(`/arkivuttrekk/${id}`)

	return (
		<>
			<Typography variant='h6' color='primary' gutterBottom>
				{data?.tittel || 'Ingen tittel'}
			</Typography>
			<Divider />
			<List component='div'>
				<ListItem>
            		<Grid className={classes.label} item xs={12} sm={3}>
						<div>Koordinators epost:</div>
					</Grid>
					<Grid item xs={12} sm={6}>
						<div>{data?.koordinator_epost}</div>
					</Grid>
				</ListItem>
				<Divider light={true} variant='middle' />
				<ListItem>
					<Grid className={classes.label} item xs={12} sm={3}>
						<div>Objektid:</div>
					</Grid>
					<Grid item xs={12} sm={6}>
						<div>{data?.obj_id}</div>
					</Grid>
				</ListItem>
				<Divider light={true} variant='middle' />
				<ListItem>
					<Grid className={classes.label} item xs={12} sm={3}>
						<div>Arkivtype:</div>
					</Grid>
					<Grid item xs={12} sm={6}>
						<div>{data?.type}</div>
					</Grid>
				</ListItem>
				<Divider light={true} variant='middle' />
				<ListItem>
					<Grid className={classes.label} item xs={12} sm={3}>
						<div>Størrelse:</div>
					</Grid>
					<Grid item xs={12} sm={6}>
						<div>{data?.storrelse}</div>
					</Grid>
				</ListItem>
				<Divider light={true} variant='middle' />
				<ListItem>
					<Grid className={classes.label} item xs={12} sm={3}>
						<div>Tidsspenn:</div>
					</Grid>
					<Grid item xs={12} sm={6}>
						<div>{`${data?.arkiv_startdato} - ${data?.arkiv_sluttdato}`}</div>
					</Grid>
				</ListItem>
				<Divider light={true} variant='middle' />
				<ListItem>
					<Divider />
					<Grid className={classes.label} item xs={12} sm={3}>
						<div>Avtalenummer:</div>
					</Grid>
					<Grid item xs={12} sm={6}>
						<div>{data?.avgiver_epost}</div>
					</Grid>
				</ListItem>
				<Divider light={true} variant='middle' />
			</List>
		</>
	)
}

export default Details
