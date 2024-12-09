import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import InnerRouter from './innerRouter';
import OuterRouter from './outerRouter';
import axios from 'axios';

const queryClient = new QueryClient();

export default function Router() {
  const [jwt, setJWT] = useState(null);

  useEffect(() => {
    axios
      .get('http://eailab.kangnam.ac.kr:8502')
      .then(() => {
        console.log('Server is up');
      })
      .catch(() => {
        console.error('Server is down');
        localStorage.removeItem('x-jwt');
        alert('서버와 연결할 수 없습니다.');
      });
    const getJwt = () => localStorage.getItem('x-jwt');
    setJWT(getJwt());
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {jwt ? <InnerRouter jwt={jwt} /> : <OuterRouter setJWT={setJWT} />}
      </BrowserRouter>
    </QueryClientProvider>
  );
}
