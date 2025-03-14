// src/routers/InnerRouter.js

import React from 'react';
import axios from 'axios';
import { useQuery } from '@tanstack/react-query';
import { UserContext } from '../context/user';
import { Route, Routes } from 'react-router-dom';
import App from '../screens/App';
import Loading from '../screens/loading';

// Define a function to fetch user data
const fetchUser = async (jwt) => {
  const response = await axios.get(`http://eailab.kangnam.ac.kr:8502/user/me`, {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${jwt}`,
    },
  });
  if (response.status !== 200 || !response.data['user']) {
    let errorMessage = '사용자 정보를 가져오는 데 실패했습니다.';
    // localstorage에 'x-jwt' 제거.
    localStorage.removeItem('x-jwt');
    throw new Error(errorMessage);
  }

  return { ...response.data['user'], jwt };
};

export default function InnerRouter({ jwt }) {
  const {
    data: user,
    error,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ['user', jwt],
    queryFn: () => fetchUser(jwt),
    enabled: !!jwt,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 1,
  });

  if (isLoading) {
    return <Loading />;
  }

  if (isError) {
    localStorage.removeItem('x-jwt');
    return <div>에러가 발생했습니다: {error.message}</div>;
  }

  return (
    <UserContext.Provider value={user}>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="*" element={<App />} />
      </Routes>
    </UserContext.Provider>
  );
}
