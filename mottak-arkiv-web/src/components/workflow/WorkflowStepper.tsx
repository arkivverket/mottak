import React, { useContext, useEffect } from 'react'
import {
	Stepper,
	Step,
	StepLabel,
	Grid,
} from '@material-ui/core'
import { useHistory } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'

import { WorkflowContext } from './InvitationWorkflowContainer'

const useStyles = makeStyles(theme => ({
	root: {
		'&.active': {
			color: theme.palette.primary,
		},
		'&.completed': {
			color: theme.palette.primary,
		},
	}
}))

export type ContextType = ({
	handleNext: () => void,
	handleCancel: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void,
})

export const StepperContext = React.createContext<Partial<ContextType>>({})

/**
 * Handle and display step-labels and current step in workflow.
 */
const WorkflowStepper: React.FC = (): JSX.Element => {
	const [activeStep, setActiveStep] = React.useState(0)
	const { steps } = useContext(WorkflowContext)
	const classes = useStyles()
	const history = useHistory()

	const step = steps?.find(({ number }) => number === activeStep)

	const handleNext = () => {
		setActiveStep(prevActiveStep => prevActiveStep + 1)
	}

	const handleCancel = ( event: React.MouseEvent<HTMLButtonElement, MouseEvent> ) => {
		event.preventDefault()
		history.push('/')
	}

	useEffect(() => {
		if (steps && (activeStep >= steps.length)) {
			history.push('/')
		}
	}, [activeStep])

	return (
		<StepperContext.Provider value={{ handleNext, handleCancel }}>
			<Grid
				container
				direction='column'
				justify='space-around'
				alignItems='center'
			>
				<Grid item>
					<Stepper
						alternativeLabel
						activeStep={activeStep}
						style={{ width: '50vw' }}
						data-testid='stepper'
					>
						{steps?.map(step => (
							<Step key={step.number}>
								<StepLabel className={classes.root}>
									{step.label}
								</StepLabel>
							</Step>
						))}
					</Stepper>
				</Grid>
				<Grid item>
					{step?.component}
				</Grid>
			</Grid>
		</StepperContext.Provider>
	)
}

export default WorkflowStepper
