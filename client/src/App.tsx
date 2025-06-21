import { Routes, Route } from 'react-router-dom';
import AboutUs from "@/pages/AboutUs";

import { ThemeProvider } from "./components/ThemeContext"
import "./App.css"
import HeaderCompo from "@/pages/components/Header";
import AuthPage from "@/pages/AuthPage"
import FooterCompo from "@/pages/components/Footer";

function App() {
    return (
        <ThemeProvider>
            <Routes>
                <Route path="/" element={<HeaderCompo/>} />
                <Route path="/Aboutus" element={<AboutUs/>} />
                <Route path="/auth" element={<AuthPage />} />
                <Route path="/login" element={<AuthPage />} />
                <Route path="/register" element={<AuthPage />} />
            </Routes>
        </ThemeProvider>

    );
}

export default App;