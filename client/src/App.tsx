import { Routes, Route } from 'react-router-dom';
import FooterCompo from "@/pages/components/footer";

function App() {
    return (
        <Routes>
            <Route path="/" element={<FooterCompo/>} />
        </Routes>
    );
}

export default App;