import { Routes, Route } from 'react-router-dom';
import FooterCompo from "@/pages/components/footer";
import AboutUs from "@/pages/AboutUs";

import { ThemeProvider } from "./components/ThemeContext"
import ThemeToggle from "./components/ThemeToggle"
import "./App.css"

function App() {
    return (
        <ThemeProvider>
            <Routes>
                <Route path="/" element={<FooterCompo/>} />
                <Route path="/Aboutus" element={<AboutUs/>} />
            </Routes>
        </ThemeProvider>

    );
}

export default App;