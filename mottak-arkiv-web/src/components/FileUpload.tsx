import React, { useContext, useEffect } from 'react'
import { Button, Grid } from '@material-ui/core'

import { useSharedStyles } from '../styles/sharedStyles'
import useRequest from '../hooks/useRequest'
import { WorkflowContext } from './workflow/InvitationWorkflowContainer'

export let sendFile = () => {}

const FileUpload: React.FC = (): JSX.Element => {
	const sharedClasses = useSharedStyles()
	const { metsFile, setMetsFile, setMetadataId } = useContext(WorkflowContext)

	//TODO: consider moving to container
	const {
		data,
		error,
		performRequest } = useRequest()

	sendFile = () => {
		performRequest({
			url: '/metadata',
			method: 'POST',
			headers: { 'Content-Type': 'text/xml' },
			data: metsFile
		})
	}

	const handleFileChosen = (event: React.ChangeEvent<HTMLInputElement>) => {
		console.warn('event.target.files', event.target.files && event.target.files[0])
		event.target.files && setMetsFile && setMetsFile(event.target.files[0])
	}

	useEffect(() => {
		//TODO: replace with real data once we have endpoint
		console.warn(data)
		//setMetadataId(data)
	}, [data])

	useEffect(() => {
		//TODO: replace with warning
		error && console.warn(error)
	}, [error])

	return (
		<Grid container spacing={2} direction='column' justify='center'>
			<Grid item justify='center'>
				<p>
						Skal det være noe beskrivelse av format eller prosess eller annet?
				</p>
			</Grid>
			<Grid item style={{ margin: 'auto' }}>
				<input
					accept='*.xml'
					style={{ display: 'none' }}
					id='button-file'
					type='file'
					onChange={handleFileChosen}
				/>
				<label htmlFor='button-file'>
					<Button
						variant={'outlined'}
						component='span'
						className={sharedClasses.buttonDA}
					>
                    Velg METS-fil
					</Button>
				</label>
			</Grid>
		</Grid>
	)
}

export default FileUpload
