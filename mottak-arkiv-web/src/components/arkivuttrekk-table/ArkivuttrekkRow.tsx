import React, { useState } from 'react'
import {
	Box,
	Collapse,
	IconButton,
	Icon,
	List,
	ListItem,
	TableCell,
	TableRow,
} from '@material-ui/core'
import { Link } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'

import { ArkivUttrekk } from '../../types/sharedTypes'

const useStyles = makeStyles(theme => ({
	root: {
		'&:hover': {
			color: theme.palette.primary.main,
			backgroundColor: theme.palette.secondary.light,
		}
	},
	gridMargin: {
		marginBottom: theme.spacing(3)
	},
	label: {
		color: theme.palette.primary.main,
		marginRight: theme.spacing(1),
	},
}))

/**
 * Display single arkivuttrekk as a toggle-row.
 */
const ArkivuttrekkRow: React.FC<{ arkivUttrekk: ArkivUttrekk }> = ({ arkivUttrekk }):JSX.Element => {
	const [isOpen, setIsOpen] = useState(false)
	const classes = useStyles()

	const toggle = () => {
		setIsOpen(prevState => !prevState)
	}

	return (
		<>
			<TableRow key={arkivUttrekk.id} className={classes.root}>
				<TableCell component='th' scope='row'>
					<Link style={{ color: '#034c6b' }} to={`/arkivuttrekk/${arkivUttrekk.id}`}>{arkivUttrekk.tittel}</Link>
				</TableCell>
				<TableCell>
					{arkivUttrekk.type}
				</TableCell>
				<TableCell>
					{arkivUttrekk.avgiver_navn}
				</TableCell>
				<TableCell>
					{arkivUttrekk.status}
				</TableCell>
				<TableCell>
					<IconButton aria-label="expand row" size="small" onClick={toggle}>
						<Icon>{isOpen ? 'keyboard_arrow_up' : 'keyboard_arrow_down'}</Icon>
					</IconButton>
				</TableCell>
			</TableRow>
			<TableRow>
				<TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
					<Collapse in={isOpen} timeout="auto" unmountOnExit>
						<Box>
							<List component='div'>
								<ListItem>
									<span className={classes.label}>Koordinators epost: </span>
									<span>{arkivUttrekk?.koordinator_epost}</span>
								</ListItem>
								<ListItem>
									<span className={classes.label}>Objektid: </span>
									<span>{arkivUttrekk?.obj_id}</span>
								</ListItem>
								<ListItem>
									<span className={classes.label}>Størrelse: </span>
									<span>{arkivUttrekk?.storrelse}</span>
								</ListItem>
								<ListItem>
									<span className={classes.label}>Tidsspenn: </span>
									<span>{`${arkivUttrekk?.arkiv_startdato} - ${arkivUttrekk?.arkiv_sluttdato}`}</span>
								</ListItem>
								<ListItem>
									<span className={classes.label}>Avtalenummer: </span>
									<span>{arkivUttrekk?.avtalenummer}</span>
								</ListItem>
							</List>
						</Box>
					</Collapse>
				</TableCell>
			</TableRow>
		</>
	)
}

export default ArkivuttrekkRow
