import React, { useContext, useEffect, useState } from 'react'
import { Button, Grid } from '@material-ui/core'

import DragDropFile from './DragDropFile'
import { AlertContext } from './WorkArea'
import { MetadataFil } from '../types/sharedTypes'
import { StepperContext } from './workflow/WorkflowStepper'
import { WorkflowContext } from './workflow/InvitationWorkflowContainer'
import { useSharedStyles } from '../styles/sharedStyles'
import useRequest from '../hooks/useRequest'

/**
 * Step component for uploading the metadata file.
 */
const FileUpload: React.FC = (): JSX.Element => {
	const sharedClasses = useSharedStyles()
	const { setAlertContent } = useContext(AlertContext)
	const { handleNext, handleCancel } = useContext(StepperContext)
	const { setMetadataId } = useContext(WorkflowContext)
	const [metsFile, setMetsFile] = useState<Blob | string>('')

	const {
		data,
		error,
		performRequest }: {data: MetadataFil | null, error: boolean, performRequest: any} = useRequest()

	const sendFile = () => {
		const formData = new FormData()
		formData.append('file', metsFile)

		performRequest({
			url: '/metadatafil',
			method: 'POST',
			headers: { 'Content-Type': 'multipart/form-data' },
			data: formData
		})
	}

	const showMissingMetsWarning = () => {
		setAlertContent && setAlertContent({ msg: 'Du må velge en METS-fil før du kan laste den opp.', type: 'warning' })
	}

	const validate = ( event: React.FormEvent<HTMLFormElement> ) => {
		const performAction = async () => {
			if (!metsFile) {
				showMissingMetsWarning()
				return
			}
			await sendFile()
		}
		event.preventDefault()
		performAction()
	}

	useEffect(() => {
		if ( data ) {
			setMetadataId && setMetadataId(data.id)
			setAlertContent && setAlertContent({ msg: `${data.filnavn} ble lastet opp.`, type: 'info' })
			handleNext && handleNext()
		}
	}, [data])

	useEffect(() => {
		error && setAlertContent && setAlertContent({ msg: 'Det skjedde en feil under opplasting av filen.', type: 'error' })
	}, [error])


	return (
		<Grid container direction='column' justify='center'>
			<Grid item style={{ margin: 'auto' }}>
				<DragDropFile
					selectedFile={metsFile}
					setSelectedFile={setMetsFile}
				/>
			</Grid>
			<form onSubmit={validate} className={sharedClasses.styledForm}>
				<Grid
					container
					item
					alignItems='center'
					justify='center'
					spacing={3}
					style={{ marginTop: '1rem' }}
				>
					<Grid item xs={12} sm={6}>
						<Button
							variant='outlined'
							type='button'
							className={sharedClasses.fullWidth}
							onClick={handleCancel}
						>
						Avbryt
						</Button>
					</Grid>
					<Grid item xs={12} sm={6}>
						<Button
							variant='outlined'
							color="primary"
							type='submit'
							className={sharedClasses.fullWidth}
						>
						Kvalitetssjekk
						</Button>
					</Grid>
				</Grid>
			</form>
		</Grid>
	)
}

export default FileUpload
