import React, { useState } from 'react'
import WorkflowStepper from './WorkflowStepper'
import FileUpload from '../FileUpload'
import QualityCheck from '../QualityCheck'


export type ContextType = ({
	metadataId: number | null,
	setMetadataId: React.Dispatch<React.SetStateAction<number | null>>,
	steps: {
		number: number,
		label: string,
		component: JSX.Element,
	}[],
})

export const WorkflowContext = React.createContext<Partial<ContextType>>({})

const InvitationWorkflowContainer: React.FC<{ children: unknown }> = ({ children }): JSX.Element => {
	const [metadataId, setMetadataId] = useState<number | null>(null)

	const steps = [
		{
			number: 0,
			label: 'Last opp fil',
			component: <FileUpload />
		},
		{
			number: 1,
			label: 'Godkjenn verdier',
			component: <QualityCheck />
		},
	]

	return (
		<WorkflowContext.Provider value={{ metadataId, setMetadataId, steps }}>
			<WorkflowStepper data-testid='stepper'/>
		</WorkflowContext.Provider>
	)
}

export default InvitationWorkflowContainer
