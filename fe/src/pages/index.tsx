import Image from "next/image";
import Link from "next/link";
import { Button } from "~/components/ui/button";

import Menu from "~/components/Menu";
import { useContext } from "react";
import { GlobalContext } from "~/lib/utils";
import { Checkbox } from "~/components/ui/checkbox";
import { useMutation } from "@tanstack/react-query";
import { request } from "~/lib/request";
import Note from "~/components/Note";
import { CreateNoteItem } from "~/components/CreateNoteItem";
import { Input } from "~/components/ui/input";
import _ from "lodash";

const awaita = (time: number = 200) =>
  new Promise((res) => {
    setTimeout(() => {
      res(null);
    }, time);
  });

const filterByUserNameAsync = _.debounce(
  (mutation) => {
    mutation.mutateAsync(true);
  },
  200,
  {}
);

export default function Home() {
  const [global, dispatch, , setDialogInitial] = useContext(
    GlobalContext
  ) as any;

  const mutation = useMutation({
    mutationFn: (isFilterName?: boolean) => {
      return request
        .post("/", {
          method: "GET",
          query: {
            username:
              global.byUsername ||
              (global.isFilterAll ? undefined : global.username),
            page: global.page,
          },
        })
        .then((res) => {
          if (!res?.data?.data?.length && !isFilterName) {
            return dispatch({
              type: "setPage",
              page: global.page,
              stop: true,
            });
          }
          console.log("isIdle", res.data.data);
          if (isFilterName) {
            return dispatch({
              type: "updateNotes",
              notes: { [global.page]: res.data.data },
              page: global.page + 1,
            });
          }

          return dispatch({
            type: "updateNotes",
            notes: { ...global.notes, [global.page]: res.data.data },
            page: global.page + 1,
          });
        });
    },
  });

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24 max-w-[980px] min-width-[980px] m-auto">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <Button onClick={() => setDialogInitial(true)}>
          {global?.username ? global?.username : "Input User Name"}
        </Button>
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white lg:static lg:h-auto lg:w-auto lg:bg-none dark:from-black dark:via-black">
          <a
            className="pointer-events-none flex place-items-center gap-2 p-8 lg:pointer-events-auto lg:p-0"
            href="https://vercel.com?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            By <b>NK</b>
          </a>
        </div>
      </div>

      <div className="flex justify-between items-center w-full mt-5">
        <div>
          <div className="flex items-center space-x-4">
            <Input
              className=""
              placeholder="search username"
              value={global.byUsername}
              onChange={(e: any) => {
                dispatch({ type: "byUsername", byUsername: e.target.value });
                filterByUserNameAsync(mutation);
              }}
            ></Input>
            <div className="flex items-center space-x-2">
              <Checkbox
                disabled={Boolean(global.byUsername)}
                id="terms2"
                onCheckedChange={async (e) => {
                  dispatch({ type: "isFilterAll", isFilterAll: e });
                  await awaita();
                  mutation.mutateAsync(false);
                }}
              />
              <label
                htmlFor="terms2"
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 w-[200px]"
              >
                All Users
              </label>
            </div>
          </div>
        </div>
        <div className="space-x-4">
          <Button
            onClick={async () => {
              dispatch({ type: "resetFilter" });
              await awaita();
              mutation.mutateAsync(false);
            }}
          >
            Reset
          </Button>
          <CreateNoteItem></CreateNoteItem>
        </div>
      </div>
      <div className="flex flex-wrap justify-start">
        {global.notes &&
          Object.values(global.notes)
            .flat()
            .map((note: any, index: any) => (
              <Note key={note.id + index} note={note}></Note>
            ))}
      </div>
      {mutation.isPending ? "---Loading----"
        : (!global.stop) && (
            <div>
              <Button
                variant="secondary"
                onClick={async () => {
                  dispatch({ type: "setPage", page: global.page });
                  await awaita();
                  mutation.mutateAsync(false);
                }}
              >
                Load More
              </Button>
            </div>
          )}

      <div className="before:bg-gradient-radial after:bg-gradient-conic relative z-[-1] flex place-items-center before:absolute before:h-[300px] before:w-full before:-translate-x-1/2 before:rounded-full before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-full after:translate-x-1/3 after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] sm:before:w-[480px] sm:after:w-[240px] before:lg:h-[360px] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40">
        <Image
          className="relative dark:drop-shadow-[0_0_0.3rem_#ffffff70] dark:invert"
          src="/NK.png"
          alt="Note Logo"
          width={280}
          height={37}
          priority
        />
      </div>

      <div className="mb-32 grid text-center lg:mb-0 lg:w-full lg:max-w-5xl lg:grid-cols-4 lg:text-left"></div>
    </main>
  );
}
