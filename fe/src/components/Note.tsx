import moment from "moment";
import { Textarea } from "./ui/textarea";

export const Note = (props: any) => {
  const { content, id, timestamp, username } = props.note;

  return (
    <div
      key={id}
      className="m-2 max-w-[378px] min-w-[378px] max-w-sm overflow-hidden rounded p-4 shadow-lg"
    >
      <div className="flex items-center justify-between space-x-10">
        <Textarea
          value={content}
          disabled
        />
      </div>
      <div className="flex items-center justify-between space-x-10 pt-4">
          <span className="mb-2 mr-2 inline-block rounded-full bg-gray-200 px-3 py-1 text-sm font-semibold text-gray-700">{`At: ${moment(timestamp*1000).fromNow()}`}</span>
          <span className="inline-block rounded-full bg-gray-200 px-3 py-1 text-sm font-semibold text-gray-700">{`By: ${username}`}</span>
      </div>
    </div>
  );
};

export default Note;
