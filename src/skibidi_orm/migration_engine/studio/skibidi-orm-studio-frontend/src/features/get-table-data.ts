import { useQuery, queryOptions } from '@tanstack/react-query'
import { QueryConfig } from '@/lib/react-query'

export type RowType = {
    [key: string]: string
}

type GetTableDataOptions = {
    tableName: string,
    offset?: number,
    limit?: number
}
function getTableData({ tableName, offset = 0, limit = 100 }: GetTableDataOptions): Promise<RowType> {
    return fetch(`http://localhost:8000/db/${tableName}/rows?offset=${offset}&limit=${limit}`) as any
}

function getTableDataQueryOptions({ tableName, offset = 0, limit = 100 }: GetTableDataOptions) {
    return queryOptions({
        queryKey: ['tableData', tableName],
        queryFn: () => getTableData({ tableName, limit, offset }),
    });
}

type UseTableDataOptions = {
    tableName: string,
    offset?: number,
    limit?: number
    queryConfig?: QueryConfig<typeof getTableDataQueryOptions>
}

export function useTableData({ tableName, queryConfig, offset = 0, limit = 100 }: UseTableDataOptions) {
    return useQuery({
        ...getTableDataQueryOptions({ tableName, offset, limit }),
        ...queryConfig
    })
}

const { } = useTableData({
    tableName: 'tableName',
})
