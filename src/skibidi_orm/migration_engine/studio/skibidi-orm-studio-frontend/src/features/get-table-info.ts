import { QueryConfig, ReqQueryOptions } from '@/lib/react-query'
import { useQuery } from '@tanstack/react-query'


export type QueryConstraint = {
    constraint_type: string
    table_name: string
    column_name: string
}

export type QueryColumn = {
    name: string
    data_type: string
    constraints: QueryConstraint[]
}

export type QueryTable = {
    name: string
    columns: QueryColumn[]
}

async function getTableInfo(): Promise<QueryTable[]> {
    const res = await fetch(`http://localhost:8000/db`) as any
    const data = await res.json()
    return data.tables as QueryTable[]
}

export function getTableInfoQueryOptions(): ReqQueryOptions<typeof getTableInfo> {
    return {
        queryKey: ['tableInfo'],
        queryFn: () => getTableInfo(),
    }
}

type UseTableInfoOptions<T> = {
    queryConfig?: QueryConfig<typeof getTableInfo, T>;
};
export function useTableInfo<T = QueryTable[]>({ queryConfig }: UseTableInfoOptions<T> = {}) {
    return useQuery({
        ...getTableInfoQueryOptions(),
        ...queryConfig
    })
}
