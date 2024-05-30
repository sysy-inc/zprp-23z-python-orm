import { useTableInfo } from "@/features/get-table-info";
import { Link } from "@tanstack/react-router";
import { FaDatabase } from "react-icons/fa";
import { ModeToggle } from "./mode-toggle";

export const Sidebar = () => {
    const { data } = useTableInfo()

    return (
        <div className="flex flex-col justify-between h-full px-2 py-4">
            <div className="flex flex-col gap-2">
                {data?.map((table, index) => {
                    return (
                        <Link key={index} to={`/table/${table.name}`} className={`[&.active]:font-medium [&.active]:text-zinc-100 [&:not(active)]:text-muted-foreground`}>
                            <div className="px-2 flex items-center gap-2 ">
                                <FaDatabase className="flex-shrink-0" />
                                <p className="">{table.name}</p>
                            </div>
                        </Link>
                    )
                })}
            </div>
            <ModeToggle />
        </div>
    )
}
