import React from 'react'
import { Button, Grid } from '@material-ui/core'
import { useHistory } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'

import ArkivuttrekkTable from './arkivuttrekk-table/ArkivuttrekkTable'

const useStyles = makeStyles((theme) => ({
	gridMargin: {
		marginBottom: theme.spacing(3),
	},
	title: {
		color: theme.palette.primary.main,
	},
}))

/**
 * Display arkivuttrekk as table data, and initializing adding new arkivuttrekk workflow.
 */
const Overview: React.FC = (): JSX.Element => {
	const classes = useStyles()
	const history = useHistory()

	function gotoInvite() {
		history.push('/arkivuttrekk/invitation')
	}

	return (
		<>
			<Grid container alignItems="center" justify="space-between" className={classes.gridMargin}>
				<Grid item xs={12} sm={6}>
					<h2>Arkivuttrekk</h2>
				</Grid>
				<Grid item container xs={12} sm={6} justify="flex-end">
					<Button variant={'outlined'} color="primary" onClick={gotoInvite}>
						Nytt arkivuttrekk
					</Button>
				</Grid>
			</Grid>
			<ArkivuttrekkTable />
		</>
	)
}

export default Overview
