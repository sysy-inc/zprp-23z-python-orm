import { useQueryClient, useMutation } from '@tanstack/react-query';
import { RowType, getTableDataQueryOptions } from './get-table-data';
import { MutationConfig } from '../lib/react-query';


type EditTableRowOptions = {
    tableName: string,
    oldRow: RowType,
    newRow: RowType
}
function editTableRow({ tableName, oldRow, newRow }: EditTableRowOptions) {
    const set = Object.entries(newRow).map(([key, value]) => `${key} = '${value}'`).join(', ')
    const where = Object.entries(oldRow).map(([key, value]) => `${key} = '${value}'`).join(' AND ')
    const body = JSON.stringify({
        query: `UPDATE ${tableName} SET ${set} WHERE ${where}`
    })
    console.log(body)
    return fetch(`http://localhost:8000/db/query`, {
        method: "POST",
        body: body,
        headers: {
            'Content-Type': 'application/json'
        }
    })
}


type UseEditTableRowOptions = {
    mutationConfig: MutationConfig<typeof editTableRow>
}
export function useEditTableRow({ mutationConfig }: UseEditTableRowOptions) {
    const queryClient = useQueryClient()
    const { onSuccess, ...restConfig } = mutationConfig || {}

    return useMutation({
        ...restConfig,
        mutationFn: ({ tableName, oldRow, newRow }) => editTableRow({ tableName, oldRow, newRow }),
        onSuccess: (...args) => {
            queryClient.invalidateQueries({
                queryKey: getTableDataQueryOptions({ tableName: args[1].tableName }).queryKey
            })
            onSuccess?.(...args)
        }
    })
}
