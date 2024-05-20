import { useQueryStore } from "@/lib/query-store"
import { Link } from "@tanstack/react-router"

export const TablesList = () => {
    const { data } = useQueryStore().tables()

    return (
        <div className="border rounded-md flex flex-col gap-2">
            {data.map((table) => {
                return (
                    <Link to={`/table/${table.name}`}>
                        <div className="px-2">
                            <p>{table.name}</p>
                        </div>
                    </Link>
                )
            })}
        </div>
    )
}
