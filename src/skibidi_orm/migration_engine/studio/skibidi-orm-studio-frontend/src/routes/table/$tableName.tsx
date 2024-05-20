import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/table/$tableName')({
  component: () => <div>Hello /table/$tableName!</div>
})
