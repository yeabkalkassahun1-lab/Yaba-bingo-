// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import TransactionHistoryPage from './pages/TransactionHistoryPage';
import CreateGamePage from './pages/CreateGamePage';
import Layout from './components/Layout';
import './App.css';

function PrivateRoute({ children }) {
    const { user } = useAuth();
    return user ? children : <Navigate to="/login" />;
}

function App() {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route
                        path="/"
                        element={
                            <PrivateRoute>
                                <Layout />
                            </PrivateRoute>
                        }
                    >
                        <Route index element={<Navigate to="/dashboard" replace />} />
                        <Route path="dashboard" element={<DashboardPage />} />
                        <Route path="transactions" element={<TransactionHistoryPage />} />
                        <Route path="create-game" element={<CreateGamePage />} />
                    </Route>
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;