import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css"

import MainPage from "./components/pages/MainPage/MainPage";
import LoginPage from "./components/pages/LoginPage/LoginPage";
import { ProtectedRouter } from "./hoc/ProtectedRouter";
import { AuthProvider } from "./hoc/AuthProvider";

function App () {
  return (
    <AuthProvider>
      <BrowserRouter>
      <Routes>
        <Route path='/' element={
          <ProtectedRouter>
            <MainPage />
          </ProtectedRouter>
        } />
        <Route path='/login' element={<LoginPage />} />
      </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;