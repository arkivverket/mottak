import React, { useState } from 'react'
import { Button } from '@material-ui/core'
import { getHeapCodeStatistics } from 'v8'


type Props = {
	title: string
}

const WorkArea: React.FC<Props> = ({
	title
}) => {
	const [data, setData] = useState('Ingen data ennå')

	const updateData = () => {
		const getData = async () => {
			try {
				const response = await fetch('http://lego.arkivverket.local/bakom/public/api/index.php/metadata/municipalities')

				const json = await response.json()
				// console.log(json);
				setData(JSON.stringify(json))
			} catch (error) {
				setData('Feil ved lasting av data')
			}
		}

		console.log('clicked')
		getData()
	}

	return (
		<div>
			<Button onClick={updateData} color="primary">{title}</Button>
			<div>{data}</div>
		</div>
	)
}

export default WorkArea
