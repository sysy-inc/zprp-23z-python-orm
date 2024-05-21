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

function getTableInfo(): Promise<QueryTable[]> {
    return fetch(`http://localhost:8000/db`) as any
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
export function useTableInfo<T>({ queryConfig }: UseTableInfoOptions<T>) {
    return useQuery({
        ...getTableInfoQueryOptions(),
        ...queryConfig
    })
}
