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
    const tables = () => useQuery({
        queryKey: ['tablesData'],
        initialData: [],
        queryFn: async () => {
            const response = await fetch('http://localhost:8000/db')
            const data = await response.json()
            return data.tables as QueryTable[]
        },
    })

    return {
        tables,
    }
}
