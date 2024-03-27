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
import { Textarea } from "./ui/textarea";
import { useContext, useState } from "react";
import { GlobalContext } from "~/lib/utils";
import { useMutation } from "@tanstack/react-query";
import { request } from "~/lib/request";

export function CreateNoteItem() {
  const [content, setContent] = useState();
  const [error, setError] = useState(false);
  const [open, setOpen] = useState(false);
  const [global, dispatch, , setDialogInitial] = useContext(
    GlobalContext
  ) as any;
  const mutation = useMutation({
    mutationFn: () => {
      return request
        .post("/", {
          method: "POST",
          body: {
            content,
            username: global.username,
          },
        })
        .then((res: any) => {
          dispatch({
            type: "updateNotes",
            page: global.page,
            notes: {
              ...global.notes,
              1000: [...(global?.notes?.[1000] || []), res.data.data],
            },
          });
        });
    },
  });

  console.log("global.notes", global.notes);

  return (
    <Dialog open={open} onOpenChange={() => setOpen(!open)}>
      <DialogTrigger asChild>
        <Button variant="outline" onClick={() => setOpen(!open)}>
          Create Note
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Note</DialogTitle>
          <DialogDescription>you want to create a note</DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid items-center gap-4">
            <Textarea
              placeholder="content"
              value={content}
              onChange={(e: any) => setContent(e.target.value)}
            />
          </div>
          {error && <small className="text-[red]">Please input content</small>}
        </div>
        <DialogFooter>
          <Button
            type="button"
            disabled={mutation.isPending}
            onClick={async () => {
              if (!content) return setError(true);
              setError(false);
              await mutation.mutateAsync();
              setOpen(false);
            }}
          >
            Save changes
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
