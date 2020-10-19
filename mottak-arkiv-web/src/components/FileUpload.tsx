import React, { useContext, useEffect } from 'react'
import { Button, Grid } from '@material-ui/core'

import { useSharedStyles } from '../styles/sharedStyles'
import { WorkflowContext } from './workflow/InvitationWorkflowContainer'

const FileUpload: React.FC = (): JSX.Element => {
	const sharedClasses = useSharedStyles()
	const { setMetsFile } = useContext(WorkflowContext)

	const handleFileChosen = (event: React.ChangeEvent<HTMLInputElement>) => {
		event.target.files && setMetsFile && setMetsFile(event.target.files[0])
	}

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
