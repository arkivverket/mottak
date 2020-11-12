import React from 'react'
import ArkivuttrekkTable from './ArkivuttrekkTable'

/**
 * Display all arkivuttrekk as table data.
 */
const AllArkivuttrekk: React.FC = ():JSX.Element => {

	return (
		<>
			<h2>Alle arkivuttrekk</h2>
			<ArkivuttrekkTable pagination={false}/>
		</>
	)
}

export default AllArkivuttrekk
