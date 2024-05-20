import { useQuery } from '@tanstack/react-query'

type QueryConstraint = {
    constraint_type: string
    table_name: string
    column_name: string
}

type QueryColumn = {
    name: string
    data_type: string
    constraints: QueryConstraint[]
}

type QueryTable = {
    name: string
    columns: QueryColumn[]
}

export const useQueryStore = () => {
    const tablesInfo = () => useQuery({
        queryKey: ['tablesInfo'],
        initialData: [],
        queryFn: async () => {
            const response = await fetch('http://localhost:8000/db')
            const data = await response.json()
            return data.tables as QueryTable[]
        },
    })

    const tableData = <RowT,>(tableName: string, offset: number = 0, limit: number = 100) => useQuery({
        queryKey: ['tableData', tableName],
        initialData: [],
        queryFn: async () => {
            const response = await fetch(`http://localhost:8000/db/${tableName}/rows?offset=${offset}&limit=${limit}`)
            const data = await response.json()
            return data as RowT[]
        },
    })

    return {
        tablesInfo,
        tableData,
    }
}
