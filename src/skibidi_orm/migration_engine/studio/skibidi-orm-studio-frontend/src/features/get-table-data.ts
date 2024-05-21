import { useQuery, queryOptions, QueryKey, UseQueryOptions } from '@tanstack/react-query'
import { QueryConfig, ReqQueryOptions } from '@/lib/react-query'

export type RowType = {
    [key: string]: string
}

type GetTableDataOptions = {
    tableName: string,
    offset?: number,
    limit?: number
}
function getTableData({ tableName, offset = 0, limit = 100 }: GetTableDataOptions): Promise<RowType[]> {
    return fetch(`http://localhost:8000/db/${tableName}/rows?offset=${offset}&limit=${limit}`) as any
}

export function getTableDataQueryOptions({ tableName, offset = 0, limit = 100 }: GetTableDataOptions): ReqQueryOptions<typeof getTableData> {
    return {
        queryKey: ['tableData', tableName],
        queryFn: () => getTableData({ tableName, limit, offset }),
    };
}

type UseTableDataOptions<T> = {
    tableName: string,
    offset?: number,
    limit?: number
    queryConfig?: QueryConfig<typeof getTableData, T>
}

export function useTableData<T>({ tableName, queryConfig, offset = 0, limit = 100 }: UseTableDataOptions<T>) {
    return useQuery({
        ...getTableDataQueryOptions({ tableName, offset, limit }),
        ...queryConfig
    })
}
