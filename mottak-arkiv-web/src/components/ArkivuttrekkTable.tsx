import React, { useContext, useEffect } from 'react'
import {
	CircularProgress,
	TableBody,
} from '@material-ui/core'
import { ArkivUttrekk } from '../types/sharedTypes'
import ArkivuttrekkRow from './ArkivuttrekkRow'
import useRequest from '../hooks/useRequest'
import useTable from '../hooks/useTable'
import { AlertContext } from './WorkArea'


/**
 * Get and display arkivuttrekk as table data.
 */
const ArkivuttrekkTable: React.FC<{ pagination?: boolean }> = ({ pagination = true }):JSX.Element => {
	const columns = [
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
		},
		{
			id: 'icon',
			label: '',
		},
	]

	const { data, loading, error, performRequest } = useRequest<ArkivUttrekk[]>()
	const { setAlertContent } = useContext(AlertContext)

	useEffect(() => {
		error && setAlertContent && setAlertContent({ msg: error?.response?.data?.detail || 'Det skjedde en feil under lasting av arkivuttrekk.', type: 'error' })
	}, [error])

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
		loading ?
			<CircularProgress /> :
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
