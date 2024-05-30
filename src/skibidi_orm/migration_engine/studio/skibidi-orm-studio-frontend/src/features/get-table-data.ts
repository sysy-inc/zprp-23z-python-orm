import { QueryConfig, ReqQueryOptions } from '@/lib/react-query'
import { useQuery } from '@tanstack/react-query'

export type RowType = {
    [key: string]: string
}

type GetTableDataOptions = {
    tableName: string,
    offset?: number,
    limit?: number
}
async function getTableData({ tableName, offset = 0, limit = 100 }: GetTableDataOptions): Promise<RowType[]> {
    const res = await fetch(`http://localhost:8000/db/${tableName}/rows?offset=${offset}&limit=${limit}`) as any
    const data = await res.json()
    return data as RowType[]
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

export function useTableData<T = RowType[]>({ tableName, queryConfig, offset = 0, limit = 100 }: UseTableDataOptions<T>) {
    return useQuery({
        ...getTableDataQueryOptions({ tableName, offset, limit }),
        ...queryConfig
    })
}
