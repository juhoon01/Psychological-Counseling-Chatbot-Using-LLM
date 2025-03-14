import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';

const Login = ({ setJWT }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const mutation = useMutation({
    mutationFn: async (user) =>
      await axios.post(`http://eailab.kangnam.ac.kr:8502/user/me/login`, user),
    onSuccess: async (data) => {
      console.log(data.data);
      if (data.status === 200 && data.data.success) {
        const token = data.data['token']['access_token'];
        if (token) {
          localStorage.setItem('x-jwt', token);
          setJWT(token);
          return;
        }
      }
      alert(`Error: ${data.data.message}`);
    },
    onError: (error) => {
      alert(`Error: ${error.response.data.message ?? 'Something went wrong'}`);
    },
  });

  const handleLogin = () => {
    mutation.mutate({
      email: email,
      password: password,
    });
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className=" min-w-[40%] flex flex-col items-center justify-center p-4">
        <h1 className="text-4xl mb-8">Login</h1>
        <input
          type="text"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-2 mb-4 border border-gray-400 rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 mb-4 border border-gray-400 rounded"
        />
        <button
          onClick={handleLogin}
          className="w-full py-2 mb-4 bg-blue-500 text-white rounded"
        >
          Login
        </button>
        <Link to="/signup" className="text-purple-600">
          Go to Signup
        </Link>
      </div>
    </div>
  );
};

export default Login;
