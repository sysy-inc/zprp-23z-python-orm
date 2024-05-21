import { useMutation } from '@tanstack/react-query';
import { MutationConfig } from '../lib/react-query';


type RunCommandOptions = {
    command: string
}
async function runCommand({ command }: RunCommandOptions) {
    const body = JSON.stringify({
        query: command
    })
    const res = await fetch(`http://localhost:8000/db/query`, {
        method: "POST",
        body: body,
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const data = await res.json()
    return data
}


type UseRunCommandOptions = {
    mutationConfig: MutationConfig<typeof runCommand>
}
export function useRunCommand({ mutationConfig }: UseRunCommandOptions) {
    const { onSuccess, ...restConfig } = mutationConfig || {}

    return useMutation({
        ...restConfig,
        mutationFn: ({ command }) => runCommand({ command }),
        onSuccess: (...args) => {
            onSuccess?.(...args)
        }
    })
}
