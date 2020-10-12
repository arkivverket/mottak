import axios, { AxiosPromise, AxiosRequestConfig } from 'axios'
import { useEffect, useReducer } from 'react'
import axiosAPI from '../request'

type Action<T> = { type: 'PENDING' } | { type: 'SUCCESS'; payload: T } | { type: 'ERROR' };

interface State<T> {
    loading: boolean;
    error: boolean;
    data: T | null;
}

const getReducer = <T>() => (state: State<T>, action: Action<T>): State<T> => {
	switch (action.type) {
		case 'PENDING':
			return {
				...state,
				loading: true,
			}
		case 'SUCCESS': {
			return {
				...state,
				loading: false,
				error: false,
				data: action.payload,
			}
		}
		case 'ERROR':
			return {
				...state,
				loading: false,
				error: true,
			}
	}
}

const useGetOnMount = <T>(
	url: string,
	params: AxiosRequestConfig | undefined = undefined ): State<T> => {

	const [{ data, error, loading }, dispatch] = useReducer(getReducer<T>(), {
		loading: false,
		error: false,
		data: null,
	})

	const source = axios.CancelToken.source()

	useEffect(() => {
		const performRequest = async () => {
			dispatch({ type: 'PENDING' })
			try {
				const axiosPromise: AxiosPromise<T> = axiosAPI.get(url, {
					params: {
						params
					},
					cancelToken: source.token
				})
				const result = await axiosPromise
				dispatch({ type: 'SUCCESS', payload: result.data })
			} catch (error) {
				if (!axios.isCancel(error)) {
					dispatch({ type: 'ERROR' })
				}
			}
		}
		performRequest()
		return () => {
			source.cancel()
		}
	}, [url, params])

	return { data, error, loading }
}

export default useGetOnMount

