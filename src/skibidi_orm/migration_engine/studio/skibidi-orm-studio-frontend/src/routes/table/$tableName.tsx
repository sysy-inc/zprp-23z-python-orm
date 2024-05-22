import { WorkspaceEditor } from '@/components/WorkspaceEditor';
import { CommandsHisotryDialog } from '@/components/commands-hisotry-dialog';
import { QueryResultsTable } from '@/components/queryResultsTable';
import { useTheme } from '@/components/theme-provider';
import { Button } from '@/components/ui/button';
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable';
import { useDeleteTableRow } from '@/features/delete-table-row';
import { useEditTableRow } from '@/features/edit-row';
import { useTableData } from '@/features/get-table-data';
import { QueryColumn, useTableInfo } from '@/features/get-table-info';
import { useRunCommand } from '@/features/run-command';
import { useCommandResult } from '@/hooks/useCommandResult';
import { useCommands } from '@/hooks/useCommandsHistory';
import { labelRow } from '@/lib/table-data-utils';
import { cn } from '@/lib/utils';
import { createFileRoute } from '@tanstack/react-router';
import { CellEditingStoppedEvent, ColDef, ICellRendererParams } from 'ag-grid-community';
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import { useEffect, useRef } from 'react';
import { FaCog } from "react-icons/fa";
import { RiDeleteBinLine } from "react-icons/ri";

export const Route = createFileRoute('/table/$tableName')({
    component: Table
})


export function Table() {
    const { theme } = useTheme()
    const { saveCommand, currentCommand } = useCommands()
    const { commandResult, setCommandResult } = useCommandResult()
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
    const commandMutation = useRunCommand({
        mutationConfig: {
            onSuccess(data) {
                setCommandResult(data)
            },
        }
    })

    useEffect(() => {
        console.log('commandResult', commandResult)
    }, [commandResult])

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

    function handleRunCommand() {
        saveCommand(currentCommand)
        commandMutation.mutate({ command: currentCommand })
    }

    return (
        <div className='h-full flex flex-1 flex-col'>
            <ResizablePanelGroup direction='horizontal' className='flex-1'>
                <ResizablePanel className={cn(theme === 'dark' ? `ag-theme-quartz-dark` : 'ag-theme-quartz')}>
                    <AgGridReact
                        ref={gridRef}
                        rowData={labeledData}
                        columnDefs={columnDefs}
                        onCellEditingStopped={onCellEditingStopped}
                    />
                </ResizablePanel>
                <div className='relative'>
                    <div className='absolute w-[50px] h-[55px] z-10 -translate-x-1/2 left-1/2 top-1/2 flex items-center justify-center gap-[5px]'>
                        <div className='h-[50%] bg-zinc-200 w-[4px] rounded-md dark:bg-zinc-500'>

                        </div>
                        <div className='h-full w-[4px] bg-zinc-200 rounded-md dark:bg-zinc-500'>

                        </div>
                        <div className='h-[50%] w-[4px] bg-zinc-200 rounded-md dark:bg-zinc-500'>

                        </div>
                    </div>
                    <ResizableHandle className='opacity-100 bg-transparent mx-1 h-full z-20' />
                </div>
                <ResizablePanel className='relative flex'>
                    <ResizablePanelGroup direction='vertical'>
                        <ResizablePanel className='relative flex'>
                            <div className='h-full flex-1'>
                                <div className='bg-zinc-100 rounded-tl-md px-4 py-4 border-t border-l dark:bg-zinc-900'>
                                    <p className='font-medium text-sm'>write queries</p>
                                </div>
                                <WorkspaceEditor />
                            </div>
                            <div className='py-4 px-4 min-w-[200px] bg-zinc-100 border-t border-l flex flex-col gap-4 dark:bg-zinc-900'>
                                <Button
                                    className='w-full flex items-center justify-center gap-2 dark:bg-zinc-200'
                                    variant='default'
                                    onClick={() => handleRunCommand()}
                                >
                                    <FaCog />
                                    <p>run query</p>
                                </Button>
                                <CommandsHisotryDialog />
                            </div>
                        </ResizablePanel>
                        <ResizableHandle />
                        <ResizablePanel className='flex flex-col'>
                            <p className='font-medium bg-zinc-100 px-4 py-3 border-l dark:bg-zinc-900 text-sm'>query results</p>
                            <QueryResultsTable />
                        </ResizablePanel>
                    </ResizablePanelGroup>
                </ResizablePanel>
            </ResizablePanelGroup>
        </div>
    )
}
