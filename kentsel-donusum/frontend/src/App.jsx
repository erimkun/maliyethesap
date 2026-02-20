import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AnaSayfa from './pages/AnaSayfa';
import AdminPanel from './pages/AdminPanel';

function App() {
    return (
        <div className="font-sans antialiased text-gray-900 bg-gray-50 min-h-screen">
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<AnaSayfa />} />
                    <Route path="/admin" element={<AdminPanel />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
