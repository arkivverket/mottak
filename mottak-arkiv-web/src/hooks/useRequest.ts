import axios, { AxiosPromise, AxiosRequestConfig } from 'axios'
import { useReducer, useRef } from 'react'
import axiosAPI from '../request'

type Action<T> = { type: 'PENDING' } | { type: 'SUCCESS'; payload: T } | { type: 'ERROR', payload: string };

type Method = 'DELETE' | 'PATCH' | 'POST' | 'GET'

interface State<T> {
	data: T | null;
	error: any;
	loading: boolean;
}

type RequestType = {
	url: any,
	method?: Method,
	headers?: AxiosRequestConfig['headers'],
	data?: AxiosRequestConfig['data'],
	params?: AxiosRequestConfig['params']
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

const useRequest = <T>() => {
	const componentIsMounted = useRef(true)

	const [{ data, error, loading }, dispatch] = useReducer(getReducer<T>(), {
		data: null,
		error: false,
		loading: false,
	})

	const performRequest = async({
		url,
		method = 'GET',
		headers = null,
		data = null,
		params = null }: RequestType ) => {
		const source = axios.CancelToken.source()

		let settings = <{
			method: Method,
			headers?: AxiosRequestConfig['headers'],
			data?: AxiosRequestConfig['data'],
			params?: AxiosRequestConfig['params'],
			cancelToken?: AxiosRequestConfig['cancelToken']}>{ method }


		dispatch({ type: 'PENDING' })

		switch (method) {
			case 'POST':
			case 'PATCH':
			case 'DELETE': {
				settings = {
					...settings,
					headers: { headers },
					data,
				}
				break
			}
			default: {
				settings = {
					...settings,
					params,
					cancelToken: source.token
				}
			}
		}

		try {
			const axiosPromise: AxiosPromise<T> = axiosAPI(url, settings)
			const result = await axiosPromise
			componentIsMounted.current && dispatch({ type: 'SUCCESS', payload: result.data })
		} catch (error) {
			if (!axios.isCancel(error)) {
				componentIsMounted.current && dispatch({ type: 'ERROR', payload: error })
			}
		}
		source.cancel()
	}

	return { data, error, loading, performRequest }
}

export default useRequest

