import { Routes, Route } from 'react-router-dom';
import AboutUs from "@/pages/AboutUs";

import { ThemeProvider } from "./components/ThemeContext"
import "./App.css"
import HeaderCompo from "@/pages/components/Header";
import FooterCompo from "@/pages/components/Footer";
import ProfilePage from '@/pages/ProfilePage';

function App() {
    return (
        <ThemeProvider>
            <Routes>
                <Route path="/" element={<HeaderCompo/>} />
                <Route path="/Aboutus" element={<AboutUs/>} />
                <Route path="/profile" element={<ProfilePage />} />
            </Routes>
        </ThemeProvider>

    );
}

export default App;