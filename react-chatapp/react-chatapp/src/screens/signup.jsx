import React, { useRef, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';

const Signup = ({ navigate, setJWT }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const [image, setImage] = useState(null);
  const jwt = useRef(null);
  const [imagePreview, setImagePreview] = useState(
    'default_profile_image.jpeg'
  );

  const handleImageClick = () => {
    document.getElementById('imageInput').click();
  };

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImage(file);
      const imageUrl = URL.createObjectURL(file);
      setImagePreview(imageUrl);
    }
  };

  const imageMutation = useMutation({
    mutationFn: async () => {
      const formData = new FormData();
      formData.append('file', image);

      const response = await axios.post(
        `http://eailab.kangnam.ac.kr:8502/user/upload/profile`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${jwt.current}`,
          },
        }
      );
      return response;
    },
    onSuccess: async (data) => {
      if (data.status === 200 && data.data.success) {
        setJWT(jwt.current);
        // 필요한 경우 다음 페이지로 이동
      } else {
        alert(`Error: ${data.data.message}`);
      }
    },
    onError: (error) => {
      alert(`Error: ${error.response.data.message ?? 'Something went wrong'}`);
    },
  });

  const mutation = useMutation({
    mutationFn: async (user) => {
      const res = await axios.post(
        `http://eailab.kangnam.ac.kr:8502/user/me`,
        user
      );
      return res;
    },
    onSuccess: async (data) => {
      if (data.status === 200 && data.data.success) {
        const res_jwt = data.data['token']['access_token'];
        if (!res_jwt) {
          throw new Error('JWT is not found');
        }
        jwt.current = res_jwt;
        localStorage.setItem('x-jwt', res_jwt);
        if (image) {
          imageMutation.mutate();
        } else {
          setJWT(jwt.current);
        }
      } else {
        alert(`Error: ${data.data.message}`);
      }
    },
    onError: (error) => {
      alert(`Error: ${error.response.data.message ?? 'Something went wrong'}`);
    },
  });

  const handleLogin = () => {
    try {
      mutation.mutate({
        name: name,
        email: email,
        password: password,
        access_code: accessToken,
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className=" min-w-[40%] flex flex-col items-center justify-center p-4">
        <h1 className="text-4xl mb-8">SignUp</h1>
        <div
          className=" w-40 h-40 rounded-full overflow-hidden border-4 border-solid border-gray-200 mb-10"
          style={{
            backgroundImage: `url(${imagePreview})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            cursor: 'pointer',
          }}
          onClick={handleImageClick}
        >
          <input
            className="hidden"
            type="file"
            id="imageInput"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full p-2 mb-4 border border-gray-400 rounded"
        />
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
        <input
          type="password"
          placeholder="Access Token"
          value={accessToken}
          onChange={(e) => setAccessToken(e.target.value)}
          className="w-full p-2 mb-4 border border-gray-400 rounded"
        />
        <button
          onClick={handleLogin}
          className="w-full py-2 mb-4 bg-blue-500 text-white rounded"
        >
          Signup
        </button>
        <Link to="/login" className="text-purple-600">
          Go to Login
        </Link>
      </div>
    </div>
  );
};

export default Signup;
