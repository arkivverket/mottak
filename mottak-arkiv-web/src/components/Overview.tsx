import React from 'react'
import {
	Button,
	Grid,
	TableBody,
	TableCell,
	TableRow,
} from '@material-ui/core'
import { useHistory } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'
import { useSharedStyles } from '../styles/sharedStyles'
import useGetOnMount from '../hooks/useGetOnMount'
import useTable from '../hooks/useTable'

type Props = {
	title: string
}

//TODO: replace with real type once we have endpoint
type Arkivuttrekk = {
    tag_no: string,
    id: number,
}

const useStyles = makeStyles(theme => ({
	gridMargin: {
		marginBottom: theme.spacing(3)
	},
	hoverRow: {
		'&:hover': {
			backgroundColor: theme.palette.primary
		}
	}
}))

const Overview: React.FC<Props> = ():JSX.Element => {
	const columns = [
		{
			id: 'tittel',
			label: 'Tittel',
		},
		{
			id: 'type',
			label: 'Type',
		},
		{
			id: 'beskrivelse',
			label: 'Beskrivelse',
		},
	]

	//TODO: replace with real url once we have endpoint
	const { data, loading, error } = useGetOnMount<Arkivuttrekk[]>('/tags')
	const { TblContainer, TblHead } = useTable(columns)
	const classes = useStyles()
	const sharedClasses = useSharedStyles()
	const history = useHistory()

	function gotoInvite() {
		history.push('/upload')
	}

	return (
		<>
			<Grid container xs={12} alignItems='center' className={classes.gridMargin}>
				<Grid item xs={12} sm={6}>
					<h2>Arkivuttrekk</h2>
				</Grid>
				<Grid container item xs={12} sm={6} justify='flex-end'>
					<Button
						variant={'outlined'}
						onClick={gotoInvite}
						className={sharedClasses.buttonDA}
					>
                        Last opp ny
					</Button>
				</Grid>
			</Grid>
			<TblContainer>
				<TblHead />
				<TableBody>
					{data?.length && data.map((arkivUttrekk: Arkivuttrekk) => (
						<TableRow key={arkivUttrekk.tag_no} className={classes.hoverRow}>
							<TableCell component='th' scope='row'>
								{arkivUttrekk.tag_no}
							</TableCell>
							<TableCell>
								{arkivUttrekk.id}
							</TableCell>
							<TableCell>
								{arkivUttrekk.tag_no}
							</TableCell>
						</TableRow>
					))}
				</TableBody>
			</TblContainer>
		</>
	)
}

export default Overview
