import { datetimeStringFormat } from '../utils/date';

const ChatListItem = ({ chat, onClick }) => {
  return (
    <div
      key={chat.id}
      onClick={onClick}
      className="cursor-pointer mb-4 flex flex-col justify-start items-start border-b-[0.5px] border-solid border-gray-200 pb-3"
    >
      <div className="w-full flex justify-between items-baseline">
        <div className="text-md font-semibold ">
          {chat.chats.length > 0
            ? String(chat.chats[0].model)
            : 'Model not found'}
        </div>
        <div className="text-sm text-gray-400">
          {datetimeStringFormat(chat.created_at)}
        </div>
      </div>
      <div className="w-full flex justify-start items-baseline text-sm text-gray-500">
        {chat.chats.length > 0
          ? String(chat.chats[0].ask).slice(0, 20)
          : 'Chat not found'}
        ...
      </div>
    </div>
  );
};

export default ChatListItem;
