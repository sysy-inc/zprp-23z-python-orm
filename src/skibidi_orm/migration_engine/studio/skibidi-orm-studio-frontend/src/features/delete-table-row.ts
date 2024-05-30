import { useQueryClient, useMutation } from '@tanstack/react-query';
import { RowType, getTableDataQueryOptions } from './get-table-data';
import { MutationConfig } from '../lib/react-query';


type DeleteTableRowOptions = {
    tableName: string,
    row: RowType
}
function deleteTableRow({ tableName, row }: DeleteTableRowOptions) {
    const where = Object.entries(row).map(([key, value]) => `${key} = '${value}'`).join(' AND ')
    const body = JSON.stringify({
        query: `DELETE FROM ${tableName} WHERE ${where}`
    })
    return fetch(`http://localhost:8000/db/query`, {
        method: "POST",
        body: body,
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

type UseDeleteTableRowOptions = {
    mutationConfig: MutationConfig<typeof deleteTableRow>
}
export function useDeleteTableRow({ mutationConfig }: UseDeleteTableRowOptions) {
    const queryClient = useQueryClient()
    const { onSuccess, ...restConfig } = mutationConfig || {}

    return useMutation({
        ...restConfig,
        mutationFn: ({ tableName, row }) => deleteTableRow({ tableName, row }),
        onSuccess: (...args) => {
            queryClient.invalidateQueries({
                queryKey: getTableDataQueryOptions({ tableName: args[1].tableName }).queryKey
            })
            onSuccess?.(...args)
        }
    })
}
