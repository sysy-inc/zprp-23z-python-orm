import { useCommands } from "@/hooks/useCommandsHistory"
import { toast } from "react-hot-toast"
import { BsBoxArrowInUpRight } from "react-icons/bs"
import { RxCaretSort } from "react-icons/rx"
import { Button } from "./ui/button"
import { Dialog, DialogContent, DialogTrigger } from "./ui/dialog"

export function CommandsHisotryDialog() {
    const { commandsHistory, setCurrentCommand } = useCommands()

    return (
        <Dialog>
            <DialogTrigger className='inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2 dark:bg-zinc-900'>
                <RxCaretSort className='w-6 h-6' />
                <p>Commands history</p>
            </DialogTrigger>
            <DialogContent className='flex flex-col gap-2 pt-10 max-h-[70vh] w-full max-w-screen-md overflow-auto'>
                {commandsHistory.map((command, index) => (
                    <div key={index} className='font-mono border bg-zinc-100 px-3 py-2 rounded-md relative dark:bg-zinc-900' >
                        <p dangerouslySetInnerHTML={{ __html: command.split('\n').join('<br />') }}></p>
                        <Button
                            variant={'ghost'}
                            className='border bg-white flex items-center justify-center absolute right-1 top-1 p-[6px] aspect-square w-[32px] h-[32px] dark:bg-zinc-800 dark:border-zinc-700'
                            onClick={() => {
                                toast.success('Command pasted to workspace!')
                                setCurrentCommand(command)
                            }}
                        >
                            <BsBoxArrowInUpRight className='w-[18px] h-[18px]' />
                        </Button>
                    </div>
                ))}
            </DialogContent>
        </Dialog>
    )
}
