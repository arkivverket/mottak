import React, { useContext, useEffect } from 'react'
import {
	Button,
	Stepper,
	Step,
	StepLabel,
	Grid,
} from '@material-ui/core'
import { useHistory } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'

import { useSharedStyles } from '../../styles/sharedStyles'
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

const WorkflowStepper: React.FC = (): JSX.Element => {
	const [activeStep, setActiveStep] = React.useState(0)
	const { steps } = useContext(WorkflowContext)

	const classes = useStyles()
	const sharedClasses = useSharedStyles()

	const history = useHistory()

	const step = steps?.find(({ number }) => number === activeStep)

	const handleNext = ( event: React.FormEvent<HTMLFormElement> ) => {
		const action = steps && steps[activeStep]?.action
		if (!action) return
		const updateStep = async () => {
			await action()
			setActiveStep(prevActiveStep => prevActiveStep + 1)
		}
		event.preventDefault()
		updateStep()
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
		<Grid
			container
			direction='column'
			justify='space-around'
			alignItems='center'
			spacing={5}
		>
			<Grid item>
				<Stepper alternativeLabel activeStep={activeStep} style={{ width: '40vw' }}>
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
			<Grid
				container
				item
				justify='center'
			>
				<form onSubmit={handleNext} className={sharedClasses.styledForm}>
					<Grid
						container
						item
						alignItems='center'
						justify='center'
						spacing={2}
					>
						<Grid item>
							<Button
								variant='outlined'
								type='button'
								className={sharedClasses.buttonDA}
								onClick={handleCancel}
							>
								Avbryt
							</Button>
						</Grid>
						<Grid item>
							<Button
								variant='outlined'
								type='submit'
								className={sharedClasses.buttonDA}
							>
								{step?.buttonLabel}
							</Button>
						</Grid>
					</Grid>
				</form>
			</Grid>
		</Grid>
	)
}

export default WorkflowStepper
