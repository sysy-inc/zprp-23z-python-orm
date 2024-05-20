import { Button } from '@/components/ui/button'
import { QueryColumn, RowType, useQueryStore } from '@/lib/query-store'
import { createFileRoute } from '@tanstack/react-router'
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the grid
import { useState } from 'react';
import { ColDef, CellEditingStoppedEvent } from 'ag-grid-community';

export const Route = createFileRoute('/table/$tableName')({
    component: Table
})

function labelRow(row: RowType, columns: QueryColumn[]) {
    const labeledRow: { [key: string]: string } = {}
    let i = 0
    for (const { name } of columns) {
        labeledRow[name] = row[i]
        i++
    }
    return labeledRow
}

export function Table() {
    const { tableName } = Route.useParams()
    const { data } = useQueryStore().tableData<RowType>(tableName)
    const tableColumns = useQueryStore().tablesInfo().data.find(table => table.name === tableName)?.columns

    if (!data || !tableColumns) {
        return null
    }

    const labeledData = data.map(row => labelRow(row, tableColumns))
    const columnDefs: ColDef[] = tableColumns.map(column => ({
        headerName: column.name,
        field: column.name,
        filter: true,
        editable: true,
        cellEditor: 'agTextCellEditor',
    }))

    function onCellEditingStopped(e: CellEditingStoppedEvent) {
        if (e.oldValue === e.newValue) return
        console.log(e)
        e.oldValue
    }


    return (
        <div className='ag-theme-quartz h-[90vh]'
        >
            <AgGridReact
                rowData={labeledData}
                columnDefs={columnDefs}
                onCellEditingStopped={onCellEditingStopped}
            />
        </div>
    )
}
