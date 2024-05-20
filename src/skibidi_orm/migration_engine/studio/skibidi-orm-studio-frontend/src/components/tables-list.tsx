import { useQueryStore } from "@/lib/query-store"

export const TablesList = () => {
    const { data } = useQueryStore().tables()

    return (
        <div>
            {data.map((table) => {
                return (
                    <div>
                        <p>dsdasd</p>
                        <p>{table.name}</p>
                    </div>
                )
            })}
        </div>
    )
}
