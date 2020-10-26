import React, { useEffect } from 'react'
import {
	Button,
	Grid,
	TableBody,
} from '@material-ui/core'
import { useHistory } from 'react-router-dom'
import { ArkivUttrekk } from '../types/sharedTypes'
import { makeStyles } from '@material-ui/core/styles'
import { useSharedStyles } from '../styles/sharedStyles'
import useGetOnMount from '../hooks/useGetOnMount'
import ArkivuttrekkRow from './ArkivuttrekkRow'
import useRequest from '../hooks/useRequest'
import useTable from '../hooks/useTable'

const useStyles = makeStyles(theme => ({
	gridMargin: {
		marginBottom: theme.spacing(3)
	},
	title: {
		color: theme.palette.primary.main,
	},
}))

const Overview: React.FC = ():JSX.Element => {
	const columns = [
		{
			id: 'icon',
			label: '',
		},
		{
			id: 'tittel',
			label: 'Tittel',
		},
		{
			id: 'type',
			label: 'Type',
		},
		{
			id: 'avgiver_navn',
			label: 'Avgivers navn',
		},
		{
			id: 'status',
			label: 'Status',
		}
	]

	//TODO: replace with real url once we have endpoint
	//const { data, loading, error } = useGetOnMount<ArkivUttrekk[]>('/arkivuttrekk')
	const { data, loading, error, performRequest } = useRequest<ArkivUttrekk[]>()

	useEffect(() => {
		performRequest({
			url: '/arkivuttrekk',
			method: 'GET',
		})

	}, [])


	const { TblContainer, TblHead } = useTable(columns, handleTableChange)
	const classes = useStyles()
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
						color='primary'
						onClick={gotoInvite}
					>
                        Nytt arkivuttrekk
					</Button>
				</Grid>
			</Grid>
			<TblContainer>
				<TblHead />
				<TableBody>
					{data?.length && data.map((arkivUttrekk: ArkivUttrekk) => (
						<ArkivuttrekkRow key={arkivUttrekk.id} arkivUttrekk={arkivUttrekk} />
					))}
				</TableBody>
			</TblContainer>
		</>
	)
}

export default Overview
