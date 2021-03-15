import { useLayoutEffect, useCallback, useState } from 'react'

import { useRequest } from 'src/hooks'
import { validateArkivopiStatus } from 'src/utils'

import { ArkivkopiStatusRequest, ArkivkopiStatus } from 'src/types/sharedTypes'

type ExecuteType = () => void
type DownloadStatusState = ArkivkopiStatus | 'Ukjent status' | 'Ikke bestilt'

interface State {
	data: ArkivkopiStatusRequest | null
	status: DownloadStatusState
	error: any
	disable: boolean
	loading: boolean
	performRequest: ExecuteType
}

interface Props {
	url: string
	statusInterval: number
}

const useArkivkopi = ({ url, statusInterval }: Props): State => {
	const [disable, setDisable] = useState<boolean>(false)
	const [loading, setLoading] = useState<boolean>(false)
	const [status, setStatus] = useState<DownloadStatusState>('Ikke bestilt')
	const { data, error, performRequest: request } = useRequest<ArkivkopiStatusRequest>()
	const { data: dataStatus, performRequest: getStatus } = useRequest<ArkivkopiStatusRequest>()

	const statusURL = `${url}/status`

	const performRequest = useCallback<ExecuteType>(async () => {
		if (disable) return

		setDisable(true)
		setLoading(true)

		await request({
			url,
			method: 'POST',
		})
	}, [disable, url, request])

	useLayoutEffect(() => {
		setLoading(false)

		if (!data) return
		setStatus(ArkivkopiStatus.BESTILT)
	}, [data])

	useLayoutEffect(() => {
		setDisable(false)
		setLoading(false)
	}, [error])

	useLayoutEffect(() => {
		getStatus({ url: statusURL })

		const interval = setInterval(() => {
			getStatus({ url: statusURL })
		}, statusInterval)

		return () => {
			clearInterval(interval)
		}

		// @TODO: Figure out why useRequest causes infinte requests
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [])

	useLayoutEffect(() => {
		if (!dataStatus) return
		const { status } = dataStatus

		setStatus(validateArkivopiStatus(status) ? status : 'Ukjent status')
		setLoading(false)

		switch (status) {
			case ArkivkopiStatus.FEILET:
				setDisable(false)
				break

			default:
				setDisable(true)
				break
		}
	}, [dataStatus])

	return { data, status, error, disable, loading, performRequest }
}
export default useArkivkopi
