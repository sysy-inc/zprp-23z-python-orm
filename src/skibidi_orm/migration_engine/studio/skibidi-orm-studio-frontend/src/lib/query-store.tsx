import { useQuery } from '@tanstack/react-query'

export const useQueryStore = () => {
    const { data } = useQuery({
        queryKey: ['tablesData'],
        initialData: [],
        queryFn: async () => {
            const response = await fetch('http://localhost:4000/tables')
            const data = await response.json()
            return data
        },
    })

    return data
}
