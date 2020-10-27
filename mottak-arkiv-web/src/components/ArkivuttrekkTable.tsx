import React, { useEffect } from 'react'
import {
	TableBody,
} from '@material-ui/core'
import { ArkivUttrekk } from '../types/sharedTypes'
import ArkivuttrekkRow from './ArkivuttrekkRow'
import useRequest from '../hooks/useRequest'
import useTable from '../hooks/useTable'


/**
 * Get and display arkivuttrekk as table data.
 */
const ArkivuttrekkTable: React.FC = ():JSX.Element => {
	const columns = [
		{
			id: 'icon',
			label: '',
		},
		{
			id: 'tittel',
			label: 'Tittel',
		},
		{
			id: 'type',
			label: 'Type',
		},
		{
			id: 'avgiver_navn',
			label: 'Avgivers navn',
		},
		{
			id: 'status',
			label: 'Status',
		}
	]

	const { data, loading, error, performRequest } = useRequest<ArkivUttrekk[]>()

	useEffect(() => {
		performRequest({
			url: '/arkivuttrekk',
			method: 'GET',
		})
	}, [])

	const handleTableChange = (skip: number, limit: number) => {
		performRequest({
			url: `/arkivuttrekk?skip=${skip}&limit=${limit}`,
			method: 'GET',
		})
	}

	const { TblContainer, TblHead } = useTable(columns, handleTableChange)

	return (
		<TblContainer>
			<TblHead />
			<TableBody>
				{data?.length && data.map((arkivUttrekk: ArkivUttrekk) => (
					<ArkivuttrekkRow key={arkivUttrekk.id} arkivUttrekk={arkivUttrekk} />
				))}
			</TableBody>
		</TblContainer>
	)
}

export default ArkivuttrekkTable
