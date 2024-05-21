import { useQuery, queryOptions } from '@tanstack/react-query'
import { QueryConfig } from '@/lib/react-query'
import { RowType } from './get-table-data'



function getTableInfo(): Promise<RowType> {
    return fetch(`http://localhost:8000/db`) as any
}

export function getTableDataQueryOptions() {
    return queryOptions({
        queryKey: ['tableInfo'],
        queryFn: () => getTableInfo(),
    });
}

type UseTableInfoOptions = {
    queryConfig?: QueryConfig<typeof getTableDataQueryOptions>
}

export function useTableData({ queryConfig }: UseTableInfoOptions) {
    return useQuery({
        ...getTableDataQueryOptions(),
        ...queryConfig
    })
}
