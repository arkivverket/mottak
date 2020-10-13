import React from 'react'
import {
	Table,
	TableCell,
	TableHead,
	TablePagination,
	TableRow,
	TableSortLabel,
} from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'

const useStyles = makeStyles(theme => ({
	title: {
		color: theme.palette.primary.main,
	},
}))

const useTable = columns => {
	const TblContainer = ({ children }) => (
		<Table>
			{children}
		</Table>
	)

	const TblHead = props => {
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

