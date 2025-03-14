// chatList.js
import { useContext, useEffect, useState } from 'react';
import ChatListItem from './chatListItem';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { UserContext } from '../context/user';

const ChatList = ({ setChatId, refetchChats }) => {
  const [chatList, setChatList] = useState([]);
  const userInfo = useContext(UserContext);

  const { data, error, isLoading, refetch } = useQuery({
    queryKey: ['myChats'],
    queryFn: async () => {
      const { data } = await axios.get(
        `http://eailab.kangnam.ac.kr:8502/room/myrooms`,
        {
          headers: { Authorization: `Bearer ${userInfo.jwt}` },
        }
      );
      return data;
    },
  });

  useEffect(() => {
    refetchChats.current = refetch;
  }, [refetchChats, refetch]);

  useEffect(() => {
    if (!data) return;
    console.log('load chatlist', data);
    setChatList(data['rooms']);

    if (
      data &&
      data['available_models'] &&
      data['available_models'].length > 0
    ) {
      localStorage.setItem(
        'available_models',
        JSON.stringify(data['available_models'])
      );
    }
  }, [data]);

  const onChatClick = (chat) => {
    console.log('On Chat Click', chat);
    setChatId(chat.id);
  };

  if (isLoading)
    return <div className="w-72 min-w-72 h-full px-6 py-8">Loading...</div>;
  if (error) {
    console.error(error);
    return <div>Error</div>;
  }

  return (
    <div className="w-full h-full px-6">
      {chatList.map((chat) => (
        <ChatListItem
          key={chat.id}
          chat={chat}
          onClick={() => onChatClick(chat)}
        />
      ))}
    </div>
  );
};

export default ChatList;
