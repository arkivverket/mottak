import React, { useState } from 'react'
import { ArkivUttrekk,  } from '../../types/sharedTypes'
import WorkflowStepper from './WorkflowStepper'
import FileUpload from './FileUpload'
import QualityCheck from './QualityCheck'
import SendInvitation from './SendInvitation'


export type ContextType = ({
	metadataId: number | null,
	setMetadataId: React.Dispatch<React.SetStateAction<number | null>>,
	arkivUttrekk: ArkivUttrekk | null,
	setArkivUttrekk: React.Dispatch<React.SetStateAction<ArkivUttrekk | null>>,
	steps: {
		number: number,
		label: string,
		component: JSX.Element,
	}[],
})

export const WorkflowContext = React.createContext<Partial<ContextType>>({})

/**
 * Provide context for stepper-workflow
 */
const InvitationWorkflowContainer: React.FC = (): JSX.Element => {
	const [metadataId, setMetadataId] = useState<number | null>(null)
	const [arkivUttrekk, setArkivUttrekk] = useState<ArkivUttrekk | null>(null)

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
		{
			number: 2,
			label: 'Send invitasjon',
			component: <SendInvitation />
		},
	]

	return (
		<WorkflowContext.Provider value={{ metadataId, setMetadataId, arkivUttrekk, setArkivUttrekk, steps }}>
			<WorkflowStepper />
		</WorkflowContext.Provider>
	)
}

export default InvitationWorkflowContainer
