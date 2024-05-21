import { WorkspaceEditor } from '@/components/WorkspaceEditor';
import { CommandsHisotryDialog } from '@/components/commands-hisotry-dialog';
import { Button } from '@/components/ui/button';
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable';
import { useDeleteTableRow } from '@/features/delete-table-row';
import { useEditTableRow } from '@/features/edit-row';
import { RowType, useTableData } from '@/features/get-table-data';
import { QueryColumn, useTableInfo } from '@/features/get-table-info';
import { useCommands } from '@/hooks/useCommandsHistory';
import { createFileRoute } from '@tanstack/react-router';
import { CellEditingStoppedEvent, ColDef, ICellRendererParams } from 'ag-grid-community';
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the grid
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import { useRef } from 'react';
import { FaCog } from "react-icons/fa";
import { RiDeleteBinLine } from "react-icons/ri";

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
    const { saveCommand, currentCommand } = useCommands()
    const gridRef = useRef<AgGridReact>(null)
    const { tableName } = Route.useParams()
    const { data: tableColumns } = useTableInfo<QueryColumn[]>({
        queryConfig: {
            select(data) {
                const found = data.find(table => table.name === tableName)?.columns
                if (!found) {
                    throw new Error('table not found')
                }
                return found
            },
        }
    })
    const { data: labeledData, refetch } = useTableData({
        tableName: tableName,
        queryConfig: {
            select(data) {
                if (!tableColumns) {
                    throw new Error('table columns not found')
                }
                return data.map(row => labelRow(row, tableColumns))
            }
        }
    })
    const rowDeleteMutation = useDeleteTableRow({ mutationConfig: { onSuccess: () => refetch() } })
    const rowEditMutation = useEditTableRow({ mutationConfig: { onSuccess: () => refetch() } })

    if (!labeledData || !tableColumns) {
        return null
    }

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
                return (
                    <Button
                        className='flex items-center gap-2 bg-transparent hover:bg-transparent hover:underline text-red-800'
                        variant={'secondary'}
                        onClick={() => {
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
                        <WorkspaceEditor />
                    </div>
                    <div className='py-4 px-4 min-w-[200px] bg-zinc-100 border-t border-l flex flex-col gap-4'>
                        <Button
                            className='w-full flex items-center justify-center gap-2'
                            variant='default'
                            onClick={() => saveCommand(currentCommand)}
                        >
                            <FaCog />
                            <p>run query</p>
                        </Button>
                        <CommandsHisotryDialog />
                    </div>
                </ResizablePanel>
            </ResizablePanelGroup>
        </div>
    )
}
