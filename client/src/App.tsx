import { Routes, Route } from 'react-router-dom';
import AboutUs from "@/pages/AboutUs";
import HomePage from "@/pages/Home";

import { ThemeProvider } from "./components/ThemeContext"
import "./App.css"
import HeaderCompo from "@/pages/components/Header";
import AuthPage from "@/pages/AuthPage"
import FooterCompo from "@/pages/components/Footer";
import ChatPage from "@/pages/Chat";
import ServicesPage from "@/pages/Services";

function App() {
    return (
        <ThemeProvider>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/Aboutus" element={<AboutUs/>} />
                <Route path="/auth" element={<AuthPage />} />
                <Route path="/login" element={<AuthPage />} />
                <Route path="/register" element={<AuthPage />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/services" element={<ServicesPage />} />
            </Routes>
        </ThemeProvider>

    );
}

export default App;