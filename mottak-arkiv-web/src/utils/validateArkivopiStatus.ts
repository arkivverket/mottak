import { ArkivkopiStatus } from 'src/types/sharedTypes'

export default (status: string): boolean => Object.values(ArkivkopiStatus).includes(status as any)
