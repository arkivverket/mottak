import React, { FC } from 'react'
import WorkflowStepper from './WorkflowStepper'
import FileUpload, { sendFile } from '../FileUpload'
import QualityCheck from '../QualityCheck'

export type ContextType = ({
	metsFile: File | null,
	setMetsFile: React.Dispatch<React.SetStateAction<File | null>>,
	stepValid: boolean,
	setStepValid: React.Dispatch<React.SetStateAction<boolean>>,
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
	const [stepValid, setStepValid] = useState<boolean>(false)

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

	useEffect(() => {
		if ( data ) {
			setMetadataId(data.id)
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
