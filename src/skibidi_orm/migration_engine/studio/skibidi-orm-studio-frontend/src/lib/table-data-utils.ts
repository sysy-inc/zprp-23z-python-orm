import { RowType } from "@/features/get-table-data"
import { QueryColumn } from "@/features/get-table-info"

export function labelRow(row: RowType, columns: QueryColumn[]) {
    const labeledRow: { [key: string]: string } = {}
    let i = 0
    for (const { name } of columns) {
        labeledRow[name] = row[i]
        i++
    }
    return labeledRow
}
