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

export type RowType = {
    [key: string]: string
}


export const useQueryStore = () => {
    const queryTablesInfo = () => useQuery({
        queryKey: ['tablesInfo'],
        initialData: [],
        queryFn: async () => {
            const response = await fetch('http://localhost:8000/db')
            const data = await response.json()
            return data.tables as QueryTable[]
        },
    })

    const queryTableData = <RowT,>(tableName: string, offset: number = 0, limit: number = 100) => useQuery({
        queryKey: ['tableData', tableName],
        initialData: [],
        queryFn: async () => {
            const response = await fetch(`http://localhost:8000/db/${tableName}/rows?offset=${offset}&limit=${limit}`)
            const data = await response.json()
            return data as RowT[]
        },
    })

    return {
        tablesInfo: queryTablesInfo,
        tableData: queryTableData,
    }
}
