// src/components/Layout.jsx
import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Layout() {
    const { user, logout, agentDetails } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const formatCredit = (amount) => {
         if (amount === null || amount === undefined) return 'Loading...';
         return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'ETB' }).format(amount);
    }

    return (
        <div className="app-layout">
            <aside className="sidebar">
                <div className="sidebar-header">
                    <h3>Yaba Bingo</h3>
                    <div className="user-profile">
                        <p>{user?.username}</p>
                        <button onClick={handleLogout} className="logout-button">ውጣ</button>
                    </div>
                </div>
                <nav className="sidebar-nav">
                    <NavLink to="/dashboard">ዳሽቦርድ (Dashboard)</NavLink>
                    <NavLink to="/create-game">ጨዋታ ፍጠር (Create Game)</NavLink>
                    <NavLink to="/transactions">ሪፖርቶች (Reports)</NavLink>
                </nav>
                <div className="credit-display">
                    <h4>Operational Credit</h4>
                    <p>{formatCredit(agentDetails?.operational_credit)}</p>
                </div>
            </aside>
            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
}

export default Layout;