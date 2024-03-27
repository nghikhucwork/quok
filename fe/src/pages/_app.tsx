import {
  QueryClient,
  QueryClientProvider,
  useMutation,
} from "@tanstack/react-query";
import moment from "moment-timezone";
import type { AppProps } from "next/app";
import { useEffect, useReducer, useState } from "react";
import { InitialUserNameDialog } from "~/components/InitialUserNameDialog";
import { Toaster } from "~/components/ui/toaster";
import { useToast } from "~/components/ui/use-toast";
import { request } from "~/lib/request";
import { GlobalContext } from "~/lib/utils";
import "~/styles/globals.css";

moment.tz.setDefault("Asia/Ho_Chi_Minh");

const awaita = (time: number = 200) =>
  new Promise((res) => {
    setTimeout(() => {
      res(null);
    }, time);
  });


function globalReducer(state: any, action: any) {
  switch (action.type) {
    case "byUsername": {
      return { ...state, byUsername: action.byUsername, page: 1, time: undefined, stop: false};
    }
    case "setUser": {
      return { ...state, username: action.username };
    }
    case "isFilterAll": {
      return { ...state, isFilterAll: action.isFilterAll, page: 1, time: undefined, notes: {}, stop: false };
    }
    case "resetFilter": {
      return { ...state, isFilterAll: false, page: 1, time: undefined, notes: {}, stop: false, byUsername: undefined };
    }
    case "setPage": {
      return { ...state, page: action.page, stop: action.stop };
    }
    case "updateNotes": {
      return { ...state, notes: action.notes, page: action.page };
    }
    default: {
      throw Error("Unknown action: " + action.type);
    }
  }
}
const queryClient = new QueryClient();

export default function App({ Component, pageProps }: AppProps) {
  const [dialogInitial, setDialogInitial] = useState(false);

  const [global, dispatch] = useReducer(globalReducer, {
    username: undefined,
    byUsername: undefined,
    notes: {},
    isFilterAll: false,
    page: 1,
    stop: false,
    time: undefined,
  });

  useEffect(() => {
    setDialogInitial(true);
  }, []);

  const { toast } = useToast();

  const submitUserName = async (username: string) => {

    dispatch({ type: "setUser", username });
    await awaita()
    dispatch({ type: "resetFilter" });
    setDialogInitial(false);
    await awaita()

    if(!username) {
      return toast({
        variant: "default",
        title: `Empty`,
      });
    };

    request
      .post("/", {
        method: "GET",
        query: {
          username: global.isFilterAll ? undefined : username,
          page: global.page,
        },
      })
      .then((res) => {
        if(!res?.data?.data?.length) {
          return dispatch({
            type: "setPage",
            page: global.page, stop: true
          });
        }

        dispatch({
          type: "updateNotes",
          notes: { ...global.notes, [global.page]: res.data.data },
          page: global.page + 1,
        });
      });
  };

  return (
    <GlobalContext.Provider
      value={[global, dispatch, queryClient, setDialogInitial]}
    >
      <QueryClientProvider client={queryClient}>
        <InitialUserNameDialog
          open={dialogInitial}
          onOpenChangeDialog={setDialogInitial}
          submitUserName={submitUserName}
        />
        <Component {...pageProps} />
        <Toaster />
      </QueryClientProvider>
    </GlobalContext.Provider>
  );
}
