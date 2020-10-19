import React, { useContext, useEffect, useState } from 'react'
import WorkflowStepper from './WorkflowStepper'
import FileUpload from '../FileUpload'
import QualityCheck from '../QualityCheck'
import useRequest from '../../hooks/useRequest'
import { AlertContext } from '../WorkArea'
import { MetadataFil } from '../../types/sharedTypes'
//import { boolean } from 'yargs'

export type ContextType = ({
	stepValid: boolean,
	setStepValid: React.Dispatch<React.SetStateAction<boolean>>,
	metsFile: Blob | string,
	setMetsFile: React.Dispatch<React.SetStateAction<Blob | string>>,
	metadataId: number | null,
	setMetadataId: React.Dispatch<React.SetStateAction<number | null>>,
	sendFile: () => void,
	steps: {
		number: number,
		label: string,
		buttonLabel: string,
		//@ts-ignore
		action: any,
		component: JSX.Element,
	}[],
})

export const WorkflowContext = React.createContext<Partial<ContextType>>({})

const InvitationWorkflowContainer: React.FC<{ children: unknown }> = ({ children }): JSX.Element => {
	const [metsFile, setMetsFile] = useState<Blob | string>('')
	const [metadataId, setMetadataId] = useState<number | null>(null)
	const [stepValid, setStepValid] = useState<boolean>(false)
	const { setAlertContent } = useContext(AlertContext)

	const showMissingMetsWarning = () => {
		setAlertContent && setAlertContent({ msg: 'Du må velge en METS-fil før du kan laste den opp.', type: 'warning' })
		setStepValid(false)
	}

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

	const steps = [
		{
			number: 0,
			label: 'Last opp fil',
			buttonLabel: 'Last opp',
			action: metsFile ? sendFile : showMissingMetsWarning,
			component: <FileUpload />
		},
		{
			number: 1,
			label: 'Godkjenn verdier',
			buttonLabel: 'Godkjenn',
			action: () => console.warn('hei'),
			component: <QualityCheck />
		},
	]

	useEffect(() => {
		if ( data ) {
			setMetadataId(data.id)
			setAlertContent && setAlertContent({ msg: `${data.filnavn} ble lastet opp.`, type: 'info' })
			setStepValid(true)
		}
	}, [data])

	useEffect(() => {
		error && setAlertContent && setAlertContent({ msg: 'Det skjedde en feil under opplasting av filen.', type: 'error' })
		setStepValid(false)
	}, [error])

	return (
		<WorkflowContext.Provider value={{ stepValid, setStepValid, metsFile, setMetsFile, metadataId, setMetadataId, steps }}>
			<WorkflowStepper data-testid='stepper'/>
		</WorkflowContext.Provider>
	)
}

export default InvitationWorkflowContainer
