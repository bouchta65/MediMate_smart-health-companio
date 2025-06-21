import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./components/ThemeContext"
import AboutUs from "./pages/AboutUs"
import ThemeToggle from "./components/ThemeToggle"
import "./App.css"

function App() {
    return (
        <Router>
                <ThemeProvider>
                    <div className="relative">
                        {/* Theme Toggle Button - Fixed Position */}
                        <div className="fixed top-6 right-6 z-50">
                        <ThemeToggle />
                        </div>

                        {/* About Us Page */}
                        <AboutUs />
                    </div>
                </ThemeProvider>
            <Routes>
                <Route path="/" element={<div>HomePage</div>} />
                <Route path="/Profile" element={<div>Profile</div>} />
                <Route path="/History" element={<div>History</div>} />
            </Routes>
        </Router>
    );
}

export default App;
