import { Route, Routes } from 'react-router-dom';
import Login from '../screens/login';
import Signup from '../screens/signup';

export default function OuterRouter({ setJWT }) {
  return (
    <Routes>
      <Route path="/login" element={<Login setJWT={setJWT} />} />
      <Route path="/signup" element={<Signup setJWT={setJWT} />} />
      <Route path="/*" element={<Login setJWT={setJWT} />} />
    </Routes>
  );
}
