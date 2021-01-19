module.exports = {
	roots: ['<rootDir>/'],
	preset: 'ts-jest',
	testEnvironment: 'jsdom',
	moduleFileExtensions: ['ts', 'tsx', 'js', 'json', 'jsx'],
	moduleDirectories: ['node_modules', 'src', 'test'],
	moduleNameMapper: {
		'\\.(css|less|sass|scss)$': 'identity-obj-proxy',
		'\\.(gif|ttf|eot|svg|png)$': '<rootDir>/src/__tests__/__mocks__/fileMock.js',
		'^src/(.*)': '<rootDir>/src/$1',
	},
	testPathIgnorePatterns: [
		'<rootDir>/node_modules/',
		'<rootDir>/src/__tests__/(.eslintrc.js|jest.setup.ts)',
		'<rootDir>/src/__tests__/__mocks__/',
	],
	transformIgnorePatterns: ['[/\\\\]node_modules[/\\\\].+\\.(ts|tsx)$'],
	watchPlugins: ['jest-watch-typeahead/filename', 'jest-watch-typeahead/testname'],
	setupFilesAfterEnv: ['<rootDir>/src/__tests__/jest.setup.ts'],
}
