import React from 'react'
import { makeStyles } from '@material-ui/core/styles'
import {
	Icon,
	IconButton,
} from '@material-ui/core'

const useStyles = makeStyles(theme => ({
	root: {
		flexShrink: 0,
		marginLeft: theme.spacing(2.5),
	},
}))

interface TablePaginationActionsProps {
    count: number;
    page: number;
    rowsPerPage: number;
    onChangePage: (event: React.MouseEvent<HTMLButtonElement>, newPage: number) => void;
  }

/**
 * Display Table pagination and handle paginationevents.
 */
const TablePaginationActions = (props: TablePaginationActionsProps) => {
	const classes = useStyles()
	const { count, page, rowsPerPage, onChangePage } = props

	const handleFirstPageButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
		onChangePage(event, 0)
	}

	const handleBackButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
		onChangePage(event, page - 1)
	}

	const handleNextButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
		onChangePage(event, page + 1)
	}

	const handleLastPageButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
		onChangePage(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1)) //TODO: will not work before we get total count from backend instead of default -1
	}

	return (
		<div className={classes.root}>
			<IconButton
				onClick={handleFirstPageButtonClick}
				disabled={page === 0}
				aria-label='første side'
			>
				<Icon>first_page</Icon>
			</IconButton>
			<IconButton
				onClick={handleBackButtonClick}
				disabled={page === 0}
				aria-label='forrige side'
			>
				<Icon>keyboard_arrow_left</Icon>
			</IconButton>
			<IconButton
				onClick={handleNextButtonClick}
				//disabled= TODO: fill in once we get total count from backend
				aria-label='neste side'
			>
				<Icon>keyboard_arrow_right</Icon>
			</IconButton>
			<IconButton
				onClick={handleLastPageButtonClick}
				//disabled= TODO: fill in once we get total count from backend
				aria-label='siste side'
			>
				<Icon>last_page</Icon>
			</IconButton>
		</div>
	)
}

export default TablePaginationActions
