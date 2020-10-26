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
import { ArkivUttrekk } from '../types/sharedTypes'
import { ThemeConsumer } from 'styled-components'

const useStyles = makeStyles(theme => ({
	gridMargin: {
		marginBottom: theme.spacing(3)
	},
	hoverRow: {
		'&:hover': {
			backgroundColor: theme.palette.primary
		}
	},
	label: {
		color: theme.palette.primary.main,
		marginRight: theme.spacing(1),
	},
}))

const ArkivuttrekkRow: React.FC<{ arkivUttrekk: ArkivUttrekk }> = ({ arkivUttrekk }):JSX.Element => {
	const [isOpen, setIsOpen] = useState(false)
	const classes = useStyles()

	const toggle = () => {
		setIsOpen(prevState => !prevState)
	}

	return (
		<>
			<TableRow key={arkivUttrekk.id} className={classes.hoverRow}>
				<TableCell>
					<IconButton aria-label="expand row" size="small" onClick={toggle}>
						<Icon>{isOpen ? 'keyboard_arrow_up' : 'keyboard_arrow_down'}</Icon>
					</IconButton>
				</TableCell>
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
			</TableRow>
			<TableRow>
				<TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
					<Collapse in={isOpen} timeout="auto" unmountOnExit>
						<Box style={{ marginLeft: '4rem' }}>
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
