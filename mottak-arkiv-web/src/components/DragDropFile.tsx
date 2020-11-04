import React, { useContext, useRef, useState } from 'react'
import clsx from 'clsx'
import { makeStyles } from '@material-ui/core/styles'
import { Grid, Icon } from '@material-ui/core'
import { AlertContext } from './WorkArea'

const useStyles = makeStyles(theme => ({
	container: {
		backgroundColor: '#c9e6ee',
		marginTop: theme.spacing(3),
		marginBottom: theme.spacing(3),
		padding: theme.spacing(2),
		minWidth: '100%',
		height: '40%',
	},
	zone: {
		backgroundColor: 'white',
		display: 'flex',
		justifyContent: 'flex-start',
		padding: theme.spacing(4),
		outline: `2px dashed ${theme.palette.secondary.dark}`,
		transition: theme.transitions.create('all', {
			easing: theme.transitions.easing.sharp,
		  }),
	},
	active: {
		backgroundColor: '#dceff4',
		outlineOffset: '-5px',
		transition: theme.transitions.create('all', {
			easing: theme.transitions.easing.easeOut,
		})
	},
}))

type Props = {
	selectedFile: any,
	setSelectedFile: React.Dispatch<React.SetStateAction<Blob | string>>,
}

const DragDropFile: React.FC<Props> = ({ selectedFile, setSelectedFile }) => {
	const classes = useStyles()
	const fileInputRef = useRef<HTMLInputElement>(null)
	const [inZone, setInZone] = useState(false)
	const { setAlertContent } = useContext(AlertContext)


	const handleDragEnter = (event: React.DragEvent<HTMLDivElement>) => {
		event.preventDefault()
		setInZone(true)
	}

	const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
		event.preventDefault()
		setInZone(true)
	}

	const handleDragLeave = (event: React.DragEvent<HTMLDivElement>) => {
		event.preventDefault()
		setInZone(false)
	}

	const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
		event.preventDefault()
		const { files } = event.dataTransfer
		if (files.length) {
			if (files.length > 1) {
				setAlertContent && setAlertContent({ msg: 'Du kan bare laste opp en fil av gangen.', type: 'warning' })
				return
			}
			if (files[0].type !== 'text/xml') {
				setAlertContent && setAlertContent({ msg: 'Du kan bare laste opp xml-filer.', type: 'warning' })
				return
			}
			setSelectedFile(files[0])
		}
	}

	const fileInputClicked = () => {
		fileInputRef.current?.click()
	}

	const handleFileChosen = (event: React.ChangeEvent<HTMLInputElement>) => {
		if (!event.target.files) return
		setSelectedFile(event.target.files[0] || '')
	}

	return (
		<div className={classes.container}>
			<div
				className={clsx(classes.zone, inZone && classes.active)}
				onDrop={handleDrop}
				onDragOver={handleDragOver}
				onDragLeave={handleDragLeave}
				onDragEnter={handleDragEnter}
				onClick={fileInputClicked}
			>
				<Grid
					container
					direction='column'
					alignItems='center'
					justify='center'
				>
					<Icon color='primary' fontSize='large'>{selectedFile ? 'description' : 'cloud_upload'}</Icon>
					{selectedFile && <p>{selectedFile?.name}</p>}
					<p style={{ padding: `${!selectedFile ? '0 2rem' : '' }` }}>{`Klikk for å velge ${selectedFile && 'en ny '}fil eller dra filen hit.`}</p>
				</Grid>
				<input
			   		ref={fileInputRef}
					style={{ display: 'none' }}
					id='button-file'
					type='file'
					onChange={handleFileChosen}
					data-testid='fileUi'
				/>
			</div>
		</div>
	)
}

export default DragDropFile
