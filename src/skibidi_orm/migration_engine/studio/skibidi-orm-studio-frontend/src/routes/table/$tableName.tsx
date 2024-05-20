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
import { Textarea } from '@/components/ui/textarea';
import { FaCog } from "react-icons/fa";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { RxCaretSort } from "react-icons/rx";


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
                        ref={gridRef}
                        rowData={labeledData}
                        columnDefs={columnDefs}
                        onCellEditingStopped={onCellEditingStopped}
                    />
                </ResizablePanel>
                <div className='relative'>
                    <div className='absolute w-[50px] h-[55px] z-10 -translate-x-1/2 left-1/2 top-1/2 flex items-center justify-center gap-[5px]'>
                        <div className='h-[50%] bg-zinc-200 w-[4px] rounded-md'>

                        </div>
                        <div className='h-full w-[4px] bg-zinc-200 rounded-md'>

                        </div>
                        <div className='h-[50%] w-[4px] bg-zinc-200 rounded-md'>

                        </div>
                    </div>
                    <ResizableHandle className='opacity-100 bg-transparent mx-1 h-full z-20' />
                </div>
                <ResizablePanel className='relative flex'>
                    <div className='h-full flex-1'>
                        <div className='bg-zinc-100 rounded-tl-md px-4 py-4 border-t border-l'>
                            <p className='font-medium'>write queries</p>
                        </div>
                        <Textarea
                            className=' h-full rounded-t-none outline-none border-r-0'
                            placeholder='SELECT * FROM table...'
                        />
                    </div>
                    <div className='py-4 px-4 min-w-[200px] bg-zinc-100 border-t border-l flex flex-col gap-4'>
                        <Button
                            className='w-full flex items-center justify-center gap-2'
                            variant='default'
                        >
                            <FaCog />
                            <p>run query</p>
                        </Button>
                        <Button variant={'outline'} className='flex items-center justify-center gap-1'>
                            <RxCaretSort className='w-6 h-6' />
                            <p>Commands history</p>
                        </Button>
                    </div>
                </ResizablePanel>
            </ResizablePanelGroup>
        </div>
    )
}
