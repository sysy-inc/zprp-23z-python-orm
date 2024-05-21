import { useCommandResult } from "@/hooks/useCommandResult"
import { GridOptions, ColDef } from 'ag-grid-community'
import { AgGridReact } from "ag-grid-react"
import { useMemo, useRef } from "react"
import '@/styles/ag-custom.css'

export function QueryResultsTable() {
    const gridRef = useRef<AgGridReact>(null)
    const { selected: labeledData, commandResult } = useCommandResult({
        select(data) {
            return data.map(row => {
                return row.reduce((acc, value, i) => {
                    acc[i] = value
                    return acc
                }, {} as { [key: string]: string })
            })
        }
    })
    const gridOptions: GridOptions = useMemo(() => ({
        rowData: labeledData,
        columnDefs: commandResult[0] ? commandResult[0].map((_, i): ColDef => ({
            headerName: i.toString(),
            field: i.toString(),
        })) : [],
    }), [labeledData, commandResult])


    return (
        <div id='ag-results' className="w-full h-full">
            <AgGridReact
                ref={gridRef}
                {...gridOptions}
            />
        </div>
    )
}
