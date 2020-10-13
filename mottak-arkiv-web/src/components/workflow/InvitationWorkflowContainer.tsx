import React, { FC } from 'react'
import WorkflowStepper from './WorkflowStepper'
import FileUpload, { sendFile } from '../FileUpload'
import QualityCheck from '../QualityCheck'

export type ContextType = ({
	metsFile: File | null,
	setMetsFile: React.Dispatch<React.SetStateAction<File | null>>,
	metadataId: number | null,
	setMetadataId: React.Dispatch<React.SetStateAction<number | null>>,
	steps: {
		number: number,
		label: string,
		buttonLabel: string,
		action: (() => void) | null,
		component: JSX.Element,
	}[]
})

export const WorkflowContext = React.createContext<Partial<ContextType>>({})

const InvitationWorkflowContainer: React.FC<{ children: unknown }> = ({ children }): JSX.Element => {
	const [metsFile, setMetsFile] = React.useState<File | null>(null)
	const [metadataId, setMetadataId] = React.useState<number | null>(null)

	const steps = [
		{
			number: 0,
			label: 'Last opp fil',
			buttonLabel: 'Last opp',
			action: metsFile ? sendFile : null,
			component: <FileUpload />
		},
		{
			number: 1,
			label: 'Godkjenn verdier',
			buttonLabel: 'Godkjenn',
			action: () => console.warn('send form'),
			component: <div>fil</div>
		},
	]

	return (
		<WorkflowContext.Provider value={{ metsFile, setMetsFile, metadataId, setMetadataId, steps }}>
			<WorkflowStepper />
		</WorkflowContext.Provider>
	)
}

export default InvitationWorkflowContainer
