import axios, { AxiosPromise, AxiosRequestConfig } from 'axios'
import { useEffect, useReducer } from 'react'

import axiosAPI from '../request'

type Action<T> = { type: 'PENDING' } | { type: 'SUCCESS'; payload: T } | { type: 'ERROR'; payload: string };

interface State<T> {
    loading: boolean;
    error: any;
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
				error: action.payload,
			}
	}
}

/**
 * Custom hook to get data from endpoint on mount in the form of a GET request
 *
 * @param {String} url - Endpoint url.
 * @param {AxiosRequestConfig}  params - The URL parameters to be sent with the request.
 */
const useGetOnMount = <T>(
	url: string,
	params?: AxiosRequestConfig | undefined
): State<T> => {
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
					dispatch({ type: 'ERROR', payload: error })
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
