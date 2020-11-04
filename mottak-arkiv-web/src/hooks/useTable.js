import React, { useState } from 'react'
import {
	Table,
	TableCell,
	TableFooter,
	TableHead,
	TablePagination,
	TableRow,
} from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'

const useStyles = makeStyles(theme => ({
	title: {
		color: theme.palette.primary.main,
	},
}))

const useTable = ( columns, handleTableChange, pagination ) => {
	const [page, setPage] = useState(0)
	const [rows, setRows] = useState(10)

	const handleChangePage = (e, newPage) => {
		setPage(newPage)
		handleTableChange((newPage * rows), rows)
	}

	const handleChangeRows = e => {
		const tmpRows = parseInt(e.target.value, 10)
		setRows(tmpRows)
		setPage(0)
		handleTableChange(0, tmpRows)
	}

	const TblContainer = ({ children }) => (
		<Table>
			{children}
			{ pagination &&
			<TableFooter>
				<TableRow>
					<TablePagination
						count={-1}
						page={page}
						rowsPerPage={rows}
						onChangePage={handleChangePage}
						onChangeRowsPerPage={handleChangeRows}
						labelRowsPerPage={'Velg antall per side'}
						labelDisplayedRows={({ from, to }) => (`${from}-${to} av totalt`)}
						rowsPerPageOptions={[5, 10, 20, 50]}
					/>
				</TableRow>
			</TableFooter>
			}
		</Table>
	)

	const TblHead = () => {
		const classes = useStyles()

		return (
			<TableHead>
				<TableRow>
					{
						columns.map(col => (
							<TableCell key={col.id} className={classes.title}>
								{col.label}
							</TableCell>
						))
					}
				</TableRow>
			</TableHead>
		)
	}

	return { TblContainer, TblHead }
}

export default useTable

