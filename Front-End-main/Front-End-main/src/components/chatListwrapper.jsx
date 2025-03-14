// chatListWrapper.js
import { useState, useRef, useContext } from 'react';
import { FaSync, FaPlus } from 'react-icons/fa';
import ChatList from './chatList';
import axios from 'axios';
import { UserContext } from '../context/user';

const ChatListWrapper = ({ setChatId, chatId }) => {
  const userInfo = useContext(UserContext);
  const refetchChats = useRef(null);

  const handleRefresh = () => {
    if (refetchChats.current) {
      refetchChats.current();
    }
  };

  const handleNewChat = () => {
    setChatId('New');
  };

  const inspectChats = async () => {
    if (chatId) {
      try {
        const response = await axios.get(
          `http://eailab.kangnam.ac.kr:8502/chat/inspect/${chatId}`,
          {
            headers: { Authorization: `Bearer ${userInfo.jwt}` },
          }
        );
        console.log(response);
        if (response.status === 200) {
          if (response.data.success) {
            const status = response.data['status'];
            console.log('status', status);
            alert(`당신의 채팅은 ${status} 상태입니다.`);
          } else {
            alert('적어도 3개의 채팅이 필요합니다.');
          }
        } else {
          throw new Error('Failed to inspect chat');
        }
      } catch (error) {
        alert(error.response?.data?.message ?? 'Something went wrong');
      }
    }
  };

  const logout = () => {
    localStorage.removeItem('x-jwt');
    window.location.reload();
  };

  return (
    <div className="w-72 min-w-72 h-full pb-6 overflow-y-auto border border-r-[1px] border-solid border-gray-200">
      <div className="sticky top-0 bg-white flex flex-col border-b-[1px] border-solid border-gray-300">
        <div className="flex justify-start items-center bg-white pt-4 pl-6">
          <img
            src={`http://eailab.kangnam.ac.kr:8502/raw/profile/${userInfo.id}`}
            alt="Pf"
            className=" rounded-full w-12 h-12 border border-solid border-gray-400 mr-3 object-cover"
          />
          <div className="flex flex-col justify-start items-start">
            <div className="font-bold">{userInfo.email}</div>
            <div
              onClick={() => logout()}
              className="font-bold text-sm text-red-500"
            >
              Log out
            </div>
          </div>
        </div>
        <div className="flex justify-around items-center bg-white py-4">
          <button
            className="flex items-center space-x-2 text-gray-600 hover:text-white hover:bg-blue-500 ease-in-out duration-200 border border-gray-300 rounded-md px-4 pb-3 pt-4"
            onClick={handleRefresh}
          >
            <FaSync />
            <span>새로고침</span>
          </button>
          <button
            className="flex items-center space-x-2 text-gray-600 hover:text-white hover:bg-blue-500 ease-in-out duration-200 border border-gray-300 rounded-md px-4 pb-3 pt-4"
            onClick={handleNewChat}
          >
            <FaPlus />
            <span>New</span>
          </button>
        </div>
        <button
          className="flex items-center justify-centerspace-x-2 text-gray-600 hover:text-white hover:bg-blue-500 ease-in-out duration-200 border border-gray-300 rounded-md px-4 pb-3 pt-4 mb-4 mx-5"
          onClick={inspectChats}
        >
          <FaPlus />
          <span className="pl-2 pt-[2px] font-bold text-lg">Inspect</span>
        </button>
      </div>
      <div className="h-4" />
      <ChatList setChatId={setChatId} refetchChats={refetchChats} />
    </div>
  );
};

export default ChatListWrapper;
