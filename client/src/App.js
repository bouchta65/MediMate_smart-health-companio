import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<div>HomePage</div>} />
                <Route path="/About" element={<div>About</div>} />
                <Route path="/Profile" element={<div>Profile</div>} />
                <Route path="/History" element={<div>History</div>} />
            </Routes>
        </Router>
    );
}

export default App;
