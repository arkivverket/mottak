import type { MouseEvent } from 'react'
import { useEffect, useState } from 'react'

import { makeStyles } from '@material-ui/core/styles'
import { Icon, IconButton } from '@material-ui/core'

const useStyles = makeStyles((theme) => ({
	root: {
		flexShrink: 0,
		marginLeft: theme.spacing(2.5),
	},
}))

interface TablePaginationActionsProps {
	count: number
	page: number
	rowsPerPage: number
	onChangePage: (event: MouseEvent<HTMLButtonElement>, newPage: number) => void
}

type ButtonClick = MouseEvent<HTMLButtonElement>

/**
 * Display Table pagination and handle paginationevents.
 */
const TablePaginationActions = (props: TablePaginationActionsProps) => {
	const classes = useStyles()
	const { count, page, rowsPerPage, onChangePage } = props
	const [disableNext, setDisableNext] = useState<boolean>(false)

	const handleFirstPageButtonClick = (event: ButtonClick) => {
		onChangePage(event, 0)
	}

	const handleBackButtonClick = (event: ButtonClick) => {
		onChangePage(event, page - 1)
	}

	const handleNextButtonClick = (event: ButtonClick) => {
		onChangePage(event, page + 1)
	}

	const handleLastPageButtonClick = (event: ButtonClick) => {
		onChangePage(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1))
	}

	useEffect(() => {
		setDisableNext((page + 1) * rowsPerPage >= count)
	}, [page, setDisableNext, count, rowsPerPage])

	return (
		<div className={classes.root}>
			<IconButton onClick={handleFirstPageButtonClick} disabled={page === 0} aria-label="første side">
				<Icon>first_page</Icon>
			</IconButton>
			<IconButton onClick={handleBackButtonClick} disabled={page === 0} aria-label="forrige side">
				<Icon>keyboard_arrow_left</Icon>
			</IconButton>
			<IconButton onClick={handleNextButtonClick} disabled={disableNext} aria-label="neste side">
				<Icon>keyboard_arrow_right</Icon>
			</IconButton>
			<IconButton onClick={handleLastPageButtonClick} disabled={disableNext} aria-label="siste side">
				<Icon>last_page</Icon>
			</IconButton>
		</div>
	)
}

export default TablePaginationActions
