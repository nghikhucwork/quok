import { ChangeEventHandler, useState } from "react";
import { Button } from "~/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog";
import { Input } from "~/components/ui/input";
import { Label } from "~/components/ui/label";

export function InitialUserNameDialog(props: {open: boolean, onOpenChangeDialog: (b: boolean) => void, submitUserName: (username: string) => void}) {
  const [username, setUserName] = useState<string | undefined>();
  const [error, setError] = useState<boolean | undefined>();
  return (
    <Dialog open={props.open} onOpenChange={props.onOpenChangeDialog}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>User Name</DialogTitle>
          <DialogDescription>
          Your username information
          </DialogDescription>
        </DialogHeader>
        <div className="grid">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="username" className="">
              Username
            </Label>
            <Input
              id="username"
              placeholder="admin"
              className="col-span-3"
              value={username}
              onChange={(e: any) => setUserName(e.target.value)}
            />
          </div>
          {error && <small className="text-[red]">Please input your username</small>}
        </div>
        <DialogFooter>
          <Button type="button" onClick={() => {
            if(!username) return setError(true)
            setError(false)
            props.submitUserName(username as string)
          }}>Save</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
