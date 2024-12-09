import Chat from '../components/chat';
import ChatListWrapper from '../components/chatListwrapper';
import { useState } from 'react';

export default function App() {
  const [chatId, setChatId] = useState('New');
  return (
    <div className="flex w-screen h-screen">
      <ChatListWrapper chatId={chatId} setChatId={setChatId} />
      <Chat chatId={chatId} setChatId={setChatId} />
    </div>
  );
}
