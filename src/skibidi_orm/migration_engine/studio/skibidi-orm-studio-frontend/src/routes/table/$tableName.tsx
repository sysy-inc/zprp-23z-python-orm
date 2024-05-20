import { useQueryStore } from '@/lib/query-store'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/table/$tableName')({
    component: Table
})

type RowType = {
    [key: string]: string
}

export function Table() {
    const { tableName } = Route.useParams()
    const { data } = useQueryStore().tableData<RowType>(tableName)

    return (
        <div className='flex items-center justify-center'>
            {data.map((row, index) => {
                return (
                    <div key={index} className='border rounded-md p-2'>
                        {Object.entries(row).map(([key, value]) => {
                            return (
                                <div key={key} className='flex gap-2'>
                                    <div className='font-bold'>{key}</div>
                                    <div>{value}</div>
                                </div>
                            )
                        })}
                    </div>
                )
            })}
        </div>
    )
}
