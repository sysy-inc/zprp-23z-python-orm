import { useTableInfo } from "@/features/get-table-info"
import { Link } from "@tanstack/react-router"

export const TablesList = () => {
    const { data } = useTableInfo()

    return (
        <div className="border rounded-md flex flex-col gap-2">
            {data?.map((table, index) => {
                return (
                    <Link key={index} to={`/table/${table.name}`}>
                        <div className="px-2">
                            <p>{table.name}</p>
                        </div>
                    </Link>
                )
            })}
        </div>
    )
}
