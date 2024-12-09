import React, { useEffect, useState, useCallback, useContext } from 'react';
import axios from 'axios';
import { useMutation } from '@tanstack/react-query';
import { UserContext } from '../context/user';

const Chat = ({ chatId, setChatId }) => {
  const userInfo = useContext(UserContext);
  const [messages, setMessages] = useState([]);
  const [modelName, setModelName] = useState('MentalLlm');
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const getChatList = async () => {
      if (chatId && chatId !== 'New') {
        try {
          console.log('userInfo', userInfo);
          const response = await axios.get(
            `http://eailab.kangnam.ac.kr:8502/chat/room/${chatId}`,
            {
              headers: { Authorization: `Bearer ${userInfo.jwt}` },
            }
          );
          if (
            response.status === 200 &&
            response.data.success &&
            response.data['room']
          ) {
            const chats = response.data['room']['chats'] ?? [];
            console.log('chats', chats);
            const messages = [];
            chats.forEach((chat) => {
              console.log('RESponse chat', chat);
              // User's message
              messages.push({
                id: `${chat.id}-ask`,
                text: chat.ask,
                time: new Date(chat.timestamp).toLocaleString(),
                user: chat.user_name || userInfo.userName,
                role: 'user',
              });
              // Assistant's message
              messages.push({
                id: `${chat.id}-answer`,
                text: chat.answer,
                time: new Date(chat.timestamp).toLocaleString(),
                user: 'assistant',
                role: 'assistant',
              });
            });
            setMessages(messages);
          }
        } catch (error) {
          alert(error.response?.data?.message ?? 'Something went wrong');
        }
      }
    };
    console.log('ChatId has changed', chatId);
    if (chatId) {
      if (chatId === 'New') {
        setMessages([]);
      } else {
        getChatList();
      }
    }
  }, [chatId, userInfo]);

  const mutation = useMutation({
    mutationFn: async (postData) =>
      await axios.post(
        `http://eailab.kangnam.ac.kr:8502/chat/create`,
        postData,
        {
          headers: { Authorization: `Bearer ${userInfo.jwt}` },
        }
      ),
    onSuccess: (data) => {
      if (data.status === 200 && data.data['success'] && data.data['chat']) {
        if (!chatId || chatId === 'New') {
          console.log('Set chatId to', data.data['chat']['room_id']);
          setChatId(data.data['chat']['room_id']);
        }

        const chat = data.data['chat'];

        const assistantMessage = {
          id: `${chat.id}-answer`,
          text: '',
          time: new Date(chat.timestamp).toLocaleString(),
          user: 'assistant',
          role: 'assistant',
        };

        setMessages((prevMessages) => [...prevMessages, assistantMessage]);

        displayMessageOneByOne(
          assistantMessage.id,
          chat.answer ?? 'Something went wrong...'
        );
        setIsLoading(false);
      } else {
        alert(data.data.message);
        setIsLoading(false);
      }
    },
    onError: (error) => {
      alert(error.response?.data?.message ?? 'Something went wrong');
      setIsLoading(false);
    },
  });

  const displayMessageOneByOne = (id, text) => {
    let index = 0;
    const interval = setInterval(() => {
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === id ? { ...msg, text: msg.text + text[index] } : msg
        )
      );
      index++;
      if (index >= text.length) {
        clearInterval(interval);
      }
    }, 20);
  };

  const handleSend = useCallback(
    (e) => {
      e.preventDefault();
      if (inputText.trim()) {
        const newMessage = {
          id: Math.random(),
          text: inputText,
          time: new Date().toLocaleString(),
          user: userInfo.userName,
          role: 'user',
        };
        setMessages((prevMessages) => [...prevMessages, newMessage]);

        setIsLoading(true);
        mutation.mutate({
          model: modelName,
          ask: inputText,
          room_id: chatId === 'New' ? null : chatId,
        });
        setInputText('');
      }
    },
    [inputText, mutation, modelName, userInfo.userName, chatId]
  );

  if (!chatId)
    return (
      <div className="w-full h-full px-6 py-8 bg-gray-100 flex justify-center items-center text-xl font-bold">
        채팅을 선택해주세요.
      </div>
    );

  return (
    <div className="w-full h-full flex flex-col bg-white rounded-lg p-4">
      <div className="flex-1 overflow-y-auto mb-4 flex flex-col">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`w-[90%] p-4 rounded-lg mb-4 ${
              message.role === 'user'
                ? 'bg-blue-100 self-end'
                : 'bg-gray-100 self-start'
            }`}
          >
            <div className="text-sm text-gray-700 mb-1">{message.user}</div>
            <div className="mb-2 leading-relaxed">
              {message.text}
              {message.role === 'assistant' && message.text === '' && (
                <span className="loading-dots ml-2">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </span>
              )}
            </div>
            <div className="text-xs text-gray-500">{message.time}</div>
          </div>
        ))}
      </div>
      <form className="flex items-center" onSubmit={handleSend}>
        <input
          type="text"
          className="flex-1 p-2 border border-gray-300 rounded-lg mr-2 outline-none"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type a message"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="bg-blue-500 text-white p-2 rounded-lg"
          disabled={isLoading}
        >
          Send
        </button>
      </form>
      <style>{`
        .loading-dots {
          display: inline-block;
        }
        .dot {
          display: inline-block;
          width: 6px;
          height: 6px;
          margin: 0 2px;
          background-color: #333;
          border-radius: 50%;
          animation: loading 1s infinite;
        }
        .dot:nth-child(1) {
          animation-delay: 0s;
        }
        .dot:nth-child(2) {
          animation-delay: 0.2s;
        }
        .dot:nth-child(3) {
          animation-delay: 0.4s;
        }
        @keyframes loading {
          0% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-5px);
          }
          100% {
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default Chat;
