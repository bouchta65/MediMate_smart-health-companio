import { Routes, Route } from 'react-router-dom';
import AboutUs from "@/pages/AboutUs";
import HomePage from "@/pages/Home";

import { ThemeProvider } from "./components/ThemeContext"
import "./App.css"
import HeaderCompo from "@/pages/components/Header";
import FooterCompo from "@/pages/components/Footer";

function App() {
    return (
        <ThemeProvider>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/Aboutus" element={<AboutUs/>} />
            </Routes>
        </ThemeProvider>

    );
}

export default App;