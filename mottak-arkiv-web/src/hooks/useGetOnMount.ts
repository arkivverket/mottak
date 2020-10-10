import axios, { AxiosPromise, AxiosRequestConfig } from 'axios'
import { useEffect, useReducer, useRef } from 'react'

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

	const componentIsMounted = useRef(true)

	const [{ data, error, loading }, dispatch] = useReducer(getReducer<T>(), {
		loading: false,
		error: false,
		data: null,
	})

	useEffect(() => {
		const performRequest = async () => {
			dispatch({ type: 'PENDING' })
			try {
				const axiosPromise: AxiosPromise<T> = axios(url, params)
				const result = await axiosPromise
				componentIsMounted.current && dispatch({ type: 'SUCCESS', payload: result.data })
			} catch (error) {
				componentIsMounted.current && dispatch({ type: 'ERROR' })
			}
		}
		performRequest()
		return () => {
			componentIsMounted.current = false
		}
	}, [url, params])

	return { data, error, loading }
}

export default useGetOnMount

