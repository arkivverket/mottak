import React, { useContext, useEffect, useState } from 'react'
import {
	CircularProgress,
	Table,
	TableBody,
	TableCell,
	TableFooter,
	TableHead,
	TablePagination,
	TableRow,
} from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'

import ArkivuttrekkRow from './ArkivuttrekkRow'
import TablePaginationActions from './TableActions'
import useRequest from '../../hooks/useRequest'
import { ArkivUttrekk } from '../../types/sharedTypes'
import { AlertContext } from '../WorkArea'

const useStyles = makeStyles((theme) => ({
	title: {
		color: theme.palette.primary.main,
	},
}))

/**
 * Get and display arkivuttrekk as table data.
 */
const ArkivuttrekkTable: React.FC<{ pagination?: boolean }> = ({ pagination = true }): JSX.Element => {
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
			id: 'avgiver_navn',
			label: 'Avgivers navn',
		},
		{
			id: 'status',
			label: 'Status',
		},
		{
			id: 'icon',
			label: '',
		},
	]

	const { data, loading, error, performRequest } = useRequest<{ result: ArkivUttrekk[]; count: number }>()
	const { setAlertContent } = useContext(AlertContext)
	const [page, setPage] = useState<number>(0)
	const [rows, setRows] = useState<number>(10)
	const [results, setResults] = useState<ArkivUttrekk[]>([])
	const [totalArkivuttrek, setTotalArkivuttrekk] = useState<number>(0)

	const classes = useStyles()

	//@ts-ignore
	const handleChangePage = (e, newPage) => {
		setPage(newPage)
		handleTableChange(newPage * rows, rows)
	}

	//@ts-ignore
	const handleChangeRows = (e) => {
		const tmpRows = parseInt(e.target.value, 10)
		setRows(tmpRows)
		setPage(0)
		handleTableChange(0, tmpRows)
	}

	useEffect(() => {
		error &&
			setAlertContent &&
			setAlertContent({
				msg: error?.response?.data?.detail || 'Det skjedde en feil under lasting av arkivuttrekk.',
				type: 'error',
			})
	}, [error, setAlertContent])

	useEffect(() => {
		performRequest({
			// TODO: limit=1000 is a hack until backend supports get all
			url: `/arkivuttrekk${pagination ? '' : '?limit=1000'}`,
			method: 'GET',
		})

		// @TODO: Figure out why useRequest causes infinte requests
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [])

	const handleTableChange = (skip: number, limit: number) => {
		performRequest({
			url: `/arkivuttrekk?skip=${skip}&limit=${limit}`,
			method: 'GET',
		})
	}

	useEffect(() => {
		if (!data) return

		const { result, count } = data

		setResults(result)
		setTotalArkivuttrekk(count)
	}, [data])

	return loading ? (
		<CircularProgress />
	) : (
		<Table>
			<TableHead>
				<TableRow>
					{columns.map((col) => (
						<TableCell key={col.id} className={classes.title}>
							{col.label}
						</TableCell>
					))}
				</TableRow>
			</TableHead>
			<TableBody>
				{results.length ? (
					results.map((arkivUttrekk: ArkivUttrekk) => (
						<ArkivuttrekkRow key={arkivUttrekk.id} arkivUttrekk={arkivUttrekk} />
					))
				) : (
					<TableRow>
						<TableCell>Ingen arkivuttrekk</TableCell>
					</TableRow>
				)}
			</TableBody>
			{pagination && (
				<TableFooter>
					<TableRow>
						<TablePagination
							rowsPerPageOptions={[5, 10, 20, 50]}
							count={totalArkivuttrek}
							rowsPerPage={rows}
							labelRowsPerPage={'Velg antall per side'}
							labelDisplayedRows={({ from, to }) => `${from}-${to} av totalt`}
							page={page}
							onChangePage={handleChangePage}
							onChangeRowsPerPage={handleChangeRows}
							ActionsComponent={TablePaginationActions}
						/>
					</TableRow>
				</TableFooter>
			)}
		</Table>
	)
}

export default ArkivuttrekkTable
