import React from 'react'
import ArkivuttrekkTable from './arkivuttrekk-table/ArkivuttrekkTable'

/**
 * Display all arkivuttrekk as table data.
 */
const AllArkivuttrekk: React.FC = (): JSX.Element => (
	<>
		<h2>Alle arkivuttrekk</h2>
		<ArkivuttrekkTable pagination={false} />
	</>
)

export default AllArkivuttrekk
