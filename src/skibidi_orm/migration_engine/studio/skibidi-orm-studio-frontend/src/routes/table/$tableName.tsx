import { Button } from '@/components/ui/button'
import { QueryColumn, RowType, useQueryStore } from '@/lib/query-store'
import { createFileRoute } from '@tanstack/react-router'
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the grid
import { useRef, useState } from 'react';
import { ColDef, CellEditingStoppedEvent, ICellRendererParams } from 'ag-grid-community';
import { useMutation } from '@tanstack/react-query'
import { RiDeleteBinLine } from "react-icons/ri";
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable';


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
    const gridRef = useRef<AgGridReact>(null)
    const { tableName } = Route.useParams()
    const { data, refetch } = useQueryStore().tableData<RowType>(tableName)
    const tableColumns = useQueryStore().tablesInfo().data.find(table => table.name === tableName)?.columns
    const rowDeleteMutation = useMutation({
        mutationFn: async ({ tableName, row }: { tableName: string, row: RowType }) => {
            const where = Object.entries(row).map(([key, value]) => `${key} = '${value}'`).join(' AND ')
            const body = JSON.stringify({
                query: `DELETE FROM ${tableName} WHERE ${where}`
            })
            console.log(body)
            return fetch(`http://localhost:8000/db/query`, {
                method: "POST",
                body: body,
                headers: {
                    'Content-Type': 'application/json'
                }
            })
        },
        onSuccess: () => {
            refetch()
        }
    })

    const rowEditMutation = useMutation({
        mutationFn: async ({ tableName, oldRow, newRow }: { tableName: string, oldRow: RowType, newRow: RowType }) => {
            const set = Object.entries(newRow).map(([key, value]) => `${key} = '${value}'`).join(', ')
            const where = Object.entries(oldRow).map(([key, value]) => `${key} = '${value}'`).join(' AND ')
            const body = JSON.stringify({
                query: `UPDATE ${tableName} SET ${set} WHERE ${where}`
            })
            console.log(body)
            return fetch(`http://localhost:8000/db/query`, {
                method: "POST",
                body: body,
                headers: {
                    'Content-Type': 'application/json'
                }
            })
        },
        onSuccess: () => {
            refetch()
        }
    })

    if (!data || !tableColumns) {
        return null
    }

    const labeledData = data.map(row => labelRow(row, tableColumns))
    const columnDefs: ColDef[] = [
        ...tableColumns.map(column => ({
            headerName: column.name,
            field: column.name,
            filter: true,
            editable: true,
            cellEditor: 'agTextCellEditor'
        })),
        {
            headerName: '',
            cellRenderer: (params: ICellRendererParams) => {
                // console.log('parr', params)
                return (
                    <Button
                        className='flex items-center gap-2 bg-transparent hover:bg-transparent hover:underline text-red-800'
                        variant={'secondary'}
                        onClick={() => {
                            // console.log("p.n.d", params.node.data)
                            rowDeleteMutation.mutate({
                                tableName,
                                row: params.data
                            })
                        }}
                    >
                        <RiDeleteBinLine />
                        <p>delete</p>
                    </Button>
                )
            }
        }
    ]

    function onCellEditingStopped(e: CellEditingStoppedEvent) {
        if (e.oldValue === e.newValue) return
        console.log('ev', e)
        const newRow = e.data
        const oldRow = { ...e.data, [e.colDef.field!]: e.oldValue }
        rowEditMutation.mutate({
            tableName,
            oldRow: oldRow,
            newRow: newRow
        })
        // e.oldValue
    }


    return (
        <div className='ag-theme-quartz h-[90vh]'
        >
            <ResizablePanelGroup direction='horizontal'>
                <ResizablePanel>
                    <AgGridReact
                        // className='w-[70vw]'
                        ref={gridRef}
                        rowData={labeledData}
                        columnDefs={columnDefs}
                        onCellEditingStopped={onCellEditingStopped}
                    />
                </ResizablePanel>
                <ResizableHandle />
                <ResizablePanel>
                    <div>
                        <Button
                            onClick={() => {
                                refetch()
                            }}
                        >
                            Refresh
                        </Button>
                    </div>
                </ResizablePanel>
            </ResizablePanelGroup>
        </div>
    )
}
