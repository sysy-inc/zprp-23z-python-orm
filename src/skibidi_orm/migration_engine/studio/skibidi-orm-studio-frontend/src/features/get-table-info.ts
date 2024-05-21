import { useQuery, queryOptions } from '@tanstack/react-query'
import { QueryConfig } from '@/lib/react-query'


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

function getTableInfo(): Promise<QueryTable[]> {
    return fetch(`http://localhost:8000/db`) as any
}

export function getTableInfoQueryOptions() {
    return queryOptions({
        queryKey: ['tableInfo'],
        queryFn: () => getTableInfo(),
    });
}

type UseTableInfoOptions = {
    queryConfig?: QueryConfig<typeof getTableInfoQueryOptions>
}

export function useTableInfo({ queryConfig }: UseTableInfoOptions) {
    return useQuery({
        ...getTableInfoQueryOptions(),
        ...queryConfig
    })
}
